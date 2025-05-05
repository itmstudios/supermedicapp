import os
import sentry_sdk

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-z3hq(y+)l5xr1t*ik*&m+nh49+6mee0*xj-k@a7#f&q*_2fh@5"

# sentry_sdk.init(
#     dsn=os.getenv("SENTRY_DSN"),
#     traces_sample_rate=1.0,
#     profiles_sample_rate=1.0,
# )

DEBUG = os.getenv("DEBUG") == "True"
if DEBUG:
    ALLOWED_HOSTS = ["*"]
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # ALLOWED_HOSTS = [
    #     "медик.online",
    #     "www.медик.online",
    #     "xn--d1abkig.online",
    #     "www.xn--d1abkig.online",
    # ]
    ALLOWED_HOSTS = ["*"]

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "supermedicapp",
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "supermediconline.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "supermediconline.wsgi.application"

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = False

if DEBUG:
    STATIC_URL = "supermediconline/supermedicapp/static/"
    STATIC_ROOT = "static/"

    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
else:
    STATIC_URL = "static/"
    STATIC_ROOT = "static/"

    MEDIA_URL = "static/media/"
    MEDIA_ROOT = "static/media/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING_LEVEL = "INFO"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": LOGGING_LEVEL,
            "class": "logging.FileHandler",
            "filename": "django.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
    },
}
