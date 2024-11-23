"""All settings."""

import django_stubs_ext

from .dj_2to3 import *
from .django import *
from .third_parties import *

django_stubs_ext.monkeypatch()
