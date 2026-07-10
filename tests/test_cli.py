from pathlib import Path

from typer.testing import CliRunner

from devlaunch.cli import app

runner = CliRunner()


def test_create_command_generates_project(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        ["create", "orders-api", "--destination", str(tmp_path)],
    )

    assert result.exit_code == 0
    assert "Project generated successfully" in result.stdout
    assert (tmp_path / "orders-api/app/main.py").exists()


def test_version_command() -> None:
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "1.0.0"
