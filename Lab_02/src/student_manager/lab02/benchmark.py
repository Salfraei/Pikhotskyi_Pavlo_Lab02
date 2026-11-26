"""Repeatable linear-versus-dictionary lookup timing."""
from __future__ import annotations
from timeit import repeat
from student_manager.models import Experiment
from student_manager.lab02.processors import find_by_id

def compare_lookup(records:list[Experiment], target_id:int,repeats:int=5)->dict[str,float]:
    index={r.experiment_id:r for r in records}
    linear=min(repeat(lambda:find_by_id(records,target_id),number=100,repeat=repeats))
    indexed=min(repeat(lambda:index.get(target_id),number=100,repeat=repeats))
    return {"linear_seconds":linear,"indexed_seconds":indexed,
            "speedup":linear/indexed if indexed else float('inf')}
