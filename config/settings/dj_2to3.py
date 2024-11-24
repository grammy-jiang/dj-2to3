"""All settings of dj_2to3."""

from .django import INSTALLED_APPS

INSTALLED_APPS.append("dj_2to3")

AUTH_USER_MODEL = "dj_2to3.User"
