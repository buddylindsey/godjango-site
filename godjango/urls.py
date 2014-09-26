from django.contrib import admin
from django.conf.urls import patterns, include, url

from djblog.sitemaps import ArticleSitemap

from home.sitemap import VideoSitemap
from episode.views import BrowseView, CategoryView, ProFeedView, VideoView
from newsletter.views import WebhookView
from godjango_cart.views import (
    CheckoutView, FileView, SubscribeView, SubscriptionConfirmationView)

admin.autodiscover()
sitemaps = {
    'videos': VideoSitemap(),
    'articles': ArticleSitemap()
}

urlpatterns = patterns(
    '',
    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Analytics
    url(r'^analytics/', include('analytics.urls')),

    # Home
    url(r'^', include('home.urls')),

    url(r'^browse/$', BrowseView.as_view(), name="browse"),
    url(r'^category/(?P<slug>[-\w]+)/$', CategoryView.as_view(),
        name='category'),
    url(r'^favorite/add/$', 'favorite.views.toggle_favorite',
        name='favorite_toggle'),

    # SEO
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
    url(r'^videositemap\.xml$', 'videositemap.views.video_sitemap',
        name='video_sitemap'),
    url(r'^robots\.txt$', include('robots.urls')),

    # Contact
    url(r'^feedback/', include('contact.urls')),

    # Accounts
    url('^accounts/', include('accounts.urls')),

    # Stripe
    url(r'^stripe/', include('payments.urls')),

    url(r'^blog/', include('djblog.urls', namespace='djblog')),

    url(r'^search/', include('search.urls')),

    # Subscription
    url(r'^subscribe/$', SubscribeView.as_view(), name="subscribe"),
    url(r'^subscribe/new/$',
        CheckoutView.as_view(), name="new_subscription"),
    url(r'^subscribe/confirmation/$',
        SubscriptionConfirmationView.as_view(), name='order_confirmation'),

    url(r'^newsletter/', include('newsletter.urls')),

    # Download
    url(r'^file/$',
        FileView.as_view(), name="download"),

    # Episodes
    url(r'^feeds/pro/$', ProFeedView.as_view(), name='pro_feed'),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$',
        VideoView.as_view(), name="episode"),
)
