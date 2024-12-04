"""The future model in this application."""

from __future__ import annotations

import json
import subprocess  # nosec B404
from pathlib import Path
from typing import TYPE_CHECKING

from django.db import models
from django_extensions.db.models import TimeStampedModel
from versionfield import VersionField

if TYPE_CHECKING:
    from .fix import Fix
    from .python import PythonExecutable


class Future(TimeStampedModel, models.Model):  # type: ignore[misc]
    """The future model."""

    version = VersionField(primary_key=True)

    def load_fixes(self) -> list[Fix] | None:
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

    def get_command_path(self, python_executable: PythonExecutable) -> Path:
        """Get the command path."""
        if not (futurize := Path(python_executable.path).parent / "futurize").is_file():
            raise FileNotFoundError(
                f"futurize not found with the give python executable: [{python_executable.path}]",
            )
        return futurize
