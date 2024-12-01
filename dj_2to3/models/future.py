"""The future model in this application."""

from __future__ import annotations

import json
import subprocess  # nosec B404
from typing import TYPE_CHECKING

from django.db import models
from django_extensions.db.models import TimeStampedModel
from versionfield import VersionField

if TYPE_CHECKING:
    from .fix import Fix


class Future(TimeStampedModel, models.Model):  # type: ignore[misc]
    """The future model."""

    version = VersionField(primary_key=True)

    def create_fixes(self) -> list[Fix] | None:
        """Get the fixes."""
        if not (python_executable := self.pythonexecutable_set.first()):
            return None

        from .fix import Fix  # pylint: disable=import-outside-toplevel

        categories = [
            "lib2to3_fix_names_stage1",
            "libfuturize_fix_names_stage1",
            "lib2to3_fix_names_stage2",
            "libfuturize_fix_names_stage2",
        ]

        fixes: list[Fix] = []
        for category in categories:
            result = subprocess.run(  # nosec B603
                [
                    python_executable.path,
                    "-c",
                    "import json; "
                    "from libfuturize import fixes; "
                    f"print(json.dumps(list(fixes.{category})))",
                ],
                capture_output=True,
                check=True,
                text=True,
            )
            for fix in json.loads(result.stdout.strip()):
                fix, _ = Fix.objects.get_or_create(
                    name=fix, category=category, future=self
                )
                fixes.append(fix)
        return fixes
