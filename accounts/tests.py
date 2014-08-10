import json
import mailchimp

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

import mox

from .views import NewsletterSubscribeView
from .forms import NewsletterSubscribeForm


class DashboardTest(TestCase):
    def test_dashboard_index(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_favorites(self):
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_settings(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_billing(self):
        response = self.client.get(reverse('billing'))
        self.assertEqual(response.status_code, 302)


class NewsletterSubscribeViewTest(TestCase):
    def setUp(self):
        self.mock = mox.Mox()
        self.view = NewsletterSubscribeView()
        self.view.request = RequestFactory().post(
            '/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_form_valid(self):
        form = NewsletterSubscribeForm({'email': 'other@example.com'})
        form.is_valid()

        self.mock.StubOutWithMock(mailchimp.Lists, 'subscribe')
        mailchimp.Lists.subscribe('mainlistkey', 'other@example.com')

        self.mock.ReplayAll()
        response = self.view.form_valid(form)
        self.mock.VerifyAll()

        self.assertEqual(json.loads(response.content), {
            'success': ('Thank you for subscribing. Please confirm in the '
                        'email you that you have subscribed')})

    def test_already_subscribed_form_valid(self):
        form = NewsletterSubscribeForm({'email': 'other@example.com'})
        form.is_valid()

        self.mock.StubOutWithMock(mailchimp.Lists, 'subscribe')
        mailchimp.Lists.subscribe(
            'mainlistkey', 'other@example.com').AndRaise(
                mailchimp.ListAlreadySubscribedError)

        self.mock.ReplayAll()
        response = self.view.form_valid(form)
        self.mock.VerifyAll()

        self.assertEqual(json.loads(response.content), {
            'success': ('Thank you. You are already subscribed')})

    def test_errored_form_valid(self):
        form = NewsletterSubscribeForm({'email': 'other@example.com'})
        form.is_valid()

        self.mock.StubOutWithMock(mailchimp.Lists, 'subscribe')
        mailchimp.Lists.subscribe(
            'mainlistkey', 'other@example.com').AndRaise(mailchimp.Error)

        self.mock.ReplayAll()
        response = self.view.form_valid(form)
        self.mock.VerifyAll()

        self.assertEqual(json.loads(response.content), {
            'error': {'general':[('Something went horribly wrong. Please '
                                  'try again')]}})

    def test_form_invalid(self):
        form = NewsletterSubscribeForm({'email': 'wasup'})
        form.is_valid()
        response = self.view.form_invalid(form)

        self.assertEqual(json.loads(response.content), {'errors': form.errors})

