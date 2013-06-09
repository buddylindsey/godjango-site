import views

from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from mock import patch
from cart import Cart as TheCart
from cart.models import Cart
from payments.models import Customer

from .utils import get_customer, update_email
from .models import Subscription
from episode.models import Video

class CartUrlsTest(TestCase):
    def _create_user(self):
        return User.objects.create_user('buddy', 'buddy@buddylindsey.com', 'mypass')

    def _create_video(self):
        video = Video()
        video.title = "I are title"
        video.description = "I am a lonely description"
        video.price = 9.99
        video.save()
        return video

    def setUp(self):
        user = self._create_user()
        self.client.login(username='buddy', password='mypass')

    def test_add_url(self):
        video = self._create_video()

        response = self.client.post(
            reverse('add_to_cart'), 
            {'video_pk':video.id,}, 
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(200, response.status_code)

    def test_remove_url(self):
        video = self._create_video()

        response = self.client.post(
            reverse('add_to_cart'), 
            {'video_pk':video.id,}, 
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        response = self.client.post(
            reverse('remove_from_cart'),
            {'video_pk':video.id,}, 
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(200, response.status_code)

    def test_checkout_url(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(200, response.status_code)

class CartCartTest(TestCase):
    def _create_user(self):
        return User.objects.create_user('buddy', 'buddy@buddylindsey.com', 'mypass')

    def _create_video(self):
        video = Video()
        video.title = "I are title"
        video.description = "I am a lonely description"
        video.price = 9.99
        video.save()
        return video

    def setUp(self):
        user = self._create_user()
        self.client.login(username='buddy', password='mypass')

    def test_cart_creation(self):
        video = self._create_video()

        self.assertEqual(0, Cart.objects.count())
        response = self.client.post(
            reverse('add_to_cart'), 
            {'video_pk':video.id,}, 
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(200, response.status_code)

        self.assertEqual(1, Cart.objects.count())

    def test_cart_items(self):
        video = self._create_video()

        self.assertEqual(0, Cart.objects.count())
        response = self.client.post(
            reverse('add_to_cart'), 
            {'video_pk':video.id,}, 
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(200, response.status_code)
        cart = Cart.objects.all()[0]

        self.assertEqual(1, cart.item_set.count())

    def test_remove_from_cart(self):
        video = self._create_video()

        self.assertEqual(0, Cart.objects.count())
        response = self.client.post(
            reverse('add_to_cart'), 
            {'video_pk':video.id,}, 
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(200, response.status_code)
        cart = Cart.objects.all()[0]
        self.assertEqual(1, cart.item_set.count())

        response = self.client.post(
            reverse('remove_from_cart'),
            {'video_pk':video.id,},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(200, response.status_code)
        cart = Cart.objects.all()[0]
        self.assertEqual(0, cart.item_set.count())

class CheckoutTest(TestCase):
    def _create_user(self):
        return User.objects.create_user('buddy', 'buddy@buddylindsey.com', 'mypass')

    def _create_video(self):
        video = Video()
        video.title = "I are title"
        video.description = "I am a lonely description"
        video.price = 9.99
        video.save()
        return video

    def setUp(self):
        self.user = self._create_user()
        self.video = self._create_video()
        self.factory = RequestFactory()
        sub = Subscription()
        sub.price = 9.00
        sub.plan = 'monthly'
        sub.title = 'Pro'
        sub.save()

    def test_login_required_checkout_url(self):
        request = self.factory.get('/cart/checkout/')
        request.user = AnonymousUser()
        response = views.checkout(request)
        self.assertEqual(response.status_code, 302)

    def test_checkout_url_logged_in(self):
        request = self.factory.get('/cart/checkout/')
        request.user = self.user
        request.session = {}
        response = views.checkout(request)
        self.assertEqual(response.status_code, 200)

    def test_invalid_form(self):
        request = self.factory.post(
            '/cart/checkout/', 
            {'stripeToke':'xxxxxxxxxx'}
        )
        request.user = self.user
        request.session = {}

        response = views.checkout(request)
        self.assertContains(
            response, 
            'Problem with your card please try again'
        )

    @patch('payments.models.Customer.update_card')
    @patch('payments.models.Customer.subscribe')
    @patch('payments.models.Customer.charge')
    def test_valid_form(self, UpdateMock, SubscribeMock, ChargeMock):
        Customer.objects.create(
            user=self.user,
            stripe_id=1
        )

        request = self.factory.post(
            '/cart/checkout/', 
            {'stripeToken':'xxxxxxxxxx'}
        )
        request.user = self.user
        request.session = {}

        cart = TheCart(request)
        sub = Subscription.objects.get(plan='monthly')
        cart.add(sub, sub.price, 1)

        response = views.checkout(request)
        self.assertEqual(response.status_code, 302)

    @patch('payments.models.Customer.update_card')
    @patch('payments.models.Customer.subscribe')
    @patch('payments.models.Customer.charge')
    def test_email_change_while_checkingout(self, UpdateMock, SubscribeMock, ChargeMock):
        Customer.objects.create(
            user=self.user,
            stripe_id=1
        )

        request = self.factory.post(
            '/cart/checkout/', 
            {
                'stripeToken':'xxxxxxxxxx',
                'email': 'other@other.com'
            }
        )
        request.user = self.user
        request.session = {}

        cart = TheCart(request)
        sub = Subscription.objects.get(plan='monthly')
        cart.add(sub, sub.price, 1)

        self.assertEqual(request.user.email, 'buddy@buddylindsey.com')
        response = views.checkout(request)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(pk=1)
        self.assertEqual(request.user.email, 'other@other.com')

    @patch('payments.models.Customer.create')
    def test_get_customer(self, CreateMock):
        CreateMock.return_value = Customer()
        customer = get_customer(self.user)
        self.assertEqual(type(Customer()), type(customer))

    def test_get_customer_attached_to_user(self):
        customer = Customer.objects.create(
            user=self.user,
            stripe_id=1
        )

        customer = get_customer(self.user)
        self.assertEqual(1, self.user.customer.stripe_id)

class UtilTest(TestCase):
    def _create_user(self):
        return User.objects.create_user('buddy', 'buddy@buddylindsey.com', 'mypass')

    def setUp(self):
        self.user = self._create_user()

    @patch('payments.models.Customer.create')
    def test_get_customer(self, CreateMock):
        CreateMock.return_value = Customer()
        customer = get_customer(self.user)
        self.assertEqual(type(Customer()), type(customer))

    def test_update_email(self):
        update = update_email(self.user, 'other@other.com')
        self.assertEqual(update, 'other@other.com')
