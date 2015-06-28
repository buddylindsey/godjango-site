import mailchimp

from django.conf import settings

from godjango.celery import app

from .models import Subscriber


@app.task
def newsletter_subscribe(first_name, last_name, email):
    if Subscriber.objects.filter(email=email).exists():
        return

    try:
        mc = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)

        name = {'FNAME': first_name, 'LNAME': last_name}
        email = {'email': email}
        mc.lists.subscribe(
            settings.MAILCHIMP_LIST_MAIN, email, merge_vars=name)
    except mailchimp.ListAlreadySubscribedError:
        pass
