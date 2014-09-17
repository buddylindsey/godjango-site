import random
import string


def generate_password():
    return ''.join(
        [random.choice(
            string.ascii_letters + string.digits) for n in xrange(9)])
