from .base import *  # noqa
import os

DEBUG = True
ALLOW_ROBOTS = True
CORS_ORIGIN_ALLOW_ALL = True

if DEBUG_TOOLBAR:
    INTERNAL_IPS = ["127.0.0.1"]

    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

    DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(config("PROJECT_HOME_DIR", ""), "tmp/emails/")
os.makedirs(EMAIL_FILE_PATH, exist_ok=True)
