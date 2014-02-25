from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, TemplateView

from djblog.sitemaps import ArticleSitemap

from home.sitemap import VideoSitemap
from episode.models import Video

admin.autodiscover()
sitemaps = {
    'videos': VideoSitemap(),
    'articles': ArticleSitemap()
}

urlpatterns = patterns(
    '',
    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Home
    url(r'^', include('home.urls')),

    # SEO
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
    url(
        r'^videositemap\.xml$', 'videositemap.views.video_sitemap',
        name='video_sitemap'),
    url(r'^robots\.txt$', include('robots.urls')),

    # Contact
    url(r'^feedback/', include('contact.urls')),

    # Accounts
    url('^accounts/', include('accounts.urls')),

    # Stripe
    url(r'^stripe/', include('payments.urls')),

    # Cart
    url(r'^cart/', include('godjango_cart.urls')),

    url(r'^blog/', include('djblog.urls', namespace='djblog')),

    # Subscription
    url(r'^subscribe/$',
        TemplateView.as_view(template_name="home/subscribe.html"),
        name="subscribe"),
    url(r'^subscribe/new/$', 'godjango_cart.views.subscribe',
        name="new_subscription"),

    # Episodes
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$',
        DetailView.as_view(
            model=Video, template_name="episode/video.html"), name="episode"),
)
