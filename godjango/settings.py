# Django settings for godjango project.
import os
import sys

DJANGO_ENV = os.environ.get('DJANGO_ENV', '')

if(DJANGO_ENV == "production"):
    DEBUG = False
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DATABASE_NAME', ''),
            'USER': os.environ.get('DATABASE_USER', ''),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
            'HOST': os.environ.get('DATABASE_HOST', ''),
            'PORT': os.environ.get('DATABASE_PORT', ''),
        }
    }
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    DEBUG = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

ADMINS = (
    ('Buddy Lindsey', 'buddy@buddylindsey.com'),
)

MANAGERS = ADMINS


SITE_ID = 1

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True


if(DJANGO_ENV == "production"):
    MEDIA_ROOT = '/var/www/assets/godjango/'
else:
    MEDIA_ROOT = "{}/media/".format(os.path.join(BASE_DIR, 'media'))
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static_final')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_COMPILERS = (
    'pipeline.compilers.coffee.CoffeeScriptCompiler',
    'pipeline.compilers.stylus.StylusCompiler',
)

SECRET_KEY = 'l$f@dvrc!!+afw$-a-w(^vv889^%5%cl%+1)h+0!8@i0eq=sv2'

TEMPLATE_LOADERS = (
    'django_jinja.loaders.FileSystemLoader',
    'django_jinja.loaders.AppLoader',
)

DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.jinja'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages"
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'godjango.urls'

WSGI_APPLICATION = 'godjango.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'home',
    'episode',
    'social.apps.django_app.default',
    'accounts',
    'favorite',
    'payments',
    'cart',
    'godjango_cart',
    'contact',
    'south',
    'django.contrib.sitemaps',
    'robots',
    'crispy_forms',
    'videositemap',
    'django_extensions',
    'djblog',
    'search',
    'djcelery',
    'pipeline',
    'django_jinja',
    'django_jinja.contrib._pipeline',
    'newsletter',
    'analytics',
    'rest_framework',
    'rest_framework.authtoken',
    'podcasts',
    'raven.contrib.django.raven_compat',
)

# Django Social Auth settings
AUTHENTICATION_BACKENDS = (
    'social.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_ENABLED_BACKENDS = ('github',)
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

SOCIAL_AUTH_GITHUB_KEY = os.environ.get('GITHUB_APP_ID', '')
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get('GITHUB_API_SECRET', '')

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/dashboard/'
LOGIN_ERROR_URL = '/accounts/login-error/'

STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')

EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

EMAIL_USE_TLS = True

PAYMENTS_INVOICE_FROM_EMAIL = "buddy@buddylindsey.com"
PAYMENTS_PLANS = {
    "monthly": {
        "stripe_plan_id": "14-pro-monthly",
        "name": "Pro Monthly 14",
        "description": "The monthly subscription plan to GoDjango",
        "price": 1495,
        "currency": "usd",
        "interval": "month"
    },
    "yearly": {
        "stripe_plan_id": "14-pro-yearly",
        "name": "Pro Yearly 14",
        "description": "The yearly subscription plan to GoDjango",
        "price": 14950,
        "currency": "usd",
        "interval": "yearly"
    },
    "monthly-first": {
        "stripe_plan_id": "pro",
        "name": "Pro - Monthly",
        "description": "The monthly subscription plan to GoDjango",
        "price": 9,
        "currency": "usd",
        "interval": "month"
    },
    "yearly-first": {
        "stripe_plan_id": "pro-yearly",
        "name": "Pro - Yearly",
        "description": "The yearly subscription plan to GoDjango",
        "price": 90,
        "currency": "usd",
        "interval": "yearly"
    }
}

CRISPY_TEMPLATE_PACK = 'bootstrap'

BROKER_URL = 'redis://127.0.0.1:6379/1'
BROKER_TRANSPORT = 'redis'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'

PIPELINE_JS = {
    'main': {
        'source_filenames': (
            'coffee/app.coffee',
        ),
        'output_filename': 'js/main.min.js'
    },
    'vendor': {
        'source_filenames': (
            'js/django-csrf.js',
            'js/underscore-min.js',
            'js/backbone-min.js',
        ),
        'output_filename': 'js/vendor.js'
    }
}

PIPELINE_CSS = {
    'main': {
        'source_filenames': (
            'stylus/main.styl',
            'stylus/properties.styl'
        ),
        'output_filename': 'css/main.min.css'
    },
    'vendor': {
        'source_filenames': (
            'css/pygments.css',
        ),
        'output_filename': 'css/vendor.min.css'
    }
}

MAILCHIMP_API_KEY = ''
MAILCHIMP_LIST_MAIN = ''

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
    }
}

try:
    from local_settings import *
except ImportError:
    pass
