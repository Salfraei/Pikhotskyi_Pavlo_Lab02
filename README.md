# Experiment Manager — Lab 02

Laboratory project for the course "Professional Python".

## Description

Collections and functional data analysis. Individual variant: **15** — scientific experiment results.

Проаналізувати записи експериментів у колекціях Python: групування за параметрами й дослідниками, агрегування результатів, сортування та пошук.

Core experiment fields: `experiment_id`, `name`, `researcher`, `parameter`, `result`, `date`.
This project is a cumulative version of the same application (laboratories 01–02); previous Python modules are preserved in `src/student_manager/`.

The implementation includes list, tuple, set, dict, collections, comprehensions, *args, **kwargs, closures, decorators, search, filtering and grouping.

## Requirements

Python 3.11+.

## Installation

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project in editable mode with testing dependencies:

```powershell
python -m pip install -e ".[dev]"
```

If script activation is disabled, use `.\.venv\Scripts\python.exe` in place of `python` in all commands.

## Run

Run the current laboratory as a Python module:

```powershell
python -m student_manager.lab02.main
```

Run the base console application (laboratory 01):

```powershell
python -m student_manager.main
```

or through its console command:

```powershell
student-manager
```

Run automated tests:

```powershell
python -m pytest -v
```

## Project structure

```text
Pikhotskyi_Pavlo_Lab02/
├── pyproject.toml
├── README.md
├── .gitignore
├── src/
│   └── student_manager/
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       ├── services.py
│       ├── analytics.py
│       ├── readers.py
│       ├── repositories.py
│       └── lab02/
├── tests/
├── data/
├── results/
└── report/
```

`src/student_manager/models.py` — base `Experiment`, `Researcher`, and `ExperimentStatistics` models.  
`src/student_manager/services.py` — core business logic, researcher search, value-range filtering, and statistics.  
`src/student_manager/main.py` — shared application entry point.  
`src/student_manager/lab02/` — additional modules specific to laboratory 02.  
`src/student_manager/lab02/data.py` — sample experiment records.  
`src/student_manager/lab02/processors.py` — processing and grouping.  
`src/student_manager/lab02/analytics.py` — statistics and aggregation.  
`src/student_manager/lab02/decorators.py` — decorators.  
`src/student_manager/lab02/benchmark.py` — performance measurements.  
`tests/` — unit/integration tests; `data/` — sample experimental data; `results/` — execution output; `report/` — PDF report.

## Author

Student: Піхоцький Павло  
Group: ФеП-31  
Variant: 15
