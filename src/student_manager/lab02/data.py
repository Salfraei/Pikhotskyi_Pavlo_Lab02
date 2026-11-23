"""Scientific experiment data and basic collection types."""
from student_manager.models import Experiment
from student_manager.main import demo_experiments

def load_experiments() -> list[Experiment]:
    return demo_experiments()

def experiment_ids(records: list[Experiment]) -> set[int]:
    return {e.experiment_id for e in records}

def experiment_index(records: list[Experiment]) -> dict[int, Experiment]:
    return {e.experiment_id: e for e in records}

def experiment_tuple(record: Experiment) -> tuple[int,str,float]:
    return (record.experiment_id, record.parameter,record.result)
