"""All settings."""

import django_stubs_ext

from .django import *
from .third_parties import *

django_stubs_ext.monkeypatch()
