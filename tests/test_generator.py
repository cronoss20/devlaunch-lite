from pathlib import Path

import pytest

from devlaunch.generator import (
    InvalidProjectNameError,
    ProjectAlreadyExistsError,
    generate_project,
    validate_project_name,
)
from devlaunch.models import ProjectConfig


def test_generate_project_creates_expected_files(tmp_path: Path) -> None:
    config = ProjectConfig(
        project_name="payments-api",
        destination=tmp_path,
        description="Payments service.",
    )

    output_path = generate_project(config)

    assert output_path == tmp_path / "payments-api"
    assert (output_path / "app/main.py").exists()
    assert (output_path / "tests/test_health.py").exists()
    assert (output_path / ".github/workflows/ci.yml").exists()
    assert "Payments service." in (output_path / "README.md").read_text(encoding="utf-8")
    assert "payments-api" in (output_path / "app/main.py").read_text(encoding="utf-8")


def test_generate_project_rejects_existing_directory(tmp_path: Path) -> None:
    config = ProjectConfig(project_name="payments-api", destination=tmp_path)
    (tmp_path / "payments-api").mkdir()

    with pytest.raises(ProjectAlreadyExistsError):
        generate_project(config)


@pytest.mark.parametrize(
    "name",
    ["Payments", "ab", "-payments", "payments-", "payments_api", "payments api"],
)
def test_validate_project_name_rejects_invalid_names(name: str) -> None:
    with pytest.raises(InvalidProjectNameError):
        validate_project_name(name)
