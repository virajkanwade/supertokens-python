"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
from typing import List

from corsheaders.defaults import default_headers
from dotenv import load_dotenv

from supertokens_python import (
    InputAppInfo,
    SupertokensConfig,
    get_all_cors_headers,
    init,
)
from supertokens_python.recipe import (
    dashboard,
    emailverification,
    session,
    thirdpartyemailpassword,
)
from supertokens_python.recipe.thirdpartyemailpassword import (
    Apple,
    Discord,
    Github,
    Google,
    GoogleWorkspaces,
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Supertokens settings
load_dotenv()


def get_api_port():
    return "8000"


def get_website_port():
    return "3000"


def get_website():
    return "http://localhost:" + get_website_port()


init(
    supertokens_config=SupertokensConfig(connection_uri="https://try.supertokens.io"),
    app_info=InputAppInfo(
        app_name="Supertokens",
        api_domain="http://localhost:" + get_api_port(),
        origin=get_website(),
    ),
    framework="django",
    mode="wsgi",
    recipe_list=[
        session.init(),
        dashboard.init(),
        emailverification.init("REQUIRED"),
        thirdpartyemailpassword.init(
            providers=[
                Google(
                    is_default=True,
                    client_id=os.environ.get("GOOGLE_CLIENT_ID"),  # type: ignore
                    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),  # type: ignore
                ),
                Google(
                    client_id=os.environ.get("GOOGLE_CLIENT_ID_MOBILE"),  # type: ignore
                    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET_MOBILE"),  # type: ignore
                ),
                Github(
                    is_default=True,
                    client_id=os.environ.get("GITHUB_CLIENT_ID"),  # type: ignore
                    client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),  # type: ignore
                ),
                Github(
                    client_id=os.environ.get("GITHUB_CLIENT_ID_MOBILE"),  # type: ignore
                    client_secret=os.environ.get("GITHUB_CLIENT_SECRET_MOBILE"),  # type: ignore
                ),
                Apple(
                    is_default=True,
                    client_id=os.environ.get("APPLE_CLIENT_ID"),  # type: ignore
                    client_key_id=os.environ.get("APPLE_KEY_ID"),  # type: ignore
                    client_team_id=os.environ.get("APPLE_TEAM_ID"),  # type: ignore
                    client_private_key=os.environ.get("APPLE_PRIVATE_KEY"),  # type: ignore
                ),
                Apple(
                    client_id=os.environ.get("APPLE_CLIENT_ID_MOBILE"),  # type: ignore
                    client_key_id=os.environ.get("APPLE_KEY_ID"),  # type: ignore
                    client_team_id=os.environ.get("APPLE_TEAM_ID"),  # type: ignore
                    client_private_key=os.environ.get("APPLE_PRIVATE_KEY"),  # type: ignore
                ),
                GoogleWorkspaces(
                    is_default=True,
                    client_id=os.environ.get("GOOGLE_WORKSPACES_CLIENT_ID"),  # type: ignore
                    client_secret=os.environ.get("GOOGLE_WORKSPACES_CLIENT_SECRET"),  # type: ignore
                ),
                Discord(
                    is_default=True,
                    client_id=os.environ.get("DISCORD_CLIENT_ID"),  # type: ignore
                    client_secret=os.environ.get("DISCORD_CLIENT_SECRET"),  # type: ignore
                ),
            ]
        ),
    ],
    telemetry=False,
)

CORS_ORIGIN_WHITELIST = [get_website()]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [get_website()]
CORS_ALLOW_HEADERS: List[str] = (
    list(default_headers) + ["Content-Type"] + get_all_cors_headers()
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-7_3spq%4(**w@^yge4yuz0p=r%29vrol7qiydnvg5&i9@oyw&4"

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
    "corsheaders",
    "supertokens_python",
    "sampleapp",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "supertokens_python.framework.django.django_middleware.middleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [  # type: ignore
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

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
