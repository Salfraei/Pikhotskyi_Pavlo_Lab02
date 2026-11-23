from pathlib import Path
import importlib

def test_variant_15_models_and_core_modules():
    for name in ['student_manager.main', 'student_manager.models',
                 'student_manager.services', 'student_manager.readers']:
        assert importlib.import_module(name)
    from student_manager.main import demo_experiments
    from student_manager.services import calculate_statistics
    assert calculate_statistics(demo_experiments()).count == 4

def test_mandatory_directories():
    root=Path(__file__).resolve().parents[1]
    for name in ('src/student_manager','tests','data','report'):
        assert (root/name).is_dir()

def test_lab01_required_files_exist():
    root = Path(__file__).resolve().parents[1]
    required = (
        'src/student_manager/__init__.py',
        'src/student_manager/models.py',
        'src/student_manager/services.py',
        'src/student_manager/main.py',
        'README.md',
        '.gitignore',
        'pyproject.toml',
    )
    assert all((root / name).is_file() for name in required)


def test_progressive_modules_of_current_laboratory_exist():
    root = Path(__file__).resolve().parents[1] / "src" / "student_manager"
    for number in range(2, 3):
        module = root / f"lab{number:02d}"
        assert module.is_dir(), f"Missing earlier laboratory module: {module}"
        assert (module / "main.py").is_file(), f"Missing entry point: {module}"
