"""The Python executable model in this application."""

import subprocess  # nosec B404
from pathlib import Path

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_stubs_ext.db.models import TypedModelMeta


def validate_python_executable(path: str) -> None:
    """Validate the Python executable."""
    path_ = Path(path)
    if not path_.is_file():
        raise ValueError(f"Invalid Python executable: {path_}.")
    if not path_.stat().st_mode & 0o111:
        raise ValueError(f"Python executable is not executable: {path_}.")


class PythonExecutable(TimeStampedModel, models.Model):  # type: ignore[misc]
    """The Python executable model."""

    path = models.FilePathField(
        path=str(Path.home()),
        match=r"^python[23]\.[0-9]{,2}$",
        recursive=True,
        allow_files=True,
        allow_folders=False,
        validators=[validate_python_executable],
        primary_key=True,
    )

    class Meta(TypedModelMeta):
        """The Meta class for PythonExecutable."""

        verbose_name = "Python Executable"

    @property
    def version(self) -> str:
        """Get the version of the Python executable."""
        try:
            result = subprocess.run(  # nosec B603
                [self.path, "--version"],
                capture_output=True,
                check=True,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            raise ValueError(
                f"Failed to get version of Python executable: {exc}."
            ) from exc
        except PermissionError as exc:
            raise ValueError(f"Permission denied: {exc}.") from exc
        return (result.stdout.strip() or result.stderr.strip()).split(" ")[-1]
