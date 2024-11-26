"""The settings of django-debug-toolbar extensions."""

from ..django import DEBUG, INSTALLED_APPS, INTERNAL_IPS, MIDDLEWARE

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

    INTERNAL_IPS.append("127.0.0.1")
