"""Pure business logic for variant 15 (no DB / IO dependency)."""
from __future__ import annotations
from collections.abc import Iterable, Sequence
from math import fsum
from student_manager.models import Experiment, ExperimentStatistics

class DuplicateExperimentError(ValueError):
    """Experiment ID already exists."""

def add_experiment(experiments: list[Experiment], experiment: Experiment) -> None:
    if any(old.experiment_id == experiment.experiment_id for old in experiments):
        raise DuplicateExperimentError(f"Duplicate experiment ID: {experiment.experiment_id}")
    experiments.append(experiment)

def find_experiment_by_id(experiments: Iterable[Experiment], experiment_id: int) -> Experiment | None:
    return next((e for e in experiments if e.experiment_id == experiment_id), None)

def find_experiments_by_researcher(experiments: Iterable[Experiment], researcher: str) -> list[Experiment]:
    term = researcher.strip().casefold()
    return [e for e in experiments if term in e.researcher.casefold()] if term else []

def filter_by_researcher(experiments: Iterable[Experiment], researcher: str) -> list[Experiment]:
    return find_experiments_by_researcher(experiments, researcher)

def filter_by_result_range(experiments: Iterable[Experiment], minimum: float, maximum: float) -> list[Experiment]:
    if minimum > maximum:
        raise ValueError("minimum may not exceed maximum")
    return [e for e in experiments if minimum <= e.result <= maximum]

def calculate_average(experiments: Iterable[Experiment]) -> float | None:
    values = [e.result for e in experiments]
    return fsum(values) / len(values) if values else None

def average_result(experiments: Iterable[Experiment]) -> float | None:
    return calculate_average(experiments)

def minimum_result(experiments: Iterable[Experiment]) -> float | None:
    return min((e.result for e in experiments), default=None)

def maximum_result(experiments: Iterable[Experiment]) -> float | None:
    return max((e.result for e in experiments), default=None)

def calculate_statistics(experiments: Iterable[Experiment]) -> ExperimentStatistics:
    values = [e.result for e in experiments]
    if not values:
        return ExperimentStatistics(0, None, None, None)
    return ExperimentStatistics(len(values), fsum(values) / len(values), min(values), max(values))

def summarize_experiments(experiments: Iterable[Experiment]) -> ExperimentStatistics:
    return calculate_statistics(experiments)

def sort_experiments_by_date(experiments: Iterable[Experiment], descending: bool = False) -> list[Experiment]:
    return sorted(experiments, key=lambda e: (e.date, e.experiment_id), reverse=descending)

def group_by_researcher(experiments: Iterable[Experiment]) -> dict[str, list[Experiment]]:
    groups: dict[str, list[Experiment]] = {}
    for experiment in experiments:
        groups.setdefault(experiment.researcher, []).append(experiment)
    return groups

class ExperimentService:
    """In-memory application service; persistence added in later labs."""
    def __init__(self, experiments: Iterable[Experiment] = ()) -> None:
        self._experiments: list[Experiment] = []
        for e in experiments:
            self.add(e)

    def add(self, experiment: Experiment) -> None:
        add_experiment(self._experiments, experiment)

    def list_all(self) -> list[Experiment]:
        return list(self._experiments)

    def get(self, experiment_id: int) -> Experiment | None:
        return find_experiment_by_id(self._experiments, experiment_id)

    def by_researcher(self, researcher: str) -> list[Experiment]:
        return find_experiments_by_researcher(self._experiments, researcher)

    def in_range(self, minimum: float, maximum: float) -> list[Experiment]:
        return filter_by_result_range(self._experiments, minimum, maximum)

    def statistics(self) -> ExperimentStatistics:
        return calculate_statistics(self._experiments)
