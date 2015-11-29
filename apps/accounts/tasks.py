from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from godjango.celery import app

from .utils import generate_password


@app.task
def new_registration_email(user_id):
    user = User.objects.get(id=user_id)

    body = """
Welcome to GoDjango,

Thank you for registering for GoDjango. I hope you enjoy the videos that we
have to offer.

For a place to start visit the browse page: https://godjango.com/browse

Thank you,
Buddy Lindsey
"""

    email = EmailMessage(
        '[GoDjango] New Account', body, 'no-reply@godjango.com',
        [user.email])
    email.send()


@app.task
def password_changed_email(user_id):
    user = User.objects.get(id=user_id)

    body = "This is to inform you that you have changed your password."

    email = EmailMessage(
        '[GoDjango] Password Change', body, 'no-reply@godjango.com',
        [user.email])
    email.send()


@app.task
def password_reset_email(user_id):
    user = User.objects.get(id=user_id)

    password = generate_password()
    user.set_password(password)
    user.save()

    body = """
Sorry you are having issues with your account. Below is your username and
new password:

Username: {username}
Password: {password}

You can login here: https://godjango.com/accounts/login/
Change your password here: https://godjango.com/accounts/settings/
""".format(username=user.username, password=password)

    email = EmailMessage(
        '[GoDjango] Password Reset', body, 'no-reply@godjango.com',
        [user.email])
    email.send()
