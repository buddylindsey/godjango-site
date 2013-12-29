import views

from django.http import HttpRequest, Http404
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
from episode.models import Video


class CartViewTest(TestCase):
    def setUp(self):
        factory = RequestFactory()
        request = factory.get(reverse('cart'))
        #request.user = mommy.make('auth.User')
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


class CheckoutTest(TestCase):
    def _create_user(self):
        return User.objects.create_user(
            'buddy', 'buddy@buddylindsey.com', 'mypass')

    def setUp(self):
        self.user = self._create_user()
        self.video = mommy.make(Video, title='awesome', price=9.99)
        self.factory = RequestFactory()
        self.subscription = mommy.make(
            Subscription, price=9.00, plan='monthly', title='Pro')

    def test_login_required_checkout_url(self):
        request = self.factory.get(reverse('checkout'))
        request.user = AnonymousUser()
        response = views.checkout(request)

        self.assertEqual(response.status_code, 302)

    def test_checkout_url_logged_in(self):
        request = self.factory.get(reverse('checkout'))
        request.user = self.user
        request.session = {}
        response = views.checkout(request)

        self.assertEqual(response.status_code, 200)

    def test_invalid_form(self):
        request = self.factory.post(
            reverse('checkout'), {'stripeToke': 'xxxxxxxxxx'})
        request.user = self.user
        request.session = {}

        response = views.checkout(request)
        self.assertContains(
            response, 'Problem with your card please try again')

    @patch('payments.models.Customer.update_card')
    @patch('payments.models.Customer.subscribe')
    @patch('payments.models.Customer.charge')
    def test_valid_form(self, UpdateMock, SubscribeMock, ChargeMock):
        mommy.make(Customer, user=self.user, stripe_id=1)

        request = self.factory.post(
            '/cart/checkout/', {'stripeToken': 'xxxxxxxxxx'})
        request.user = self.user
        request.session = {}

        cart = TheCart(request)
        cart.add(self.subscription, self.subscription.price, 1)

        response = views.checkout(request)
        self.assertEqual(response.status_code, 302)

    @patch('payments.models.Customer.update_card')
    @patch('payments.models.Customer.subscribe')
    @patch('payments.models.Customer.charge')
    def test_email_change_while_checkingout(
        self, UpdateMock, SubscribeMock, ChargeMock):

        mommy.make(Customer, user=self.user, stripe_id=1)

        request = self.factory.post(
            reverse('checkout'),
            {'stripeToken': 'xxxxxxxxxx', 'email': 'other@other.com'}
        )
        request.user = self.user
        request.session = {}

        cart = TheCart(request)
        cart.add(self.subscription, self.subscription.price, 1)

        self.assertEqual(request.user.email, 'buddy@buddylindsey.com')
        response = views.checkout(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(request.user.email, 'other@other.com')

    def test_get_customer_attached_to_user(self):
        Customer.objects.create(user=self.user, stripe_id=1)

        self.assertEqual(1, self.user.customer.stripe_id)


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
