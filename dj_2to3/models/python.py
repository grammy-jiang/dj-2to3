"""The Python executable model in this application."""

from __future__ import annotations

import subprocess  # nosec B404
from pathlib import Path

from packaging.version import Version, parse

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_stubs_ext.db.models import TypedModelMeta

from .future import Future


def validate_python_executable(path: str) -> None:
    """Validate the Python executable."""
    path_ = Path(path)
    if not path_.is_file():
        raise ValueError(f"Invalid Python executable: {path_}.")
    if not path_.stat().st_mode & 0o111:
        raise ValueError(f"Python executable is not executable: {path_}.")


def check_package_installed(obj: PythonExecutable, package: str) -> bool:
    """Check if the given package is installed."""
    if obj.version < Version("3"):
        command = [
            obj.path,
            "-c",
            f"import imp; imp.find_module('{package}')",
        ]
        try:
            _ = subprocess.run(  # nosec B603
                command, capture_output=True, check=True, text=True
            )
        except subprocess.CalledProcessError:
            return False
        return True

    command = [
        obj.path,
        "-c",
        "import importlib.util; "
        f"print(importlib.util.find_spec('{package}') is not None)",
    ]
    result = subprocess.run(  # nosec B603
        command, capture_output=True, check=True, text=True
    )
    return result.stdout.strip() == "True"


class PythonExecutable(TimeStampedModel, models.Model):  # type: ignore[misc]
    """The Python executable model."""

    path = models.FilePathField(
        path=str(Path.home()),
        match=r"^python([23]\.[0-9]{,2}){,1}$",
        recursive=True,
        allow_files=True,
        allow_folders=False,
        validators=[validate_python_executable],
        primary_key=True,
    )
    future = models.ForeignKey(Future, on_delete=models.CASCADE, blank=True, null=True)

    class Meta(TypedModelMeta):
        """The Meta class for PythonExecutable."""

        verbose_name = "Python Executable"

    @property
    def version(self) -> Version:
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
        return parse((result.stdout.strip() or result.stderr.strip()).split(" ")[-1])

    def save(self, **kwargs):
        """Save the Python executable."""
        if check_package_installed(self, "future"):
            result = subprocess.run(  # nosec B603
                [
                    self.path,
                    "-c",
                    "import future; print(future.__version__)",
                ],
                capture_output=True,
                check=True,
                text=True,
            )
            future, _ = Future.objects.get_or_create(version=result.stdout.strip())
            self.future = future

        super().save(**kwargs)
