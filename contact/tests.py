from django.core import mail
from django.test import TestCase
from django.core.urlresolvers import reverse

import mox
import arrow

from model_mommy import mommy

from .views import FeedbackView, ThankyouView

from contact.forms import FeedbackForm


class FeedbackViewTest(TestCase):
    def setUp(self):
        self.view = FeedbackView()
        self.mock = mox.Mox()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_attrs(self):
        self.assertEqual(self.view.template_name, 'contact/feedback.jinja')
        self.assertEqual(self.view.form_class, FeedbackForm)
        self.assertEqual(self.view.success_url, reverse('feedback_thankyou'))

    def test_form_valid(self):
        form = FeedbackForm()

        self.mock.StubOutWithMock(form, 'send_email')
        form.send_email()

        self.mock.ReplayAll()
        self.view.form_valid(form)
        self.mock.VerifyAll()


class ThankyouViewTest(TestCase):
    def setUp(self):
        self.view = ThankyouView()

    def test_attrs(self):
        self.assertEqual(self.view.template_name, 'contact/thankyou.jinja')

    def test_context_data(self):
        date = arrow.get(2013, 12, 12, 12, 12, 12)
        video1 = mommy.make('episode.Video', publish_date=date.datetime)
        video2 = mommy.make(
            'episode.Video', publish_date=date.replace(days=-1).datetime)
        context = self.view.get_context_data()
        self.assertSequenceEqual([video1, video2], context['videos'])


class FeedbackFormTest(TestCase):
    def test_send_email(self):
        form = FeedbackForm(
            data={'email': 'buddy@buddy.com', 'body': 'test email'})

        if form.is_valid():
            form.send_email()
        else:
            self.assertFail()

        self.assertEqual(len(mail.outbox), 1)
