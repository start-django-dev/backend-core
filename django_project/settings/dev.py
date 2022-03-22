from django_project.secrets import get_secrets
from django_project.settings.base import *

DEBUG = True

SECRET_KEY = get_secrets("SECRET_KEY")

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

INTERNAL_IPS = [
    "localhost",
    "127.0.0.1",
]
