"""
Django settings for portfolio project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

from .version import get_version

# Load environment variables from .env (useful locally)
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------
# Core settings
# -------------------------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

# -------------------------------------------------------------------
# Security
# -------------------------------------------------------------------

SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", 31536000))  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = (
    os.getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", "True") == "True"
)
SECURE_HSTS_PRELOAD = os.getenv("SECURE_HSTS_PRELOAD", "True") == "True"
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False") == "True"

SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "True") == "True"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "True") == "True"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# -------------------------------------------------------------------
# Applications
# -------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "gallery",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "portfolio.urls"

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
                "portfolio.context_processors.app_version",
            ],
        },
    },
]

WSGI_APPLICATION = "portfolio.wsgi.application"

# -------------------------------------------------------------------
# Database
# -------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("DB_PATH", BASE_DIR / "db.sqlite3"),
    }
}

analytics_db_password = os.getenv("ANALYTICS_DB_PASSWORD") or os.getenv(
    "PORTFOLIO_DB_PASSWORD"
)

if os.getenv("ANALYTICS_DB_NAME") and analytics_db_password:
    DATABASES["analytics"] = {
        "ENGINE": os.getenv(
            "ANALYTICS_DB_ENGINE", "django.db.backends.postgresql"
        ),
        "NAME": os.getenv("ANALYTICS_DB_NAME"),
        "USER": os.getenv("ANALYTICS_DB_USER", "portfolio"),
        "PASSWORD": analytics_db_password,
        "HOST": os.getenv(
            "ANALYTICS_DB_HOST", "postgres.postgresql.svc.cluster.local"
        ),
        "PORT": os.getenv("ANALYTICS_DB_PORT", "5432"),
    }

# -------------------------------------------------------------------
# Password validation
# -------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"  # noqa: E501
    },
]

# -------------------------------------------------------------------
# Internationalization
# -------------------------------------------------------------------

LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "en-us")
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# Static & Media
# -------------------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = os.getenv("STATIC_ROOT", BASE_DIR / "staticfiles")
STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise storage backend (compressed + hashed filenames)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.getenv("MEDIA_ROOT", BASE_DIR / "media")

# -------------------------------------------------------------------
# Misc
# -------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
APP_VERSION = get_version()
