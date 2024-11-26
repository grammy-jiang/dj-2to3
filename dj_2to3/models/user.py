"""The User model in this application."""

from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):  # type: ignore[misc]
    """The customized User model."""
