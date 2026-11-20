"""Агрегація, статистика, сортування, closure, *args і **kwargs."""

from collections.abc import Callable, Iterable, Sequence
from math import isfinite

from student_manager.lab02.data import StudentRecord
from student_manager.lab02.decorators import measure_time
from student_manager.lab02.processors import group_students


@measure_time("Обчислення середнього бала")
def average_grade(students: Sequence[StudentRecord]) -> float:
    """Генераторний вираз: без проміжного списку оцінок."""
    return sum(student["grade"] for student in students) / len(students) if students else 0.0


def average_values(*values: float) -> float:
    """*args: середнє довільної кількості чисел."""
    return sum(values) / len(values) if values else 0.0


def create_record(**fields: object) -> StudentRecord:
    """**kwargs: створення типізованого запису з перевіркою полів."""
    if set(fields) != {"id", "name", "group", "grade"}:
        raise ValueError("Потрібні поля: id, name, group, grade")
    record_id, name, group, grade = (
        fields["id"], fields["name"], fields["group"], fields["grade"]
    )
    if type(record_id) is not int or record_id < 1:
        raise ValueError("id має бути додатним цілим числом")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name не може бути порожнім")
    if not isinstance(group, str) or not group.strip():
        raise ValueError("group не може бути порожньою")
    if isinstance(grade, bool) or not isinstance(grade, (int, float)):
        raise ValueError("grade має бути числом")
    if not isfinite(grade) or not 0 <= grade <= 100:
        raise ValueError("grade має бути в межах 0–100")
    return StudentRecord(id=record_id, name=name.strip(), group=group.strip(), grade=float(grade))


def find_best_student(students: Sequence[StudentRecord]) -> StudentRecord | None:
    return max(students, key=lambda student: student["grade"], default=None)


def sort_records(
    students: Iterable[StudentRecord],
    *,
    field: str = "grade",
    descending: bool = True,
) -> list[StudentRecord]:
    """Універсальне сортування; lambda визначає ключ."""
    if field not in ("id", "name", "group", "grade"):
        raise ValueError("Недопустиме поле сортування")
    if field in ("name", "group"):
        return sorted(students, key=lambda student: str(student[field]).casefold(), reverse=descending)
    return sorted(students, key=lambda student: student[field], reverse=descending)


def make_grade_filter(minimum: float) -> Callable[[StudentRecord], bool]:
    """Closure запам'ятовує поріг після завершення зовнішньої функції."""
    if not 0 <= minimum <= 100:
        raise ValueError("Поріг має бути у межах 0–100")

    def matches(student: StudentRecord) -> bool:
        return student["grade"] >= minimum

    return matches


def group_statistics(students: Iterable[StudentRecord]) -> dict[str, tuple[int, float]]:
    """Dict[str, tuple[кількість, середній бал]] для кожної групи."""
    groups = group_students(students)
    return {
        group: (len(members), sum(s["grade"] for s in members) / len(members))
        for group, members in sorted(groups.items())
    }


def process_pipeline(
    students: Iterable[StudentRecord],
    *,
    minimum: float,
    group: str | None = None,
) -> list[StudentRecord]:
    """Фільтрація → фільтр за групою → сортування за балом."""
    predicate = make_grade_filter(minimum)
    selected = [student for student in students if predicate(student)]
    if group is not None:
        selected = [student for student in selected if student["group"].casefold() == group.casefold()]
    return sort_records(selected)
