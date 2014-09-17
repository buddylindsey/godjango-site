from django.contrib import messages
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth.forms import (
    AuthenticationForm, SetPasswordForm, PasswordChangeForm)

import mox

from model_mommy import mommy

import accounts.views as views
import accounts.tasks as tasks
from .views import (
    AccountRegistrationView, BillingView, DashboardView, LoginView,
    PasswordRecoveryView, SettingsView, UpdateBillingView)
from .forms import CardForm, PasswordRecoveryForm, UserCreateForm
from .tasks import (
    new_registration_email, password_changed_email, password_reset_email)


class LoginViewTest(TestCase):
    def setUp(self):
        self.mock = mox.Mox()
        self.view = LoginView()
        self.view.request = RequestFactory().get('/')

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_attrs(self):
        self.assertEqual(self.view.template_name, 'accounts/login.jinja')
        self.assertEqual(self.view.form_class, AuthenticationForm)
        self.assertEqual(self.view.success_url, '/accounts/dashboard/')

    def test_form_valid(self):
        form = AuthenticationForm()
        self.mock.StubOutWithMock(form, 'get_user')
        self.mock.StubOutWithMock(views, 'auth_login')
        form.get_user().AndReturn('user')
        views.auth_login(self.view.request, 'user')

        self.mock.ReplayAll()
        self.view.form_valid(form)
        self.mock.VerifyAll()

    def test_form_invalid(self):
        form = AuthenticationForm()
        self.mock.StubOutWithMock(views.messages, 'add_message')
        views.messages.add_message(
            self.view.request, views.messages.ERROR,
            'Invalid Username or Password. Please Try Again')

        self.mock.ReplayAll()
        self.view.form_invalid(form)
        self.mock.VerifyAll()


class AccountRegistrationViewTest(TestCase):
    def setUp(self):
        self.mock = mox.Mox()
        self.view = AccountRegistrationView()
        self.view.request = RequestFactory().post('/')

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_attrs(self):
        self.assertEqual(self.view.template_name, 'accounts/register.jinja')
        self.assertEqual(self.view.form_class, UserCreateForm)
        self.assertEqual(self.view.success_url, '/accounts/dashboard/')

    def test_form_valid(self):
        form = UserCreateForm()
        form.cleaned_data = {'password1': '123', 'subscribe': False}
        user = mommy.make('auth.User')
        self.mock.StubOutWithMock(form, 'save')
        self.mock.StubOutWithMock(views, 'authenticate')
        self.mock.StubOutWithMock(views, 'auth_login')
        self.mock.StubOutWithMock(self.view, 'newsletter_subscribe')
        self.mock.StubOutWithMock(self.view, 'get_success_url')
        self.mock.StubOutWithMock(new_registration_email, 'delay')
        form.save().AndReturn(user)
        views.authenticate(
            username=user.username, password='123').AndReturn(user)
        views.auth_login(self.view.request, user)
        new_registration_email.delay(user.id)
        self.view.get_success_url().AndReturn('/')

        self.mock.ReplayAll()
        self.view.form_valid(form)
        self.mock.VerifyAll()

    def test_form_valid_subscribe(self):
        form = UserCreateForm()
        form.cleaned_data = {
            'password1': '123', 'subscribe': True, 'email': 'email'}
        user = mommy.make('auth.User')
        self.mock.StubOutWithMock(form, 'save')
        self.mock.StubOutWithMock(views, 'authenticate')
        self.mock.StubOutWithMock(views, 'auth_login')
        self.mock.StubOutWithMock(new_registration_email, 'delay')
        self.mock.StubOutWithMock(self.view, 'newsletter_subscribe')
        self.mock.StubOutWithMock(self.view, 'get_success_url')
        form.save().AndReturn(user)
        views.authenticate(
            username=user.username, password='123').AndReturn(user)
        views.auth_login(self.view.request, user)
        new_registration_email.delay(user.id)
        self.view.newsletter_subscribe('', '', 'email')
        self.view.get_success_url().AndReturn('/')

        self.mock.ReplayAll()
        self.view.form_valid(form)
        self.mock.VerifyAll()


class PasswordRecoveryViewTest(TestCase):
    def setUp(self):
        self.mock = mox.Mox()
        self.view = PasswordRecoveryView()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_attrs(self):
        self.assertEqual(
            self.view.template_name, 'accounts/password_recovery.jinja')
        self.assertEqual(self.view.form_class, PasswordRecoveryForm)
        self.assertEqual(
            self.view.success_url, reverse('password_recovery_confirmation'))

    def test_form_valid(self):
        user = mommy.make('auth.User', email='test@example.com')
        form = PasswordRecoveryForm()
        form.cleaned_data = {'email': 'test@example.com'}

        self.mock.StubOutWithMock(password_reset_email, 'delay')
        password_reset_email.delay(user.id)

        self.mock.ReplayAll()
        self.view.form_valid(form)
        self.mock.VerifyAll()


class BillingViewTest(TestCase):
    def setUp(self):
        self.view = BillingView()

    def test_attrs(self):
        self.assertEqual(self.view.template_name, 'accounts/billing.jinja')


class DashboardViewTest(TestCase):
    def setUp(self):
        self.view = DashboardView()

    def test_attrs(self):
        self.assertEqual(self.view.template_name, 'accounts/dashboard.jinja')


class SettingsViewTest(TestCase):
    def setUp(self):
        self.mock = mox.Mox()
        self.view = SettingsView()
        self.view.request = RequestFactory().post('/')
        self.view.request.user = mommy.make('auth.User')

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_attrs(self):
        self.assertEqual(self.view.template_name, 'accounts/settings.jinja')
        self.assertEqual(self.view.success_url, '/accounts/settings/')

    def test_form_valid(self):
        form = PasswordChangeForm(self.view.request.user)
        self.mock.StubOutWithMock(form, 'save')
        self.mock.StubOutWithMock(messages, 'add_message')
        self.mock.StubOutWithMock(password_changed_email, 'delay')
        form.save()
        messages.add_message(
            self.view.request, messages.SUCCESS,
            'Your password has been changed')
        password_changed_email.delay(self.view.request.user.id)

        self.mock.ReplayAll()
        self.view.form_valid(form)
        self.mock.VerifyAll()


class UpdateBillingViewTest(TestCase):
    def setUp(self):
        self.view = UpdateBillingView()

    def test_attrs(self):
        self.assertEqual(self.view.form_class, CardForm)
        self.assertEqual(self.view.template_name, 'accounts/update_card.jinja')
        self.assertEqual(self.view.success_url, reverse('billing'))


class PasswordResetEmailTest(TestCase):
    def setUp(self):
        self.mock = mox.Mox()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_password_reset_email(self):
        user = mommy.make(
            'auth.User', email='test@example.com', username='the_user')

        self.mock.StubOutWithMock(tasks, 'generate_password')
        self.mock.StubOutWithMock(User, 'set_password')
        tasks.generate_password().AndReturn('pass')
        User.set_password('pass')

        self.mock.ReplayAll()
        password_reset_email(user.id)
        self.mock.VerifyAll()

        self.assertEqual(1, len(mail.outbox))
        self.assertIn('Username: the_user', mail.outbox[0].body)
        self.assertIn('Password: pass', mail.outbox[0].body)
