import json

from django.test import TestCase
from django.test.client import RequestFactory

import mox

from model_mommy import mommy

from .views import WebhookView
from .forms import NewsletterSubscribeForm
from .models import Event, Subscriber


class EventModelTest(TestCase):
    def setUp(self):
        self.mock = mox.Mox()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_process_subscribe_existing_subscriber(self):
        sub = mommy.make('newsletter.Subscriber', email='api@mailchimp.com')

        data = {
            "type": "subscribe",
            "fired_at": "2009-03-26 21:35:57",
            "data[id]": "8a25ff1d98",
            "data[list_id]": "a6b5da1054",
            "data[email]": "api@mailchimp.com",
            "data[email_type]": "html",
            "data[merges][EMAIL]": "api@mailchimp.com",
            "data[merges][FNAME]": "MailChimp",
            "data[merges][LNAME]": "API",
            "data[merges][INTERESTS]": "Group1,Group2",
            "data[ip_opt]": "10.20.10.30",
            "data[ip_signup]": "10.20.10.30"}

        event = Event.objects.create(kind='subscribe', data=data)
        event.process()

        sub = Subscriber.objects.get(id=sub.id)

        self.assertEqual(sub.active, True)
        self.assertEqual(sub.first_name, 'MailChimp')
        self.assertEqual(sub.last_name, 'API')

    def test_process_subscribe_nonexisting_subscriber(self):
        data = {
            "type": "subscribe",
            "fired_at": "2009-03-26 21:35:57",
            "data[id]": "8a25ff1d98",
            "data[list_id]": "a6b5da1054",
            "data[email]": "api@mailchimp.com",
            "data[email_type]": "html",
            "data[merges][EMAIL]": "api@mailchimp.com",
            "data[merges][FNAME]": "MailChimp",
            "data[merges][LNAME]": "API",
            "data[merges][INTERESTS]": "Group1,Group2",
            "data[ip_opt]": "10.20.10.30",
            "data[ip_signup]": "10.20.10.30"}

        event = Event.objects.create(kind='subscribe', data=data)
        event.process()

        sub = Subscriber.objects.get()

        self.assertEqual(sub.active, True)
        self.assertEqual(sub.email, 'api@mailchimp.com')
        self.assertEqual(sub.first_name, 'MailChimp')
        self.assertEqual(sub.last_name, 'API')

    def test_process_unsubscribe(self):
        mommy.make(
            'newsletter.Subscriber', email='api+unsub@mailchimp.com',
            active=True)
        data = {
            "type": "unsubscribe",
            "fired_at": "2009-03-26 21:40:57",
            "data[action]": "unsub",
            "data[reason]": "manual",
            "data[id]": "8a25ff1d98",
            "data[list_id]": "a6b5da1054",
            "data[email]": "api+unsub@mailchimp.com",
            "data[email_type]": "html",
            "data[merges][EMAIL]": "api+unsub@mailchimp.com",
            "data[merges][FNAME]": "MailChimp",
            "data[merges][LNAME]": "API",
            "data[merges][INTERESTS]": "Group1,Group2",
            "data[ip_opt]": "10.20.10.30",
            "data[campaign_id]": "cb398d21d2",
            "data[reason]": "hard"
        }

        event = Event.objects.create(kind='unsubscribe', data=data)
        event.process()

        sub = Subscriber.objects.get(email='api+unsub@mailchimp.com')
        self.assertFalse(sub.active)

    def test_process_profile(self):
        mommy.make(
            'newsletter.Subscriber', email='api@mailchimp.com',
            first_name='Buddy', last_name='Lindsey', active=True)
        data = {
            "type": "profile",
            "fired_at": "2009-03-26 21:31:21",
            "data[id]": "8a25ff1d98",
            "data[list_id]": "a6b5da1054",
            "data[email]": "api@mailchimp.com",
            "data[email_type]": "html",
            "data[merges][EMAIL]": "api@mailchimp.com",
            "data[merges][FNAME]": "MailChimp",
            "data[merges][LNAME]": "API",
            "data[merges][INTERESTS]": "Group1,Group2",
            "data[ip_opt]": "10.20.10.30"
        }

        event = Event.objects.create(kind='profile', data=data)
        event.process()

        sub = Subscriber.objects.get()
        self.assertEqual(sub.first_name, 'MailChimp')
        self.assertEqual(sub.last_name, 'API')

    def test_update_email(self):
        mommy.make(
            'newsletter.Subscriber', email='api+old@mailchimp.com',
            first_name='Buddy', last_name='Lindsey', active=True)
        data = {
            "type": "upemail",
            "fired_at": "2009-03-26\ 22:15:09",
            "data[list_id]": "a6b5da1054",
            "data[new_id]": "51da8c3259",
            "data[new_email]": "api+new@mailchimp.com",
            "data[old_email]": "api+old@mailchimp.com"
        }

        event = Event.objects.create(kind='upemail', data=data)
        event.process()

        sub = Subscriber.objects.get()
        self.assertEqual(sub.email, 'api+new@mailchimp.com')


class WebhookViewTest(TestCase):
    def setUp(self):
        self.view = WebhookView()
        self.mock = mox.Mox()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_get(self):
        request = RequestFactory().get('/')
        response = self.view.get(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'data')

    def test_post(self):
        request = RequestFactory().post('/', data={'type': 'world'})

        self.mock.StubOutWithMock(Event, 'process')
        Event.process()

        self.mock.ReplayAll()
        response = self.view.post(request)
        self.mock.VerifyAll()

        self.assertEqual(response.status_code, 200)
