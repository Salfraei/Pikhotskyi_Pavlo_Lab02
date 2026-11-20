"""Точка входу лабораторної №2: демонстрація та benchmark."""

import argparse
from pathlib import Path

from student_manager.lab02.analytics import (
    average_grade,
    average_values,
    create_record,
    find_best_student,
    group_statistics,
    make_grade_filter,
    process_pipeline,
    sort_records,
)
from student_manager.lab02.benchmark import export_csv, run_benchmark
from student_manager.lab02.data import StudentRecord, load_students
from student_manager.lab02.processors import (
    OperationHistory,
    count_by_group,
    create_index,
    filter_items,
    find_indexed,
    find_linear,
    group_by_group_and_band,
    group_students,
    unique_groups,
)


def print_rows(title: str, rows: list[StudentRecord]) -> None:
    print(f"\n{title}")
    print(f"{'ID':>3}  {'ПІБ':<26} {'Група':<9} {'Бал':>6}")
    print("-" * 52)
    for row in rows:
        print(f"{row['id']:>3}  {row['name']:<26} {row['group']:<9} {row['grade']:>6.2f}")


def run_demo() -> None:
    students = load_students()
    history = OperationHistory(5)
    print("Лабораторна робота №2 / варіант за списком №15")
    print("Навчальний приклад: аналіз успішності студентів, продовження ЛР №1")
    print_rows("Початковий набір даних:", students)
    print("\nКортеж полів:", ("id", "name", "group", "grade"))
    groups = unique_groups(students)
    print("Унікальні групи (set):", ", ".join(sorted(groups)))
    print(f"Середній бал (generator): {average_grade(students):.2f}")
    best = find_best_student(students)
    print("Найкращий студент:", best["name"] if best else "немає")
    history.add("Обчислено середній бал і найкращого студента")
    index = create_index(students)
    for candidate in (3, 99):
        found = find_indexed(index, candidate)
        print(f"Пошук ID={candidate}: {found['name'] if found else 'не знайдено'}")
    assert find_linear(students, 3) == index.get(3)
    history.add("Пошук у list і dict-index")
    print_rows("Рейтинг за балом (lambda):", sort_records(students, field="grade"))
    history.add("Сортування за балом")
    print("\nКількість за групами (Counter):", dict(sorted(count_by_group(students).items())))
    print("Групування (defaultdict):", {k: len(v) for k,v in sorted(group_students(students).items())})
    print("Вкладене групування:", {group: {band: len(m) for band,m in bands.items()} for group,bands in group_by_group_and_band(students).items()})
    for group, (count, avg) in group_statistics(students).items():
        print(f"  {group}: {count} осіб; середній бал {avg:.2f}")
    history.add("Групування та статистика")
    good = filter_items(students, make_grade_filter(90))
    print_rows("Closure: оцінка >= 90:", good)
    print_rows("Pipeline: ФеП-31, оцінка >= 85:", process_pipeline(students, minimum=85, group="ФеП-31"))
    print(f"\n*args: середнє 75, 80, 92, 96 = {average_values(75, 80, 92, 96):.2f}")
    created = create_record(id=7, name="Новак Тарас", group="ФеП-33", grade=87.0)
    print("**kwargs: створено запис:", created)
    history.add("Фільтрація, pipeline, *args, **kwargs")
    print("Останні операції (deque):", " | ".join(history.recent()))


def run_experiment(output_dir: Path) -> None:
    rows = run_benchmark()
    print("\nBENCHMARK: пошук останнього ID, три серії")
    print(f"{'Записів':>10} {'list, мкс':>12} {'dict, мкс':>12} {'Індекс, мс':>12} {'Прискорення':>12}")
    for row in rows:
        print(f"{row.count:>10} {row.list_us:>12.3f} {row.dict_us:>12.3f} {row.index_build_ms:>12.3f} {row.speedup:>11.1f}x")
    target = output_dir / "benchmark.csv"
    export_csv(rows, target)
    print("CSV:", target)
    print("Увага: час залежить від процесора, ОС та поточного навантаження.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Структури даних та функціональна декомпозиція")
    parser.add_argument("--mode", choices=["demo", "benchmark", "all"], default="all")
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    args = parser.parse_args()
    if args.mode in ("demo", "all"):
        run_demo()
    if args.mode in ("benchmark", "all"):
        run_experiment(args.output_dir)


if __name__ == "__main__":
    main()
