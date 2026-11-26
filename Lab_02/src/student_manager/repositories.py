"""In-memory repository contract; database implementation appears in Lab07."""
from __future__ import annotations
from collections.abc import Iterable
from student_manager.models import Experiment
from student_manager.services import DuplicateExperimentError

class InMemoryExperimentRepository:
    def __init__(self,items:Iterable[Experiment]=()):
        self._by_id:dict[int,Experiment]={}
        for item in items:self.add(item)

    def add(self,item:Experiment)->Experiment:
        if item.id in self._by_id:raise DuplicateExperimentError(str(item.id))
        self._by_id[item.id]=item
        return item

    def get_by_id(self,experiment_id:int)->Experiment|None:
        return self._by_id.get(experiment_id)

    def get_all(self)->list[Experiment]:
        return list(self._by_id.values())

    def update(self,item:Experiment)->Experiment:
        if item.id not in self._by_id:raise KeyError(item.id)
        self._by_id[item.id]=item
        return item

    def delete(self,experiment_id:int)->bool:
        return self._by_id.pop(experiment_id,None) is not None
