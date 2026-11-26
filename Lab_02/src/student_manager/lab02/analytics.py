"""Aggregate numerical results and compare list/index lookup complexity."""
from __future__ import annotations
from collections.abc import Iterable
from collections import defaultdict
from math import fsum
from student_manager.models import Experiment

def average_values(*values: float) -> float | None:
    return fsum(values)/len(values) if values else None

def describe_experiment(**kwargs: object) -> dict[str,object]:
    """Demonstration of validated **kwargs contract."""
    fields={"experiment_id","name","researcher","parameter","result","date"}
    if set(kwargs)!=fields:
        raise ValueError('Expected all six variant-15 fields')
    from student_manager.readers import parse_experiment
    return parse_experiment(kwargs).to_dict()

def summarize(records: Iterable[Experiment]) -> dict[str,float | int | None]:
    values=[r.result for r in records]
    return {"count":len(values), "average":average_values(*values),
            "minimum":min(values,default=None),"maximum":max(values,default=None)}

def averages_by_researcher(records: Iterable[Experiment]) -> dict[str,float]:
    groups: defaultdict[str,list[float]]=defaultdict(list)
    for r in records:groups[r.researcher].append(r.result)
    return {name:fsum(values)/len(values) for name,values in groups.items()}

def best_experiment(records: Iterable[Experiment]) -> Experiment | None:
    return max(records,key=lambda r:r.result,default=None)
