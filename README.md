# Professional Python — Піхоцький Павло / лабораторні №1–2

**Предмет:** Професійний Python. **Група:** ФеП-31. **Номер варіанта за списком:** 15.  
**Викладач:** Свелеба Сергій Андрійович.

> У документах ЛР №1–2 наведено детальну умову для варіанта 4 і приклад для варіанта 1, але немає формулювання індивідуального варіанта 15. Тому цей проєкт демонструє **приклад обліку студентів (варіант 1 з методички)** для відпрацювання технологій курсу, а **15** вказано лише як номер студента за списком.

## Вимоги

Windows 10/11, Python 3.11+, Visual Studio Code, Git. Сторонні Python-бібліотеки не потрібні.

## Швидкий запуск у PowerShell VS Code

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m student_manager.lab02.main --mode all
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Демонстраційний режим без порівняння швидкості: `--mode demo`. Лише benchmark: `--mode benchmark`. CSV вимірювань зберігається у `results/benchmark.csv`.

## Структура

- `src/student_manager/` — функціонал ЛР №1 (`models.py`, `services.py`, `main.py`).
- `src/student_manager/lab02/data.py` — структуровані записи, TypedDict, tuple, перетворення даних ЛР №1.
- `src/student_manager/lab02/processors.py` — list/set/dict comprehensions, Counter/defaultdict/deque, індекси, фільтрація, вкладене групування.
- `src/student_manager/lab02/analytics.py` — статистика, lambda, *args, **kwargs, closure, pipeline.
- `src/student_manager/lab02/decorators.py` — параметризований декоратор часу виконання.
- `src/student_manager/lab02/benchmark.py` — експеримент 1 000, 10 000, 100 000 записів.
- `src/student_manager/lab02/main.py` — вивід результатів та запуск експерименту.
- `tests/` — юніт-тести ЛР №1 і №2.
- `report/` — PDF-звіт.

## Примітка про вимірювання

`dict` потребує одноразової побудови індексу O(n), але забезпечує середній пошук за ключем O(1); лінійний пошук у списку має O(n). Часи на різних комп'ютерах можуть різнитися. У бенчмарку обидва методи шукають останній запис. Час вимірюється повторно і виводиться в мікросекундах на одну операцію.

## Автор

Піхоцький Павло, ФеП-31, 2026.
