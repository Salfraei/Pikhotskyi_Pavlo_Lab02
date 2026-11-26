"""Tests for laboratory 1 core business logic and command-line behavior."""
from __future__ import annotations

from pathlib import Path

import pytest

from student_manager.main import create_demo_experiments, print_experiments, run_demo
from student_manager.services import (
    calculate_statistics,
    filter_by_result_range,
    find_experiments_by_researcher,
)


def test_demo_contains_scientific_experiments() -> None:
    experiments = create_demo_experiments()
    assert len(experiments) == 4
    assert experiments[0].parameter == "temperature"


def test_find_researcher_variant_15() -> None:
    experiments = create_demo_experiments()
    found = find_experiments_by_researcher(experiments, "іваненко")
    assert len(found) == 2


def test_average_minimum_maximum() -> None:
    statistics = calculate_statistics(create_demo_experiments())
    assert statistics.count == 4
    assert statistics.minimum == pytest.approx(4.95)
    assert statistics.maximum == pytest.approx(101.5)


def test_range_boundaries() -> None:
    found = filter_by_result_range(create_demo_experiments(), 23.4, 25.2)
    assert [item.experiment_id for item in found] == [1, 3]


def test_empty_dataset_statistics() -> None:
    statistics = calculate_statistics([])
    assert statistics.count == 0
    assert statistics.average is None


def test_print_experiments(capsys: pytest.CaptureFixture[str]) -> None:
    print_experiments(create_demo_experiments())
    captured = capsys.readouterr().out
    assert "Experiments:" in captured
    assert "temperature=23.4" in captured


def test_empty_csv_no_crash(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    input_file = tmp_path / "empty.csv"
    input_file.write_text("experiment_id,name,researcher,parameter,result,date\n", encoding="utf-8")
    run_demo(input_file)
    output = capsys.readouterr().out
    assert "Count=0" in output
    assert "Average=N/A" in output


def test_csv_with_records(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    input_file = tmp_path / "sample.csv"
    input_file.write_text(
        "experiment_id,name,researcher,parameter,result,date\n"
        "101,Test,Oksana,temperature,12.5,2026-10-10\n",
        encoding="utf-8",
    )
    run_demo(input_file, researcher="Oksana")
    output = capsys.readouterr().out
    assert "Count=1; Average=12.500" in output
    assert "Researcher search: ['Test']" in output
