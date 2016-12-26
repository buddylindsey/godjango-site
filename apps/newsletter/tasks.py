from django.conf import settings

from getdrip import GetDripAPI

from godjango.celery import app

from .models import Subscriber

MAIN_DRIP_CAMPAIGN = '2042936'


@app.task
def newsletter_subscribe(first_name, last_name, email, tags=None):
    if not tags:
        tags = ['celery-api']

    client = GetDripAPI(
        token=settings.DRIP_API_KEY, account_id=settings.DRIP_ACCOUNT_ID)

    payload = {
        'subscribers': [
            {
                'email': email,
                'tags': tags,
                'custom_fields': {
                    'first_name': first_name,
                    'last_name': last_name
                }
            }
        ]
    }

    client.subscribe_subscriber(MAIN_DRIP_CAMPAIGN, payload)
