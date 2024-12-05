"""The project model in this application."""

import subprocess  # nosec B404
from pathlib import Path

import git

from django.db import models
from django_extensions.db.models import TimeStampedModel

from .fix import Fix
from .project_fix import ProjectFix
from .python import PythonExecutable


class Project(TimeStampedModel, models.Model):  # type: ignore[misc]
    """The project model."""

    path = models.FilePathField(
        path=str(Path.home() / "projects"),
        recursive=False,
        allow_files=False,
        allow_folders=True,
        primary_key=True,
    )

    python_executable = models.ForeignKey(
        PythonExecutable, blank=True, null=True, on_delete=models.CASCADE
    )

    def is_git_repository(self) -> bool:
        """Check if the project is a git repository."""
        try:
            git.Repo(self.path).git_dir
        except git.exc.InvalidGitRepositoryError:
            return False
        return True

    def analyze_future(self) -> list[ProjectFix]:
        """Analyze the project."""
        project_fixes: list[ProjectFix] = []
        if not self.python_executable:
            return project_fixes
        if not (future := self.python_executable.future):
            return project_fixes
        for fix in future.fix_set.all():
            if not (obj := self.analyze_future_fix(fix)):
                continue
            project_fixes.append(obj)
        return project_fixes

    def analyze_future_fix(self, fix: Fix) -> ProjectFix | None:
        """Analyze the future fix."""
        result = subprocess.run(  # nosec B603
            [
                fix.future.get_command_path(self.python_executable),
                "--fix",
                fix.name,
                self.path,
            ],
            capture_output=True,
            check=True,
            text=True,
        )
        if result.stderr.strip() == "RefactoringTool: No files need to be modified.":
            return None
        if not result.stdout.strip():
            return None
        obj, _ = ProjectFix.objects.update_or_create(
            defaults={"diff": result.stdout}, project=self, fix=fix
        )
        return obj
