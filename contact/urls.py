from django.conf.urls import *

from contact.views import FeedbackView

urlpatterns = patterns('',
    url('^', FeedbackView.as_view(), name='feedback'),
)
