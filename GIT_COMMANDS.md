# Git — команди для лабораторної №2 (PowerShell VS Code)

> Команди виконуються у корені розпакованого проєкту. GitHub-репозиторій створюй на github.com/new, **без автоматичного README**. Назва, наприклад, `Pikhotskyi_Pavlo_Lab02`.

```powershell
git init -b main
git config --global user.name "Pavlo Pikhotskyi"
git config --global user.email "YOUR_GITHUB_EMAIL@example.com"
```

**Обов'язково** заміни адресу на власну пошту GitHub. Глобальні ім'я й пошту достатньо встановити один раз. Якщо вони вже налаштовані, ці дві команди можна пропустити.

## Коміт 1 — структура й збереження ЛР №1

```powershell
git add .gitignore .gitattributes pyproject.toml
git add src/student_manager/__init__.py src/student_manager/main.py src/student_manager/models.py src/student_manager/services.py
git add src/student_manager/lab02/__init__.py
git commit -m "Preserve Lab01 and create Lab02 structure"
```

## Коміт 2 — модулі обробки даних

```powershell
git add src/student_manager/lab02/data.py src/student_manager/lab02/processors.py
git add src/student_manager/lab02/analytics.py src/student_manager/lab02/decorators.py
git add src/student_manager/lab02/benchmark.py
git commit -m "Add collections, analytics and benchmark"
```

## Коміт 3 — точка входу, тести, документація

```powershell
git add src/student_manager/lab02/main.py tests README.md START_HERE.md GIT_COMMANDS.md results/README.md
git commit -m "Add Lab02 CLI, tests and documentation"
```

## Коміт 4 — звіт

```powershell
git add report
git commit -m "Add Lab02 report"
git log --oneline
git status
```

## Підключення GitHub (якщо репозиторій порожній)

```powershell
git remote add origin https://github.com/YOUR_GITHUB_LOGIN/Pikhotskyi_Pavlo_Lab02.git
git push -u origin main
```

Заміни `YOUR_GITHUB_LOGIN` на свій логін. `git remote -v` показує URL підключеного репозиторію. Якщо `origin` уже існує, не додавай його вдруге; перевір `git remote -v`.

**Після завантаження:** `git status`, `git log --oneline`, перегляд репозиторію у браузері. Скріншоти Git для звіту мають бути з твого фактичного середовища, а не змодельованими.
