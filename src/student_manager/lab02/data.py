"""Демонстраційні структуровані дані, створені на основі ЛР №1."""

from typing import TypedDict

from student_manager.main import create_demo_students


class StudentRecord(TypedDict):
    """Структура запису, яка зручна для індексів і comprehensions."""

    id: int
    name: str
    group: str
    grade: float


FIELDS: tuple[str, ...] = ("id", "name", "group", "grade")


def load_students() -> list[StudentRecord]:
    """Перетворити dataclass з ЛР №1 на словники з числовими ID."""
    base = [
        StudentRecord(
            id=number,
            name=f"{student.last_name} {student.first_name}",
            group=student.group,
            grade=student.average_grade,
        )
        for number, student in enumerate(create_demo_students(), 1)
    ]
    base.extend(
        [
            StudentRecord(id=5, name="Савчук Назар", group="ФеП-32", grade=84.0),
            StudentRecord(id=6, name="Шевченко Андрій", group="ФеП-31", grade=90.5),
        ]
    )
    return base
