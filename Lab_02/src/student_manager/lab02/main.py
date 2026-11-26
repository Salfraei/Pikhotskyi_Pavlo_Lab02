"""Lab 02 CLI (scientific experiments, variant 15)."""
from __future__ import annotations
import argparse
from student_manager.lab02.data import load_experiments,experiment_index,experiment_ids,experiment_tuple
from student_manager.lab02.analytics import summarize,averages_by_researcher,best_experiment,average_values,describe_experiment
from student_manager.lab02.processors import (
    filter_by_researcher,filter_by_range,group_by_researcher,sort_by_result,
    unique_parameters,result_index,count_parameters,sliding_ids,make_result_threshold,pick_by_predicate
)
from student_manager.lab02.decorators import timed
from student_manager.lab02.benchmark import compare_lookup

@timed
def demo()->None:
    records=load_experiments()
    print('Lab02 | scientific experiments | variant 15')
    print('list:',[r.id for r in records]);print('tuple:',experiment_tuple(records[0]))
    print('set:',sorted(experiment_ids(records)))
    print('dict index keys:',sorted(experiment_index(records)))
    print('list comprehension:',[e.result for e in records if e.result>20])
    print('set comprehension:',unique_parameters(records))
    print('dict comprehension:',result_index(records))
    print('Counter:',count_parameters(records))
    print('defaultdict grouping:',{k:len(v) for k,v in group_by_researcher(records).items()})
    print('deque sliding IDs:',sliding_ids(records))
    print('Researcher filter:',[x.id for x in filter_by_researcher(records,'Іваненко')])
    print('Result filter:',[x.id for x in filter_by_range(records,20,30)])
    print('Sorted:',[x.id for x in sort_by_result(records)])
    print('Aggregate:',summarize(records),'per researcher:',averages_by_researcher(records))
    print('Best:',best_experiment(records).id)
    print('*args average:',average_values(1,2,3))
    print('**kwargs record:',describe_experiment(**records[0].to_dict()))
    print('Closure:',[x.id for x in pick_by_predicate(records,make_result_threshold(20))])

def main()->None:
    parser=argparse.ArgumentParser(description='Lab02 collections and analytics, variant 15')
    parser.add_argument('--mode',choices=('demo','benchmark','all'),default='demo')
    args=parser.parse_args()
    if args.mode in ('demo','all'):demo()
    if args.mode in ('benchmark','all'):
        stats=compare_lookup(load_experiments(),4)
        for k,v in stats.items():print(k,'=',f'{v:.6f}')

if __name__=='__main__':main()
