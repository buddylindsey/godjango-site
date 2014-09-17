from django.conf import settings

import mailchimp


class MailchimpMixin(object):
    def newsletter_subscribe(self, first_name, last_name, email):
        newsletter_subscribe.delay(first_name, last_name, email)

