"""The project model in this application."""

import subprocess  # nosec B404
from pathlib import Path

import git

from django.db import models
from django_extensions.db.models import TimeStampedModel

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
            result = subprocess.run(  # nosec B603
                [
                    future.get_command_path(self.python_executable),
                    "--fix",
                    fix.name,
                    self.path,
                ],
                capture_output=True,
                check=True,
                text=True,
            )
            if (
                result.stderr.strip()
                == "RefactoringTool: No files need to be modified."
            ):
                continue
            project_fixes.append(
                ProjectFix.objects.create(project=self, fix=fix, diff=result.stdout)
            )
        return project_fixes
