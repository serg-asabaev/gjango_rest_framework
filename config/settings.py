import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


DEBUG = True if os.getenv("DEBUG") == "True" else False

SECRET_KEY = "django-insecure-2e)k^t7#&&2y^gmk4!@m9rtryb%&@8(6b3-yuwwbtpl5!4pm%c"

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "rest_framework_simplejwt",
    "drf_yasg",
    "corsheaders",
    "django_celery_beat",

    "users",
    "weblearn",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "project5",
        "USER": "postgres",
        "PASSWORD": "admin",
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Samara"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = "static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

# MAILERS = {
#     "default": {
#         "BACKEND": "django.core.mail.backends.smtp.EmailBackend"
#     },
# }

AUTH_USER_MODEL = "users.User"

# Настройки JWT-токенов
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# Настройки для рассылки по почте
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST=os.getenv("EMAIL_HOST")
EMAIL_PORT=os.getenv("EMAIL_PORT")
EMAIL_USE_TLS= True if os.getenv("EMAIL_USE_TLS") == "True" else False
EMAIL_USE_SSL= True if os.getenv("EMAIL_USE_SSL") == "True" else False
EMAIL_HOST_USER=os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD=os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL=os.getenv("DEFAULT_FROM_EMAIL")

#2it-G5b-5k2-UsV

# Настройки срока действия токенов
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

CORS_ALLOWED_ORIGINS = [
    "https://example.com",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8080",
]

STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")


CELERY_BROKER_URL = 'redis://localhost:6379' # Например, Redis, который по умолчанию работает на порту 6379
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BEAT_SCHEDULE = {
    'task-name': {
        'task': 'weblearn.tasks.check_user_last_login',
        'schedule': timedelta(minutes=1),
    },
}