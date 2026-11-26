"""Documentation, layout, and cumulative project consistency (Lab 02)."""
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def test_readme_headings_follow_first_methodical_example():
    source = (ROOT / "README.md").read_text(encoding="utf-8")
    headings = ["## Description", "## Requirements", "## Installation", "## Run", "## Project structure", "## Author"]
    indices = [source.index(heading) for heading in headings]
    assert indices == sorted(indices)
    assert "variant: **15**" in source
    assert "python -m student_manager.lab02.main" in source


def test_layout_and_required_variant_modules():
    pkg = ROOT / "src" / "student_manager"
    for filename in ["__init__.py", "main.py", "models.py", "services.py", "analytics.py", "readers.py", "repositories.py"]:
        assert (pkg / filename).is_file(), filename
    for i in range(2, 3):
        assert (pkg / f"lab{i:02d}" / "main.py").is_file(), i
    for filename in ['data.py', 'processors.py', 'analytics.py', 'decorators.py', 'benchmark.py']:
        assert (pkg / "lab02" / filename).is_file(), filename
    assert (ROOT / "data").is_dir()
    assert (ROOT / "tests").is_dir()
    assert list((ROOT / "report").glob("*.pdf"))


def test_project_exposes_methodological_entrypoint():
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert config["project"]["requires-python"].startswith(">=3.11")
    assert config["project"]["scripts"]["student-manager"] == "student_manager.main:main"
