"""CSV and JSON input interfaces; used by the next labs as well."""
from __future__ import annotations
import csv
import json
from pathlib import Path
from collections.abc import Iterator
from student_manager.models import Experiment

FIELDNAMES = ("experiment_id", "name", "researcher", "parameter", "result", "date")

def parse_experiment(row: dict[str, object]) -> Experiment:
    return Experiment(
        experiment_id=int(str(row["experiment_id"])),
        name=str(row["name"]), researcher=str(row["researcher"]),
        parameter=str(row["parameter"]), result=float(str(row["result"])),
        date=str(row["date"]),
    )

def read_experiments_csv(path: str | Path) -> Iterator[Experiment]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not set(FIELDNAMES).issubset(reader.fieldnames):
            raise ValueError("CSV schema does not match variant 15")
        for row in reader:
            yield parse_experiment(row)

def export_experiments_json(experiments: list[Experiment], path: str | Path) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps([e.to_dict() for e in experiments], indent=2, ensure_ascii=False), encoding="utf-8")
