from django_jinja import library

from payments.models import Customer, CurrentSubscription


def is_customer(user):
    customer = False
    paying = False
    try:
        if user.customer:
            customer = True
            if user.customer.has_active_subscription():
                paying = True
    except Customer.DoesNotExist:
        customer = False
    except AttributeError, e:
        if e.message == ("'AnonymousUser' object has no attribute 'customer'"):
            pass
        else:
            raise Exception(e)
    return (paying, customer)


def current_subscription(customer):
    try:
        return customer.current_subscription
    except CurrentSubscription.DoesNotExist:
        return False

library.global_function(is_customer)
library.global_function(current_subscription)
