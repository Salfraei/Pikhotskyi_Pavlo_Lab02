"""List/set/dict comprehensions, sorting, searching, grouping and decorators."""
from __future__ import annotations
from collections import Counter, defaultdict, deque
from collections.abc import Iterable, Callable
from student_manager.models import Experiment

def find_by_id(records: Iterable[Experiment], experiment_id: int) -> Experiment | None:
    return next((r for r in records if r.experiment_id == experiment_id),None)

def filter_by_researcher(records: Iterable[Experiment], term: str) -> list[Experiment]:
    query=term.strip().casefold()
    return [r for r in records if query and query in r.researcher.casefold()]

def filter_by_range(records: Iterable[Experiment], low: float, high: float) -> list[Experiment]:
    if low>high:raise ValueError('Invalid range')
    return [r for r in records if low<=r.result<=high]

def group_by_researcher(records: Iterable[Experiment]) -> dict[str,list[Experiment]]:
    data: defaultdict[str,list[Experiment]]=defaultdict(list)
    for r in records:data[r.researcher].append(r)
    return dict(data)

def sort_by_result(records: Iterable[Experiment], descending: bool=False) -> list[Experiment]:
    return sorted(records,key=lambda r:r.result,reverse=descending)

def unique_parameters(records: Iterable[Experiment]) -> set[str]:
    return {r.parameter for r in records}

def result_index(records: Iterable[Experiment]) -> dict[int,float]:
    return {r.experiment_id:r.result for r in records}

def count_parameters(records: Iterable[Experiment]) -> Counter[str]:
    return Counter(r.parameter for r in records)

def sliding_ids(records: Iterable[Experiment],size:int=2) -> list[tuple[int,...]]:
    if size<1:raise ValueError('size must be >= 1')
    window: deque[int]=deque(maxlen=size)
    output=[]
    for r in records:
        window.append(r.id)
        if len(window)==size:output.append(tuple(window))
    return output

def make_result_threshold(minimum: float) -> Callable[[Experiment],bool]:
    """Closure with an enclosed threshold."""
    def predicate(item: Experiment) -> bool:
        return item.result>=minimum
    return predicate

def pick_by_predicate(records: Iterable[Experiment], predicate: Callable[[Experiment],bool]) -> list[Experiment]:
    return [r for r in records if predicate(r)]
