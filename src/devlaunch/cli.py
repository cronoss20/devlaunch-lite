"""Command-line interface for DevLaunch Lite."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Annotated

import typer

from devlaunch import __version__
from devlaunch.generator import (
    InvalidProjectNameError,
    ProjectAlreadyExistsError,
    generate_project,
)
from devlaunch.models import ProjectConfig

app = typer.Typer(
    name="devlaunch",
    help="Generate production-ready backend services in seconds.",
    no_args_is_help=True,
)


@app.command()
def create(
    project_name: Annotated[
        str,
        typer.Argument(help="Lowercase project name, for example payments-api."),
    ],
    destination: Annotated[
        Path,
        typer.Option("--destination", "-d", help="Directory in which to create the project."),
    ] = Path("."),
    description: Annotated[
        str,
        typer.Option(help="Description used in generated metadata."),
    ] = "A production-ready FastAPI service.",
    force: Annotated[
        bool,
        typer.Option("--force", help="Replace files in an existing directory."),
    ] = False,
) -> None:
    """Create a FastAPI service with Docker, tests, linting and GitHub Actions."""
    config = ProjectConfig(
        project_name=project_name,
        destination=destination.expanduser().resolve(),
        description=description,
    )

    try:
        output_path = generate_project(config, force=force)
    except (InvalidProjectNameError, ProjectAlreadyExistsError) as exc:
        typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    typer.secho("Project generated successfully.", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"Location: {output_path}")
    typer.echo("Next steps:")
    typer.echo(f"  cd {project_name}")
    typer.echo("  python -m venv .venv")
    typer.echo("  pip install -e '.[dev]'")
    typer.echo("  pytest")


@app.command()
def doctor() -> None:
    """Check whether useful local development tools are available."""
    checks = {
        "Python 3.11+": sys.version_info >= (3, 11),
        "Git": shutil.which("git") is not None,
        "Docker (optional)": shutil.which("docker") is not None,
    }

    typer.echo("DevLaunch environment check")
    for label, available in checks.items():
        marker = "OK" if available else "NOT FOUND"
        color = typer.colors.GREEN if available else typer.colors.YELLOW
        typer.secho(f"  {label}: {marker}", fg=color)


@app.command()
def version() -> None:
    """Print the installed DevLaunch version."""
    typer.echo(__version__)


if __name__ == "__main__":
    app()
