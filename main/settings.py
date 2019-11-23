"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import datetime
import logging.config
import os
from pathlib import Path

from dotenv import load_dotenv
from marshmallow import fields
from marshmallow import Schema
from marshmallow import validates_schema
from marshmallow import ValidationError

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env_path = Path("./main") / ".env.default"
load_dotenv(env_path)

env_path = Path("./main") / ".env"
load_dotenv(env_path, override=True)


class EnvVarsValidator(Schema):
    PROJECT_NAME = fields.String(missing="Servicing")

    SERVICING_AUTH_SECRET_KEY = fields.String(missing=None)
    SERVICING_AUTH_ENABLE_SESSION = fields.Boolean(missing=False)
    SERVICING_AUTH_ENABLE_PASSWORD_VALIDATORS = fields.Boolean(missing=False)

    SERVICING_ENV = fields.String(missing="local")
    SERVICING_DEBUG = fields.Boolean(missing=True)
    SERVICING_CORS_ORIGIN_ALLOW_ALL = fields.Boolean(missing=True)
    SERVICING_STATIC_ROOT = fields.String(missing="/var/www/static/")
    SERVICING_MEDIA_ROOT = fields.String(missing="/var/www/media/")
    SERVICING_WEB_APP_URL = fields.String(missing="127.0.0.1:4000")
    SERVICING_TIMEZONE = fields.String(missing="UTC")

    SERVICING_DB_HOST = fields.String(missing="127.0.0.1")
    SERVICING_DB_PORT = fields.String(missing="5432")
    SERVICING_DB_NAME = fields.String(missing="shop_db")
    SERVICING_DB_USER = fields.String(missing="shop_user")
    SERVICING_DB_PASSWORD = fields.String(missing="shop_password")

    SERVICING_CLOUD_STORAGE_ENABLED = fields.Boolean(missing=False)
    SERVICING_AWS_S3_BUCKET_NAME = fields.String(missing=None)
    SERVICING_AWS_S3_REGION_NAME = fields.String(missing=None)
    SERVICING_AWS_S3_ENDPOINT_URL = fields.String(missing=None)
    SERVICING_AWS_ACCESS_KEY_ID = fields.String(missing=None)
    SERVICING_AWS_SECRET_ACCESS_KEY = fields.String(missing=None)

    SERVICING_SMTP_HOST = fields.String(missing=None)
    SERVICING_SMTP_PORT = fields.String(missing="25")
    SERVICING_SMTP_USER = fields.String(missing=None)
    SERVICING_SMTP_PASSWORD = fields.String(missing=None)
    SERVICING_SMTP_FROM_EMAIL = fields.String(missing=None)

    SERVICING_CELERY_BROKER_URL = fields.String(missing="redis://127.0.0.1:6379")
    SERVICING_CELERY_RESULT_URL = fields.String(missing="redis://127.0.0.1:6379")

    @validates_schema
    def validate(self, data):
        errors = []

        if data["SERVICING_CLOUD_STORAGE_ENABLED"]:
            if data["SERVICING_AWS_S3_BUCKET_NAME"] is None:
                errors.append("SERVICING_AWS_S3_BUCKET_NAME")

            if data["SERVICING_AWS_S3_REGION_NAME"] is None:
                errors.append("SERVICING_AWS_S3_REGION_NAME")

            if data["SERVICING_AWS_S3_ENDPOINT_URL"] is None:
                errors.append("SERVICING_AWS_S3_ENDPOINT_URL")

            if data["SERVICING_AWS_ACCESS_KEY_ID"] is None:
                errors.append("SERVICING_AWS_ACCESS_KEY_ID")

            if data["SERVICING_AWS_SECRET_ACCESS_KEY"] is None:
                errors.append("SERVICING_AWS_SECRET_ACCESS_KEY")

        if errors:
            raise ValidationError("Invalid field configuration.", field_names=errors)


