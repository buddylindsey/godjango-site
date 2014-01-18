import views
import mox

#from django.http import HttpRequest, Http404
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from mock import patch
from cart import Cart as TheCart
from cart.models import Cart
from payments.models import Customer
from model_mommy import mommy

from .utils import get_customer, update_email
from .models import Subscription
from .forms import CheckoutForm
from episode.models import Video


class CartViewTest(TestCase):
    def setUp(self):
        factory = RequestFactory()
        request = factory.get(reverse('cart'))
        request.user = AnonymousUser()
        request.session = {}

        self.view = views.CartView()
        self.view.request = request

    def test_attrs(self):
        self.assertEqual(self.view.template_name, 'godjango_cart/cart.html')

    def test_cart_context_data(self):
        context_data = self.view.get_context_data()
        self.assertIsInstance(context_data['cart'], TheCart)

    def test_not_logged_in(self):
        self.view.request.user = AnonymousUser()
        response = self.view.dispatch(self.view.request)
        self.assertEqual(302, response.status_code)

    def test_login_required(self):
        self.view.request.user = mommy.make('auth.User')
        response = self.view.dispatch(self.view.request).render()
        self.assertEqual(200, response.status_code)


class CartCartTest(TestCase):
    def setUp(self):
        self.user = mommy.make('auth.User')
        self.video = mommy.make(Video, title='awesome', price=9.00)
        self.client.login(username=self.user.username, password='mypass')

        factory = RequestFactory()
        self.request = factory.post(reverse('add_to_cart'))
        self.request.POST = {'video_pk': self.video.id}
        self.request.session = {}

    def test_is_ajax(self):
        self.request.META.update({'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        view = views.CartAddView()
        view.request = self.request
        response = view.dispatch(self.request)
        self.assertEqual(200, response.status_code)

    def test_cart_and_items(self):
        self.assertEqual(0, Cart.objects.count())

        view = views.CartAddView()
        view.request = self.request
        response = view.post(self.request)

        self.assertEqual(200, response.status_code)

        self.assertEqual(1, Cart.objects.count())

        cart = Cart.objects.all()[0]
        self.assertEqual(1, cart.item_set.count())

    def test_remove_from_cart(self):
        self.assertEqual(0, Cart.objects.count())

        cart = TheCart(self.request)
        cart.add(self.video, self.video.price, 1)

        view = views.CartRemoveView()
        view.request = self.request
        response = view.post(self.request)

        self.assertEqual(200, response.status_code)
        cart = Cart.objects.all()[0]
        self.assertEqual(0, cart.item_set.count())


class CheckoutViewTest(TestCase):
    def setUp(self):
        self.view = views.CheckoutView()
        self.mock = mox.Mox()

        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('checkout'))
        self.request.user = mommy.make('auth.User', email='test@example.com')
        self.request.session = {}
        self.request.POST = {'stripeToken': 'xxxxxxxxxx'}

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_attrs(self):
        self.assertEqual(self.view.form_class, CheckoutForm)
        self.assertEqual(
            self.view.template_name, 'godjango_cart/checkout.html')
        self.assertEqual(self.view.success_url, reverse('order_confirmation'))

    def test_get_context_data(self):
        self.mock.StubOutWithMock(views.CartMixin, 'get_cart')
        views.CartMixin.get_cart().AndReturn('hello')

        self.mock.ReplayAll()
        context = self.view.get_context_data()
        self.mock.VerifyAll()

        self.assertEqual(
            context['publishable_key'], settings.STRIPE_PUBLIC_KEY)
        self.assertEqual(context['cart'], 'hello')

    def test_successful_purchase(self):
        customer = mommy.make('payments.Customer')

        form = CheckoutForm(self.request.POST)
        self.assertTrue(form.is_valid())

        subscription = mommy.make('godjango_cart.Subscription', plan="monthly")
        cart = TheCart(self.request)
        cart.add(subscription, 9.00, 1)

        self.mock.StubOutWithMock(self.view, 'get_form_kwargs')
        self.mock.StubOutWithMock(views.CartMixin, 'get_cart')
        self.mock.StubOutWithMock(views.CustomerMixin, 'get_customer')
        self.mock.StubOutWithMock(customer, 'can_charge')
        self.mock.StubOutWithMock(customer, 'subscribe')

        self.view.get_form_kwargs().AndReturn({'data': {}})
        views.CartMixin.get_cart().AndReturn(cart)
        views.CustomerMixin.get_customer().AndReturn(customer)
        customer.can_charge().AndReturn(True)
        customer.subscribe('monthly')

        self.mock.ReplayAll()
        response = self.view.form_valid(form)
        self.mock.VerifyAll()

        self.assertEqual(response.status_code, 302)

    def test_successful_purchase_with_coupon(self):
        customer = mommy.make('payments.Customer')
        self.request.POST.update({'coupon': 'allthethings'})

        form = CheckoutForm(self.request.POST)
        self.assertTrue(form.is_valid())

        subscription = mommy.make('godjango_cart.Subscription', plan="monthly")
        cart = TheCart(self.request)
        cart.add(subscription, 9.00, 1)

        self.mock.StubOutWithMock(self.view, 'get_form_kwargs')
        self.mock.StubOutWithMock(views.CartMixin, 'get_cart')
        self.mock.StubOutWithMock(views.CustomerMixin, 'get_customer')
        self.mock.StubOutWithMock(customer, 'can_charge')
        self.mock.StubOutWithMock(customer, 'subscribe')

        self.view.get_form_kwargs().AndReturn(
            {'data': {'coupon': 'allthethings'}})
        views.CartMixin.get_cart().AndReturn(cart)
        views.CustomerMixin.get_customer().AndReturn(customer)
        customer.can_charge().AndReturn(True)
        customer.subscribe('monthly', coupon='allthethings')

        self.mock.ReplayAll()
        response = self.view.form_valid(form)
        self.mock.VerifyAll()

        self.assertEqual(response.status_code, 302)


class UtilTest(TestCase):
    def setUp(self):
        self.user = mommy.make('auth.User')

    @patch('payments.models.Customer.create')
    def test_get_customer(self, CreateMock):
        CreateMock.return_value = Customer()
        customer = get_customer(self.user)
        self.assertIsInstance(customer, Customer)

    def test_update_email(self):
        update = update_email(self.user, 'other@other.com')
        self.assertEqual(self.user.email, update)
