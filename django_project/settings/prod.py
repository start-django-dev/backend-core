from django_project.secrets import get_secrets
from django_project.settings.base import *

DEBUG = False

SECRET_KEY = get_secrets("SECRET_KEY")

ALLOWED_HOSTS = [
    get_secrets("ALLOWED_HOSTS"),
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_secrets("POSTGRES_NAME"),
        "USER": get_secrets("POSTGRES_USER"),
        "PASSWORD": get_secrets("POSTGRES_PASSWORD"),
        "HOST": get_secrets("POSTGRES_HOST"),
        "PORT": get_secrets("POSTGRES_PORT"),
    },
}
