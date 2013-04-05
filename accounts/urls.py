from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.auth import logout as auth_logout

urlpatterns = patterns('',
    url(r'', include('social_auth.urls')),
    url(r'^dashboard/$', TemplateView.as_view(template_name="accounts/dashboard.html"), name="dashboard"),
    url(r'^login/$', RedirectView.as_view(url="/accounts/login/github")),
    url(r'^logout/$', auth_logout, name='logout'),

)