ENV_VARS = EnvVarsValidator().load(os.environ)
PROJECT_NAME = ENV_VARS["PROJECT_NAME"]

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = ENV_VARS["SERVICING_CORS_ORIGIN_ALLOW_ALL"]
SERVICING_ENV = ENV_VARS["SERVICING_ENV"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV_VARS["SERVICING_DEBUG"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV_VARS["SERVICING_AUTH_SECRET_KEY"]

# Application definition
CORE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

CONTRIB_APPS = [
    "allauth",
    "allauth.account",
    "rest_framework",
    "rest_framework_swagger",
    "rest_framework_gis",
    "rest_framework.authtoken",
    "rest_auth",
    "django_filters",
    "corsheaders",
    "djcelery_email",
]

CUSTOM_APPS = ["apps.authentication", "apps.common", "apps.shop"]

INSTALLED_APPS = CORE_APPS + CONTRIB_APPS + CUSTOM_APPS


# Middleware definition
CORE_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

CUSTOM_MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware"]

CONTRIB_MIDDLEWARE = []

MIDDLEWARE = CORE_MIDDLEWARE + CONTRIB_MIDDLEWARE + CUSTOM_MIDDLEWARE

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["apps/authentication/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "main.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": ENV_VARS["SERVICING_DB_HOST"],
        "PORT": ENV_VARS["SERVICING_DB_PORT"],
        "NAME": ENV_VARS["SERVICING_DB_NAME"],
        "USER": ENV_VARS["SERVICING_DB_USER"],
        "PASSWORD": ENV_VARS["SERVICING_DB_PASSWORD"],
    }
}


AUTH_PASSWORD_VALIDATORS = []
ENABLE_PASSWORD_VALIDATORS = ENV_VARS["SERVICING_AUTH_ENABLE_PASSWORD_VALIDATORS"]
if ENABLE_PASSWORD_VALIDATORS:
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]


AUTH_USER_MODEL = "shop.Buyer"
AUTH_ADD_URLS = True
ACCOUNT_ADAPTER = "apps.authentication.adapters.AccountAdapter"

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"

AUTHENTICATION_BACKENDS = [
    "allauth.account.auth_backends.AuthenticationBackend",
]


ENABLE_SESSIONS = ENV_VARS["SERVICING_AUTH_ENABLE_SESSION"]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "apps.authentication.backends.CustomJSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    )
    if ENABLE_SESSIONS
    else ("apps.authentication.backends.CustomJSONWebTokenAuthentication",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "COERCE_DECIMAL_TO_STRING": False,
}


REST_USE_JWT = True
JWT_AUTH = {
    "JWT_EXPIRATION_DELTA": datetime.timedelta(hours=2),
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(hours=8),
    "JWT_ALLOW_REFRESH": True,
    "JWT_PAYLOAD_HANDLER": "apps.authentication.utils.jwt_payload_handler",
    "JWT_ENCODE_HANDLER": "rest_framework_jwt.utils.jwt_encode_handler",
}

USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = "en-us"
TIME_ZONE = ENV_VARS["SERVICING_TIMEZONE"]

SITE_ID = 1

STATIC_URL = "/static/"
STATIC_ROOT = ENV_VARS["SERVICING_STATIC_ROOT"]
MEDIA_URL = "/media/"
MEDIA_ROOT = ENV_VARS["SERVICING_MEDIA_ROOT"]

# Configure email
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = ENV_VARS["SERVICING_SMTP_HOST"]
EMAIL_USE_TLS = True
EMAIL_PORT = ENV_VARS["SERVICING_SMTP_PORT"]
EMAIL_HOST_USER = ENV_VARS["SERVICING_SMTP_USER"]
EMAIL_HOST_PASSWORD = ENV_VARS["SERVICING_SMTP_PASSWORD"]
DEFAULT_FROM_EMAIL = ENV_VARS["SERVICING_SMTP_FROM_EMAIL"]

# Configure web app urls
WEB_APP_BASE_URL = ENV_VARS["SERVICING_WEB_APP_URL"]
WEB_APP_ROUTES = {
    "account_activation": WEB_APP_BASE_URL + "/auth/login/{key}"
}

# Configure aws
if ENV_VARS["SERVICING_CLOUD_STORAGE_ENABLED"]:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    AWS_ACCESS_KEY_ID = ENV_VARS["SERVICING_AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = ENV_VARS["SERVICING_AWS_SECRET_ACCESS_KEY"]
    AWS_STORAGE_BUCKET_NAME = ENV_VARS["SERVICING_AWS_S3_BUCKET_NAME"]
    AWS_S3_REGION_NAME = ENV_VARS["SERVICING_AWS_S3_REGION_NAME"]
    AWS_S3_ENDPOINT_URL = ENV_VARS["SERVICING_AWS_S3_ENDPOINT_URL"]


# Configure logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        }
    },
    "loggers": {
        "django": {"handlers": ["console"]},
        "django.server": {"handlers": ["console"], "propagate": False},
        "apps": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": True,
        },
        "main": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": True,
        },
    },
}

logging.config.dictConfig(LOGGING)

# Print log configuration
logger.info("The server is starting with the following configuration:")
for key, value in sorted(ENV_VARS.items()):
    logger.info(f"{key} ->  {value}")


# Celery configuration
CELERY_BROKER_URL = ENV_VARS["SERVICING_CELERY_BROKER_URL"]
CELERY_RESULT_BACKEND = ENV_VARS["SERVICING_CELERY_RESULT_URL"]
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = ENV_VARS["SERVICING_TIMEZONE"]

# Swagger configuration
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": ENV_VARS["SERVICING_AUTH_ENABLE_SESSION"],
    "SECURITY_DEFINITIONS": {
        "api_key": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}
