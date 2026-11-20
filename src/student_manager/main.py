"""Точка входу в консольний застосунок: демонстрація та інтерактивне меню."""

import argparse

from student_manager import __version__
from student_manager.models import Student
from student_manager.services import (
    DuplicateStudentError,
    add_student,
    calculate_group_average,
    filter_by_group,
    find_best_student,
    find_students,
    group_statistics,
    sort_students,
)


DEMO_GROUP = "ФеП-31"


def create_demo_students() -> list[Student]:
    """Демонстраційний набір для відтворюваного запуску."""
    return [
        Student("Павло", "Піхоцький", "ФеП-31", 92.5),
        Student("Олена", "Коваль", "ФеП-31", 88.0),
        Student("Іван", "Мельник", "ФеП-31", 79.5),
        Student("Марія", "Бондар", "ФеП-32", 95.0),
    ]


def print_students(students: list[Student]) -> None:
    """Вивести коротку таблицю студентів."""
    if not students:
        print("Записів не знайдено.")
        return
    print(f"{'№':<3} {'Прізвище та ім’я':<28} {'Група':<10} {'Бал':>6}")
    print("-" * 52)
    for number, student in enumerate(students, start=1):
        name = f"{student.last_name} {student.first_name}"
        print(f"{number:<3} {name:<28} {student.group:<10} {student.average_grade:>6.2f}")


def run_demo() -> None:
    """Показати всі основні можливості програми без введення з клавіатури."""
    students = create_demo_students()
    print("Лабораторна робота №1 | Професійний Python")
    print("Система обліку студентів — демонстраційний приклад")
    print("\nУсі студенти:")
    print_students(students)

    selected = filter_by_group(students, DEMO_GROUP)
    print(f"\nСтуденти групи {DEMO_GROUP}:")
    print_students(selected)
    print(f"Середній бал групи: {calculate_group_average(selected):.2f}")

    best = find_best_student(students)
    if best is not None:
        print(f"\nНайкращий студент: {best.full_name} ({best.average_grade:.2f})")

    print("\nПошук за фрагментом «піхо»:")
    print_students(find_students(students, "піхо"))

    print("\nСортування за балом (від більшого):")
    print_students(sort_students(students, by="grade", descending=True))

    print("\nСтатистика груп:")
    for group, (count, average) in group_statistics(students).items():
        print(f"  {group}: {count} студент(ів), середній бал {average:.2f}")


def read_student() -> Student:
    """Прочитати й перевірити дані одного студента."""
    first_name = input("Ім'я: ").strip()
    last_name = input("Прізвище: ").strip()
    group = input("Група: ").strip()
    raw_grade = input("Середній бал (0–100): ").strip().replace(",", ".")
    try:
        grade = float(raw_grade)
    except ValueError as exc:
        raise ValueError("Середній бал потрібно ввести числом") from exc
    return Student(first_name, last_name, group, grade)


def run_interactive() -> None:
    """Інтерактивне меню, що дозволяє працювати з даними користувача."""
    students = create_demo_students()
    while True:
        print("\n1. Показати всіх студентів")
        print("2. Додати студента")
        print("3. Показати групу та її середній бал")
        print("4. Пошук за прізвищем/іменем/групою")
        print("5. Сортування за балом")
        print("6. Статистика всіх груп")
        print("7. Найкращий студент")
        print("0. Вийти")
        choice = input("Оберіть дію: ").strip()

        if choice == "0":
            print("Роботу завершено.")
            return
        if choice == "1":
            print_students(students)
        elif choice == "2":
            try:
                new_student = read_student()
                add_student(students, new_student)
            except (ValueError, DuplicateStudentError) as exc:
                print(f"Помилка: {exc}")
            else:
                print("Студента додано.")
        elif choice == "3":
            group = input("Назва групи: ")
            filtered = filter_by_group(students, group)
            print_students(filtered)
            if filtered:
                print(f"Середній бал: {calculate_group_average(filtered):.2f}")
        elif choice == "4":
            query = input("Запит: ")
            print_students(find_students(students, query))
        elif choice == "5":
            print_students(sort_students(students, by="grade", descending=True))
        elif choice == "6":
            for group, (count, average) in group_statistics(students).items():
                print(f"{group}: {count} студент(ів), середній бал {average:.2f}")
        elif choice == "7":
            best = find_best_student(students)
            if best is not None:
                print(f"Найкращий студент: {best.full_name} — {best.average_grade:.2f}")
        else:
            print("Невідома команда. Спробуйте ще раз.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Навчальний облік студентів")
    parser.add_argument("--interactive", action="store_true", help="запуск із меню")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args()
    try:
        if args.interactive:
            run_interactive()
        else:
            run_demo()
    except (KeyboardInterrupt, EOFError):
        print("\nЗавершено користувачем.")


if __name__ == "__main__":
    main()
