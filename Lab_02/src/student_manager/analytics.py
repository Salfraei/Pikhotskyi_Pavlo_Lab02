"""Statistics of scientific experiment results for variant 15."""
from __future__ import annotations
from collections import defaultdict
from collections.abc import Iterable
from math import fsum, sqrt
from student_manager.models import Experiment

def standard_deviation(records: Iterable[Experiment]) -> float | None:
    values=[e.result for e in records]
    if not values:return None
    average=fsum(values)/len(values)
    return sqrt(fsum((x-average)**2 for x in values)/len(values))

def statistics_by_parameter(records: Iterable[Experiment]) -> dict[str,dict[str,float]]:
    groups: defaultdict[str,list[float]]=defaultdict(list)
    for experiment in records:
        groups[experiment.parameter].append(experiment.result)
    return {key:{"count":len(values), "average":fsum(values)/len(values),
                 "minimum":min(values), "maximum":max(values)}
            for key,values in groups.items()}

def find_extreme_experiments(records: Iterable[Experiment]) -> tuple[Experiment | None, Experiment | None]:
    records=list(records)
    if not records:return None,None
    return min(records,key=lambda e:e.result),max(records,key=lambda e:e.result)
