"""Типізовані моделі даних консольної програми."""

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True, slots=True)
class Student:
    """Студент та його середній бал за шкалою від 0 до 100."""

    first_name: str
    last_name: str
    group: str
    average_grade: float

    def __post_init__(self) -> None:
        for field in ("first_name", "last_name", "group"):
            value = getattr(self, field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Поле {field} не може бути порожнім")
            object.__setattr__(self, field, value.strip())

        if not isinstance(self.average_grade, (int, float)):
            raise ValueError("Середній бал має бути числом")
        if not isfinite(self.average_grade) or not 0 <= self.average_grade <= 100:
            raise ValueError("Середній бал повинен бути в межах 0..100")
        object.__setattr__(self, "average_grade", float(self.average_grade))

    @property
    def full_name(self) -> str:
        """Повернути ім'я та прізвище для друку й пошуку."""
        return f"{self.first_name} {self.last_name}"
