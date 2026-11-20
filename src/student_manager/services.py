"""Бізнес-логіка: пошук, фільтрація, сортування та статистика."""

from collections.abc import Sequence
from typing import Literal

from student_manager.models import Student


class DuplicateStudentError(ValueError):
    """Студент із таким ПІБ та групою вже є у списку."""


def add_student(students: list[Student], student: Student) -> None:
    """Додати студента, не допускаючи повторного запису в тій самій групі."""
    key = (student.full_name.casefold(), student.group.casefold())
    for existing in students:
        if (existing.full_name.casefold(), existing.group.casefold()) == key:
            raise DuplicateStudentError("Такий студент уже є в цій групі")
    students.append(student)


def filter_by_group(students: Sequence[Student], group: str) -> list[Student]:
    """Повернути студентів заданої групи без урахування регістру."""
    target = group.strip().casefold()
    return [student for student in students if student.group.casefold() == target]


def find_students(students: Sequence[Student], query: str) -> list[Student]:
    """Пошук за будь-якою частиною імені, прізвища або назви групи."""
    normalized = query.strip().casefold()
    if not normalized:
        return []
    return [
        student
        for student in students
        if normalized in student.full_name.casefold()
        or normalized in student.group.casefold()
    ]


def calculate_group_average(students: Sequence[Student]) -> float:
    """Середній бал; для порожньої вибірки повертається 0.0."""
    return sum(student.average_grade for student in students) / len(students) if students else 0.0


def find_best_student(students: Sequence[Student]) -> Student | None:
    """Повернути студента з найвищим середнім балом."""
    return max(students, key=lambda student: student.average_grade, default=None)


def sort_students(
    students: Sequence[Student],
    by: Literal["name", "grade", "group"] = "name",
    descending: bool = False,
) -> list[Student]:
    """Повернути новий відсортований список, не змінюючи початковий."""
    if by == "name":
        key = lambda student: (student.last_name.casefold(), student.first_name.casefold())
    elif by == "grade":
        key = lambda student: student.average_grade
    elif by == "group":
        key = lambda student: (student.group.casefold(), student.last_name.casefold())
    else:
        raise ValueError("Параметр by: name, grade або group")
    return sorted(students, key=key, reverse=descending)


def group_statistics(students: Sequence[Student]) -> dict[str, tuple[int, float]]:
    """Для кожної групи повернути (кількість студентів, середній бал)."""
    groups: dict[str, list[Student]] = {}
    for student in students:
        groups.setdefault(student.group, []).append(student)
    return {
        group: (len(members), calculate_group_average(members))
        for group, members in sorted(groups.items())
    }
