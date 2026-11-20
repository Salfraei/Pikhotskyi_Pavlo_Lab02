"""Порівняння лінійного пошуку в list і індексованого в dict."""

import csv
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import TypeVar

from student_manager.lab02.data import StudentRecord
from student_manager.lab02.processors import create_index, find_indexed, find_linear

T = TypeVar("T")
SIZES: tuple[int, ...] = (1_000, 10_000, 100_000)


@dataclass(frozen=True)
class BenchmarkResult:
    count: int
    list_us: float
    dict_us: float
    index_build_ms: float
    speedup: float


def generate_records(count: int) -> list[StudentRecord]:
    """Створити відтворювані записи без випадковості."""
    if count < 1:
        raise ValueError("Кількість записів має бути додатною")
    return [
        StudentRecord(
            id=number,
            name=f"Студент {number:06d}",
            group=f"ФеП-{31 + number % 3}",
            grade=float((number * 17) % 101),
        )
        for number in range(1, count + 1)
    ]


def _average_lookup_us(operation: Callable[[], T], repeats: int, trials: int = 3) -> float:
    """Мінімум трьох серій; середній час одного виклику в мікросекундах."""
    per_trial = []
    for _ in range(trials):
        started = perf_counter()
        for _ in range(repeats):
            operation()
        per_trial.append((perf_counter() - started) * 1_000_000 / repeats)
    return min(per_trial)


def run_benchmark(sizes: tuple[int, ...] = SIZES) -> list[BenchmarkResult]:
    """У кожній серії шукається останній ID: найгірший випадок для list."""
    results = []
    for count in sizes:
        students = generate_records(count)
        started = perf_counter()
        index = create_index(students)
        build_ms = (perf_counter() - started) * 1_000
        target = count
        assert find_linear(students, target) == find_indexed(index, target)
        list_us = _average_lookup_us(lambda: find_linear(students, target), repeats=100)
        dict_us = _average_lookup_us(lambda: find_indexed(index, target), repeats=100_000)
        results.append(
            BenchmarkResult(
                count=count,
                list_us=list_us,
                dict_us=dict_us,
                index_build_ms=build_ms,
                speedup=list_us / dict_us if dict_us else float("inf"),
            )
        )
    return results


def export_csv(results: list[BenchmarkResult], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["records", "list_search_us", "dict_search_us", "index_build_ms", "speedup"])
        for row in results:
            writer.writerow(
                [row.count, f"{row.list_us:.6f}", f"{row.dict_us:.6f}", f"{row.index_build_ms:.6f}", f"{row.speedup:.2f}"]
            )
