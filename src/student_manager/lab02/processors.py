"""Пошук, фільтрація та групування структурованих записів."""

from collections import Counter, defaultdict, deque
from collections.abc import Callable, Iterable, Sequence

from student_manager.lab02.data import StudentRecord


def unique_groups(students: Iterable[StudentRecord]) -> set[str]:
    """Set comprehension: повернути перелік унікальних груп."""
    return {student["group"] for student in students}


def create_index(students: Iterable[StudentRecord]) -> dict[int, StudentRecord]:
    """Dict comprehension: індекс ID → запис; дублікати заборонені."""
    items = list(students)
    index = {student["id"]: student for student in items}
    if len(index) != len(items):
        raise ValueError("Ідентифікатори студентів мають бути унікальними")
    return index


def filter_by_group(students: Iterable[StudentRecord], group: str) -> list[StudentRecord]:
    """List comprehension: вибрати одну групу."""
    selected = group.strip().casefold()
    return [student for student in students if student["group"].casefold() == selected]


def filter_items(
    students: Iterable[StudentRecord],
    predicate: Callable[[StudentRecord], bool],
) -> list[StudentRecord]:
    """Універсальна фільтрація через функцію вищого порядку."""
    return [student for student in students if predicate(student)]


def group_students(students: Iterable[StudentRecord]) -> dict[str, list[StudentRecord]]:
    """Defaultdict(list) для групування студентів."""
    groups: defaultdict[str, list[StudentRecord]] = defaultdict(list)
    for student in students:
        groups[student["group"]].append(student)
    return dict(groups)


def count_by_group(students: Iterable[StudentRecord]) -> Counter[str]:
    """Counter: кількість студентів за групами."""
    return Counter(student["group"] for student in students)


def group_by_group_and_band(
    students: Iterable[StudentRecord],
) -> dict[str, dict[str, list[StudentRecord]]]:
    """Вкладене групування за групою та діапазоном балів."""
    grouped: defaultdict[str, defaultdict[str, list[StudentRecord]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for student in students:
        band = "90–100" if student["grade"] >= 90 else "0–89.99"
        grouped[student["group"]][band].append(student)
    return {group: dict(bands) for group, bands in grouped.items()}


def find_linear(students: Sequence[StudentRecord], student_id: int) -> StudentRecord | None:
    """Лінійний пошук O(n), потрібний також для benchmark."""
    for student in students:
        if student["id"] == student_id:
            return student
    return None


def find_indexed(index: dict[int, StudentRecord], student_id: int) -> StudentRecord | None:
    """Пошук за ключем у dict: O(1) у середньому."""
    return index.get(student_id)


class OperationHistory:
    """Deque автоматично залишає тільки кілька останніх операцій."""

    def __init__(self, limit: int = 5) -> None:
        if limit < 1:
            raise ValueError("limit має бути більшим за нуль")
        self._history: deque[str] = deque(maxlen=limit)

    def add(self, operation: str) -> None:
        self._history.append(operation)

    def recent(self) -> tuple[str, ...]:
        return tuple(self._history)
