"""Domain models for project generation."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ProjectConfig:
    """Configuration required to generate a service."""

    project_name: str
    destination: Path
    description: str = "A production-ready FastAPI service."

    @property
    def package_name(self) -> str:
        """Return a valid Python package name derived from the project name."""
        return self.project_name.replace("-", "_")

    @property
    def project_path(self) -> Path:
        """Return the final path for the generated project."""
        return self.destination / self.project_name
