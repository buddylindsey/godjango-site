from payments.models import Customer


def get_customer(user):
    try:
        return user.customer
    except:
        return Customer.create(user)


def update_email(user, email):
    if user.email == email:
        return email
    else:
        user.email = email
        user.save(update_fields=['email'])

    return user.email
