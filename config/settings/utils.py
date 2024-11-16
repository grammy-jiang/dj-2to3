"""All utilities in settings."""

from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    DATABASE_URL=(str, "sqlite:///db.sqlite3"),
    SECRET_KEY=(
        str,
        "django-insecure-^q9jy6(lf&t75$y_y)b20kfbf!+5y2656q3xadfuqycpw!sw#!",
    ),
    TIME_ZONE=(str, "UTC"),
)
environ.Env.read_env(BASE_DIR / ".env")
