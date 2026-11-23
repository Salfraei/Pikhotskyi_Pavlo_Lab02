from collections import Counter
from math import isclose
import pytest
from student_manager.lab02.data import load_experiments,experiment_ids,experiment_index,experiment_tuple
from student_manager.lab02.processors import (
    find_by_id,filter_by_researcher,filter_by_range,group_by_researcher,
    sort_by_result,unique_parameters,result_index,count_parameters,sliding_ids,
    make_result_threshold,pick_by_predicate
)
from student_manager.lab02.analytics import (average_values,describe_experiment,
     summarize,averages_by_researcher,best_experiment)
from student_manager.lab02.decorators import timed
from student_manager.lab02.benchmark import compare_lookup

@pytest.fixture
def records():return load_experiments()

def test_types(records):
    assert isinstance(experiment_ids(records),set)
    assert isinstance(experiment_index(records),dict)
    assert isinstance(experiment_tuple(records[0]),tuple)

def test_lookup(records):
    assert find_by_id(records,1)==records[0]
    assert find_by_id(records,999) is None

def test_filtering(records):
    assert len(filter_by_researcher(records,'ІВАНЕНКО'))==2
    assert len(filter_by_range(records,20,30))==2
    with pytest.raises(ValueError):filter_by_range(records,2,1)

def test_grouping(records):
    assert len(group_by_researcher(records))==3
    assert unique_parameters(records)=={'temperature','voltage','resistance'}
    assert count_parameters(records)==Counter({'temperature':2,'voltage':1,'resistance':1})
    assert result_index(records)[2]==4.95

def test_sort(records):assert sort_by_result(records)[0].id==2

def test_deque(records):
    assert sliding_ids(records)==[(1,2),(2,3),(3,4)]
    with pytest.raises(ValueError):sliding_ids(records,0)

def test_closure(records):
    assert len(pick_by_predicate(records,make_result_threshold(20)))==3

def test_analytics(records):
    assert summarize(records)['count']==4
    assert averages_by_researcher(records)['Олена Іваненко']==pytest.approx(24.3)
    assert best_experiment(records).id==4
    assert average_values(1,2,3)==2
    assert average_values() is None

def test_kwargs(records):
    assert describe_experiment(**records[0].to_dict())['experiment_id']==1
    with pytest.raises(ValueError):describe_experiment(name='Invalid')

def test_decorator():
    @timed
    def fun(x):return x*2
    assert fun(2)==4
    assert fun.__name__=='fun'
    assert fun.last_elapsed>=0

def test_benchmark(records):
    stats=compare_lookup(records,2,repeats=2)
    assert stats['indexed_seconds']>=0
