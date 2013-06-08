from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from mock import patch

from episode.models import Video
from cart.models import Cart
from payments.models import Customer
import views
from .utils import get_customer

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

def fakefunc():
    return True

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
        self.factory = RequestFactory()

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
        request = self.factory.post('/cart/checkout/', {'stripeToke':'xxxxxxxxxx'})
        request.user = self.user
        request.session = {}

        response = views.checkout(request)
        self.assertContains(response, 'Problem with your card please try again')

    @patch('payments.models.Customer.create')
    def test_valid_form(self, CreateMock):
        CreateMock.return_value = True
        request = self.factory.post('/cart/checkout/', {'stripeToken':'xxxxxxxxxx'})
        request.user = self.user
        request.session = {}

        resposne = views.checkout(request)
        self.assertEqual(response.status_code, 200)

    @patch('payments.models.Customer.create')
    def test_get_customer(self, CreateMock):
        CreateMock.return_value = Customer()
        customer = get_customer(self.user)
        self.assertEqual(Customer(), type(customer))






