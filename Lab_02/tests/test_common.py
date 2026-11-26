import json
import pytest
from student_manager.models import Experiment, Researcher
from student_manager.main import demo_experiments
from student_manager.services import (
    DuplicateExperimentError, ExperimentService, add_experiment,
    calculate_average, calculate_statistics, find_experiment_by_id,
    find_experiments_by_researcher, filter_by_result_range,
    maximum_result, minimum_result, sort_experiments_by_date, group_by_researcher,
)
from student_manager.readers import read_experiments_csv, export_experiments_json

@pytest.fixture
def experiments():
    return demo_experiments()

@pytest.mark.parametrize("invalid", [0,-1,1.5, True])
def test_bad_id(invalid):
    with pytest.raises(ValueError):
        Experiment(invalid,"Name","Researcher","temp",1.0,"2026-10-10")

@pytest.mark.parametrize("field",["name","researcher","parameter"])
def test_empty_required(field):
    kwargs={"experiment_id":1,"name":"A","researcher":"R","parameter":"p","result":1.0,"date":"2026-10-10"}
    kwargs[field]=" "
    with pytest.raises(ValueError):
        Experiment(**kwargs)

@pytest.mark.parametrize("result", [float("nan"),float("inf"),float("-inf"),"abc"])
def test_invalid_result(result):
    with pytest.raises(ValueError):
        Experiment(1,"N","R","p",result,"2026-10-10")

def test_date_invalid():
    with pytest.raises(ValueError):
        Experiment(1,"N","R","p",1,"bad")

def test_researcher():
    assert Researcher(1," Anna ").name == "Anna"

def test_duplicate(experiments):
    with pytest.raises(DuplicateExperimentError):
        add_experiment(experiments,experiments[0])

def test_service(experiments):
    service=ExperimentService(experiments)
    assert len(service.list_all()) == 4
    assert service.get(2).parameter == "voltage"
    assert len(service.by_researcher("іваненко")) == 2
    assert service.in_range(0,5)[0].experiment_id == 2

def test_search(experiments):
    assert find_experiment_by_id(experiments,3).result == 25.2
    assert find_experiment_by_id(experiments,999) is None
    assert len(find_experiments_by_researcher(experiments,"ІВАНЕНКО")) == 2
    assert find_experiments_by_researcher(experiments,"") == []

def test_filter(experiments):
    assert [e.id for e in filter_by_result_range(experiments,20,30)] == [1,3]
    with pytest.raises(ValueError):filter_by_result_range(experiments,10,9)

def test_statistics(experiments):
    assert calculate_average(experiments) == pytest.approx(sum(e.result for e in experiments)/4)
    stats=calculate_statistics(experiments)
    assert stats.count==4 and stats.minimum == pytest.approx(4.95)
    assert maximum_result(experiments) == pytest.approx(101.5)
    assert minimum_result(experiments) == pytest.approx(4.95)
    assert calculate_statistics([]).average is None
    assert calculate_average([]) is None

def test_ordering(experiments):
    assert sort_experiments_by_date(experiments,True)[0].id==4
    assert len(group_by_researcher(experiments))==3

def test_csv_json(tmp_path,experiments):
    import csv
    path=tmp_path/"experiments.csv"
    with path.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=experiments[0].to_dict().keys());writer.writeheader()
        writer.writerows([e.to_dict() for e in experiments])
    assert list(read_experiments_csv(path))==experiments
    dest=tmp_path/"output.json"
    export_experiments_json(experiments,dest)
    assert len(json.loads(dest.read_text(encoding="utf-8")))==4

def test_csv_invalid_header(tmp_path):
    path=tmp_path/"wrong.csv";path.write_text("student_id,grade\n1,90\n",encoding="utf-8")
    with pytest.raises(ValueError):list(read_experiments_csv(path))
