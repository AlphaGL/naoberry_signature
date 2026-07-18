"""
Django settings for the Naoberry Signature site.

Local dev:  sqlite + local ./media uploads (no env vars needed beyond .env defaults)
Production: Postgres via DATABASE_URL + Cloudinary via CLOUDINARY_URL, on Vercel.
"""
import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-insecure-key-change-me")
DEBUG = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = ["127.0.0.1", "localhost", ".vercel.app"]
if os.environ.get("ALLOWED_HOST"):
    ALLOWED_HOSTS.append(os.environ["ALLOWED_HOST"])

CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app"]
if os.environ.get("SITE_DOMAIN"):
    CSRF_TRUSTED_ORIGINS.append(f"https://{os.environ['SITE_DOMAIN']}")
    ALLOWED_HOSTS.append(os.environ["SITE_DOMAIN"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cloudinary_storage",
    "cloudinary",
    "core",
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "naoberry.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "naoberry.wsgi.application"

# ---------------- Database ----------------
# Postgres in production (DATABASE_URL), sqlite locally.
if os.environ.get("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True

# ---------------- Static files ----------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles_build" / "static"

# ---------------- Media / Cloudinary ----------------
# With CLOUDINARY_URL set, every ImageField upload goes straight to Cloudinary.
# Without it (local dev), files land in ./media.
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

if os.environ.get("CLOUDINARY_URL"):
    STORAGES = {
        "default": {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"},
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
    }
else:
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------- Auth / dashboard ----------------
LOGIN_URL = "dashboard:login"
LOGIN_REDIRECT_URL = "dashboard:home"
LOGOUT_REDIRECT_URL = "dashboard:login"
