import arrow

from payments.models import Charge

from godjango.celery import app


@app.task
def send_receipts():
    start_date = arrow.utcnow().replace(days=-3).datetime
    charges = Charge.objects.filter(
        receipt_sent=False, paid=True, created_at__gte=start_date)

    for charge in charges:
        charge.send_receipt()
