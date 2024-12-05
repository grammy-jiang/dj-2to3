"""The admin of the models about Python."""

import subprocess  # nosec B404
from typing import Optional

from packaging.version import Version

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

from ..models import Project, PythonExecutable


class ProjectInline(
    admin.TabularInline[Project, PythonExecutable]
):  # pylint: disable=unsubscriptable-object
    """The inline for the project model."""

    fields = ["path", "is_git_repository", "created", "modified"]
    model = Project
    readonly_fields = ["is_git_repository", "created", "modified"]

    @admin.display(boolean=True)
    def is_git_repository(self, obj: Project) -> bool:
        """Return whether the project is a git repository."""
        return obj.is_git_repository()

    def has_add_permission(
        self,
        request: HttpRequest,
        obj: Optional[Project] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the add permission."""
        return False

    def has_change_permission(
        self,
        request: HttpRequest,
        obj: Optional[Project] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the change permission."""
        return False

    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: Optional[Project] = None,  # pylint: disable=unused-argument
    ) -> bool:
        """Disable the delete permission."""
        return False


@admin.register(PythonExecutable)
class PythonExecutableAdmin(
    admin.ModelAdmin[PythonExecutable]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object
    """The PythonExecutable admin."""

    actions = [
        "install_dependencies",
    ]
    change_form_template = "dj_2to3/admin/change_form_python.html"
    fieldsets = (
        (None, {"fields": ("path", "version")}),
        (
            "Dependencies",
            {
                "fields": (
                    "future",
                    "modernize_installed",
                    "six_installed",
                    "bandit_installed",
                    "radon_installed",
                    "pylint_installed",
                )
            },
        ),
        ("Time", {"fields": ("created", "modified")}),
    )
    inlines = [ProjectInline]
    list_display = (
        "path",
        "version",
        "future__version",
        "modernize_installed",
        "six_installed",
        "bandit_installed",
        "radon_installed",
        "pylint_installed",
        "created",
        "modified",
    )
    readonly_fields = (
        "path",
        "version",
        "future",
        "created",
        "modified",
        "modernize_installed",
        "six_installed",
        "bandit_installed",
        "radon_installed",
        "pylint_installed",
    )

    def check_package_installed(self, obj: PythonExecutable, package: str) -> bool:
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

    @admin.display(boolean=True)
    def modernize_installed(self, obj: PythonExecutable) -> bool:
        """Check if the modernize package is installed."""
        return self.check_package_installed(obj, "modernize")

    @admin.display(boolean=True)
    def six_installed(self, obj: PythonExecutable) -> bool:
        """Check if the six package is installed."""
        return self.check_package_installed(obj, "six")

    @admin.display(boolean=True)
    def bandit_installed(self, obj: PythonExecutable) -> bool:
        """Check if the six package is installed."""
        return self.check_package_installed(obj, "bandit")

    @admin.display(boolean=True)
    def radon_installed(self, obj: PythonExecutable) -> bool:
        """Check if the six package is installed."""
        return self.check_package_installed(obj, "radon")

    @admin.display(boolean=True)
    def pylint_installed(self, obj: PythonExecutable) -> bool:
        """Check if the six package is installed."""
        return self.check_package_installed(obj, "pylint")

    @admin.action(description="Install dependencies")
    def install_dependencies(
        self, request: HttpRequest, queryset: QuerySet[PythonExecutable]
    ) -> None:
        """Install dependencies."""
        for python_executable in queryset:
            command = [
                python_executable.path,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "future",
                "modernize",
                "six",
            ]
            subprocess.run(  # nosec B603
                command, capture_output=True, check=True, text=True
            )

    def response_change(
        self, request: HttpRequest, obj: PythonExecutable
    ) -> HttpResponse:
        """Override the response_change method."""
        if "_install_dependencies" in request.POST:
            command = [
                obj.path,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "future",
                "modernize",
                "six",
            ]
            subprocess.run(  # nosec B603
                command, capture_output=True, check=True, text=True
            )
        return super().response_change(request, obj)
