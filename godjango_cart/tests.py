import views
import mox

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from mock import patch
from payments.models import Customer, Charge
from model_mommy import mommy

from .utils import get_customer, update_email
from .forms import CheckoutForm
from .tasks import send_receipts


class CheckoutViewTest(TestCase):
    def setUp(self):
        self.view = views.CheckoutView()
        self.mock = mox.Mox()

        self.factory = RequestFactory()
        self.request = self.factory.post('/')
        self.request.user = mommy.make('auth.User', email='test@example.com')
        self.request.session = {}
        self.request.POST = {'stripeToken': 'xxxxxxxxxx', 'plan': 'monthly'}

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_attrs(self):
        self.assertEqual(self.view.form_class, CheckoutForm)
        self.assertEqual(
            self.view.template_name, 'godjango_cart/checkout.jinja')
        self.assertEqual(self.view.success_url, reverse('order_confirmation'))

    def test_successful_purchase(self):
        pass

    def test_successful_purchase_with_coupon(self):
        pass


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


class RecieptTaskTest(TestCase):
    def setUp(self):
        self.mock = mox.Mox()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_send_reciepts(self):
        mommy.make('payments.Charge', paid=True, _quantity=3)

        self.mock.StubOutWithMock(Charge, 'send_receipt')
        Charge.send_receipt()
        Charge.send_receipt()
        Charge.send_receipt()

        self.mock.ReplayAll()
        send_receipts()
        self.mock.VerifyAll()
