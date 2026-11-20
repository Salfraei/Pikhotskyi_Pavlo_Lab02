$ErrorActionPreference = "Stop"
if (-not (Test-Path .venv)) { py -3 -m venv .venv }
& .\.venv\Scripts\python.exe -m pip install -e .
& .\.venv\Scripts\python.exe -m student_manager.lab02.main --mode all
& .\.venv\Scripts\python.exe -m unittest discover -s tests -v
