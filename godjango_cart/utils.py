from payments.models import Customer

def get_customer(user):
    try:
        return user.customer
    except:
        return Customer.create(user)


