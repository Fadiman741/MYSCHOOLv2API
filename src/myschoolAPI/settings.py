import cloudinary
import cloudinary.uploader
import cloudinary.api
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--(ml@e3ay(g$epmuve$mauohj9-77wn=a%#-&7+6xjw06xe7&="

# OPENAI_API_KEY = 'sk-proj-2ujCjOrXo6IfcqwZlDBYT3BlbkFJlB97EKOoHVhCfUPRlUYe'

# SECURITY WARNING: don't run with debug turned on in production!
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
    "channels",
    "users",
    "corsheaders",
    "rest_framework.authtoken",
    'cloudinary',
    'cloudinary_storage',
    # 'django_cloudinary_storage'
    
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

ROOT_URLCONF = "myschoolAPI.urls"

CORS_ORIGIN_ALLOW_ALL = True

AUTH_USER_MODEL = "users.User"

CORS_ORIGIN_WHITELIST = ("http://localhost:8000",)

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

WSGI_APPLICATION = "myschoolAPI.wsgi.application"

# Use Channels as the backend for Django's ASGI interface
# ASGI_APPLICATION = "notification_project.routing.application"
ASGI_APPLICATION = 'myschoolAPI.asgi.application'

# Configure Channels to use the Channel Layer as the default backend
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         # "NAME": "myschooldatabse",
#         "NAME": "myschool",
#         "USER": "root",
#         "PASSWORD": "",
#         "HOST": "localhost",
#         "PORT": "3306",
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'myschool',
#         'USER': 'postgres',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '5432',  # Default PostgreSQL port
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
#     'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
#     'SLIDING_TOKEN_LIFETIME': timedelta(days=7),
#     'SLIDING_TOKEN_REFRESH_LIFETIME_GRACE_PERIOD': timedelta(days=2),
#     'SLIDING_TOKEN_REFRESH_GAP': timedelta(days=1),
#     'SLIDING_TOKEN_LIFETIME_GRACE_PERIOD': timedelta(days=2),
#     'SLIDING_TOKEN_REFRESH_EXPIRATION': timedelta(days=30),
# }

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        "rest_framework.authentication.TokenAuthentication",
        # 'knox.auth.TokenAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}
# CLOUDINARY_URL = "cloudinary://539549775893276:4gCHTXIzejMtEiWJobfcaKKM8J4@dzpr6z2z5"

CLOUDINARY_STORAGE = {
    "cloud_name": "dzpr6z2z5",
    "api_key": "539549775893276",
    "api_secret": "4gCHTXIzejMtEiWJobfcaKKM8J4",
}
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
