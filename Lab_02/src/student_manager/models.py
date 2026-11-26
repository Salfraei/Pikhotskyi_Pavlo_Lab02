"""Variant 15 data models: results of scientific experiments."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date as Date
from math import isfinite

@dataclass(frozen=True, slots=True)
class Researcher:
    researcher_id: int
    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.researcher_id, int) or isinstance(self.researcher_id, bool) or self.researcher_id <= 0:
            raise ValueError("researcher_id must be positive")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("researcher name is required")
        object.__setattr__(self, "name", self.name.strip())

@dataclass(frozen=True, slots=True)
class Experiment:
    experiment_id: int
    name: str
    researcher: str
    parameter: str
    result: float
    date: Date | str

    def __post_init__(self) -> None:
        if type(self.experiment_id) is not int or self.experiment_id <= 0:
            raise ValueError("experiment_id must be a positive integer")
        for field_name in ("name", "researcher", "parameter"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must not be empty")
            object.__setattr__(self, field_name, value.strip())
        if type(self.result) not in (int, float) or not isfinite(self.result):
            raise ValueError("result must be a finite number")
        object.__setattr__(self, "result", float(self.result))
        if isinstance(self.date, str):
            try:
                parsed = Date.fromisoformat(self.date)
            except ValueError as error:
                raise ValueError("date must be YYYY-MM-DD") from error
            object.__setattr__(self, "date", parsed)
        elif not isinstance(self.date, Date):
            raise ValueError("date must be a date or YYYY-MM-DD string")

    @property
    def id(self) -> int:
        return self.experiment_id

    def to_dict(self) -> dict[str, object]:
        return {"experiment_id": self.experiment_id, "name": self.name,
                "researcher": self.researcher, "parameter": self.parameter,
                "result": self.result, "date": self.date.isoformat()}

@dataclass(frozen=True, slots=True)
class ExperimentStatistics:
    count: int
    average: float | None
    minimum: float | None
    maximum: float | None
