from .tasks import newsletter_subscribe


class MailchimpMixin(object):
    def newsletter_subscribe(self, first_name, last_name, email):
        newsletter_subscribe.delay(first_name, last_name, email)
