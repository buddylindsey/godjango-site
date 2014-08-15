from payments.models import Customer


class CustomerMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CustomerMixin, self).get_context_data(**kwargs)
        context['is_customer'] = self.is_customer
        return context

    def is_customer(self, user):
        try:
            if user.customer or user.customer.has_active_subscription():
                return True
        except Customer.DoesNotExist:
            print 'exception thrown'
            return False
        except AttributeError, e:
            if e.message == ("'AnonymousUser' object has no attribute "
                             "'customer'"):
                return False
            else:
                raise Exception(e)
        return False

