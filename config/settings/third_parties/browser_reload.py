"""The settings of django-browser-reload extensions."""

from ..django import DEBUG, INSTALLED_APPS, MIDDLEWARE

if DEBUG:
    INSTALLED_APPS.append("django_browser_reload")
    MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")
