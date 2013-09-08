from django.conf.urls import url, patterns

from contact.views import FeedbackView, ThankyouView

urlpatterns = patterns(
    '',
    url('^thankyou/$', ThankyouView.as_view(), name='feedback_thankyou'),
    url('^$', FeedbackView.as_view(), name='feedback'),
)
