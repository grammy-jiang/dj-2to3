"""The User model in this application."""

from django_extensions.db.models import TimeStampedModel

from django.contrib.auth.models import AbstractUser


class User(AbstractUser, TimeStampedModel):  # type: ignore[misc]
    """The customized User model."""
