# Лабораторна №2 — почати тут

1. Розпакуй ZIP до `C:\Users\Pavlo\Documents\ProfessionalPython\Pikhotskyi_Pavlo_Lab02` (це приклад, твій шлях може бути іншим).
2. VS Code → File → Open Folder → вибери папку `Pikhotskyi_Pavlo_Lab02`.
3. Terminal → New Terminal (PowerShell).
4. Виконай команди:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m student_manager.lab02.main --mode all
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

5. Переконайся, що є файл `results/benchmark.csv`.
6. Прочитай `GIT_COMMANDS.md`, щоб поетапно оформити Git-історію.
7. PDF-звіт знаходиться в `report/`.

**Якщо команда `py` недоступна:** заміни першу на `python -m venv .venv`.

**Важливо:** у методичці немає опису варіанта №15 — реалізований приклад варіанта №1 (аналіз студентів), пов'язаний із ЛР №1.
