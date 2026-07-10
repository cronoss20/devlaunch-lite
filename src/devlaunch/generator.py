"""Project generation service."""

from __future__ import annotations

import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from devlaunch.models import ProjectConfig

_PROJECT_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]{1,48}[a-z0-9]$")


class InvalidProjectNameError(ValueError):
    """Raised when a project name is not a valid lowercase slug."""


class ProjectAlreadyExistsError(FileExistsError):
    """Raised when the destination project directory already exists."""


def validate_project_name(project_name: str) -> None:
    """Validate a lowercase, hyphen-separated project name."""
    if not _PROJECT_NAME_PATTERN.fullmatch(project_name):
        raise InvalidProjectNameError(
            "Use 3-50 lowercase characters: letters, numbers and hyphens. "
            "The name must start with a letter and end with a letter or number."
        )


def generate_project(config: ProjectConfig, *, force: bool = False) -> Path:
    """Generate a FastAPI starter service and return its path."""
    validate_project_name(config.project_name)
    output_path = config.project_path

    if output_path.exists() and not force:
        raise ProjectAlreadyExistsError(
            f"'{output_path}' already exists. Use --force to replace generated files."
        )

    template_root = Path(__file__).parent / "templates" / "fastapi"
    environment = Environment(
        loader=FileSystemLoader(template_root),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
    )
    context = {
        "project_name": config.project_name,
        "package_name": config.package_name,
        "description": config.description,
    }

    for template_path in sorted(template_root.rglob("*")):
        if template_path.is_dir():
            continue

        relative_path = template_path.relative_to(template_root)
        target_relative = Path(str(relative_path).removesuffix(".j2"))
        target_path = output_path / target_relative
        target_path.parent.mkdir(parents=True, exist_ok=True)

        template = environment.get_template(relative_path.as_posix())
        target_path.write_text(template.render(**context), encoding="utf-8")

    return output_path
