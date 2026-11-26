# Experiment Manager

Laboratory project for the course "Professional Python".

## Description

Console application for recording scientific experiments and processing experimental data using Python collections.
Individual variant: **15** — scientific experiment results.

For each experiment, the program stores `experiment_id`, `name`, `researcher`, `parameter`, `result`, and `date`.
It supports searching by researcher, filtering by result range, grouping, sorting and calculating experimental statistics.

Laboratory work No. 2 extends the application from Lab 01 with `list`, `tuple`, `set`, `dict`, `Counter`, `defaultdict`, `deque`, comprehensions, `*args`, `**kwargs`, `lambda`, closures and decorators.

## Requirements

Python 3.11+

## Installation

```powershell
python -m venv .venv
```

Activate the virtual environment (Windows PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project in editable mode:

```powershell
python -m pip install -e ".[dev]"
```

## Run

```powershell
python -m student_manager.main
```

or:

```powershell
student-manager
```

Run the additional Lab 02 data processing demonstration:

```powershell
python -m student_manager.lab02.main
```

Example of the Lab 02 benchmarking mode:

```powershell
python -m student_manager.lab02.main --mode benchmark
```

Run the tests:

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
│           ├── __init__.py
│           ├── main.py
│           ├── data.py
│           ├── processors.py
│           ├── analytics.py
│           ├── decorators.py
│           └── benchmark.py
├── data/
│   └── experiments_sample.csv
├── tests/
├── results/
└── report/
    └── Pikhotskyi_Pavlo_Lab02.pdf
```

`src/student_manager/models.py` — data models `Experiment`, `Researcher`, `ExperimentStatistics`.  
`src/student_manager/services.py` — business logic, search, filtering, statistics.  
`src/student_manager/main.py` — base application entry point from Lab 01.  
`src/student_manager/lab02/data.py` — sample scientific experiment records and collection indexes.  
`src/student_manager/lab02/processors.py` — filtering, grouping, sorting, and collection operations.  
`src/student_manager/lab02/analytics.py` — statistical aggregation.  
`src/student_manager/lab02/decorators.py` — decorator for measuring execution time.  
`src/student_manager/lab02/main.py` — Lab 02 application entry point.  
`tests/` — automated tests.  
`data/` — sample scientific experiment data.  
`report/` — laboratory report in PDF format.

## Author

Student: Піхоцький Павло  
Group: ФеП-31  
Variant: 15
