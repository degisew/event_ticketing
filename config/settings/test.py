from .base import *  # noqa F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


# ! Adding explicitly for CI purposes (to make it happy..huh)

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    "rest_access_policy",
    "drf_standardized_errors",
]

CUSTOM_APPS = [
    "apps.core.apps.CoreConfig",
    "apps.account.apps.AccountsConfig",
    "apps.event.apps.EventConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS
