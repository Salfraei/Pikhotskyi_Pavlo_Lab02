from dataclasses import replace
import pytest
from student_manager.main import demo_experiments
from student_manager.analytics import standard_deviation, statistics_by_parameter, find_extreme_experiments
from student_manager.repositories import InMemoryExperimentRepository
from student_manager.services import DuplicateExperimentError

def test_standard_deviation():
    assert standard_deviation([]) is None
    assert standard_deviation(demo_experiments())>0

def test_parameter_statistics():
    data=statistics_by_parameter(demo_experiments())
    assert data['temperature']['count']==2
    assert data['temperature']['average']==pytest.approx(24.3)

def test_extremes():
    assert find_extreme_experiments([])==(None,None)
    low,high=find_extreme_experiments(demo_experiments())
    assert low.id==2 and high.id==4

def test_repository_crud():
    sample=demo_experiments()[0]
    repo=InMemoryExperimentRepository()
    assert repo.get_by_id(sample.id) is None
    repo.add(sample)
    with pytest.raises(DuplicateExperimentError):repo.add(sample)
    new=replace(sample,result=100)
    assert repo.update(new).result==100
    assert repo.get_all()==[new]
    assert repo.delete(sample.id) is True
    assert repo.delete(sample.id) is False
    with pytest.raises(KeyError):repo.update(sample)
