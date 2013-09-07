from django.core import mail
from django.test import TestCase

from contact.forms import FeedbackForm


class FeedbackFormTest(TestCase):

    def test_send_email(self):
        form = FeedbackForm(
            data={'email': 'buddy@buddy.com', 'body': 'test email'})

        if form.is_valid():
            form.send_email()
        else:
            self.assertFail()

        self.assertEqual(len(mail.outbox), 1)
