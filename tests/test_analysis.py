from pathlib import Path
import copy
import json
import math
import sys
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'content'))
sys.path.insert(0,str(ROOT/'tools'))
from worldview_lab import (haversine_km, wilson_interval, shortest_times, load,
    freshness, normalize_quakes, validate_geojson, validate_brief)
from astra_brief import prepare, parse_response

def test_distance_known_arc_antimeridian_and_identity():
    assert haversine_km(0,0,0,0)==0
    assert haversine_km(0,0,1,0)==pytest.approx(111.19508,rel=1e-6)
    assert haversine_km(179.5,0,-179.5,0)==pytest.approx(111.19508,rel=1e-6)
    assert haversine_km(0,0,180,0)==pytest.approx(math.pi*6371.0088)
    with pytest.raises(ValueError):haversine_km(181,0,0,0)

def test_wilson_published_example_and_boundaries():
    low,high=wilson_interval(20,100,scale=1)
    assert low==pytest.approx(.1333669,abs=1e-6)
    assert high==pytest.approx(.2888292,abs=1e-6)
    assert wilson_interval(0,100)[0]==0
    assert wilson_interval(100,100)[1]==100000
    with pytest.raises(ValueError):wilson_interval(2,1)
    with pytest.raises(ValueError):wilson_interval(0,0)

def test_graph_uses_indirect_route_and_preserves_unreachable():
    graph={'nodes':dict.fromkeys('ABCD'),'edges':[{'a':'A','b':'B','minutes':10},
        {'a':'A','b':'C','minutes':2},{'a':'C','b':'B','minutes':3,'closed':True}]}
    assert shortest_times(graph,'A',False)['B']==5
    assert shortest_times(graph,'A',True)['B']==10
    assert math.isinf(shortest_times(graph,'A')['D'])
    graph['edges'][0]['minutes']=-1
    with pytest.raises(ValueError):shortest_times(graph,'A')

def test_fixture_totals_and_coordinate_contract():
    districts=load('districts.geojson');daily=load('daily_cases.json')
    assert validate_geojson(districts)
    assert validate_geojson(load('facilities.geojson'))
    for f in districts['features']:
        p=f['properties'];assert sum(r['cases'] for r in daily if r['district']==f['id'])==p['cases']
        assert p['rate_per_100k']==pytest.approx(p['cases']/p['population']*100000)
    assert sum(f['properties']['cases'] for f in districts['features'])==477
    bad=copy.deepcopy(districts);bad['features'][0]['geometry']['coordinates'][0].pop()
    with pytest.raises(ValueError):validate_geojson(bad)

@pytest.mark.parametrize('observed,expected',[
    ('2026-09-14T11:30:00Z','CURRENT'),('2026-09-14T10:00:00Z','STALE'),('2026-09-14T13:00:00Z','FUTURE')])
def test_freshness_uses_observation_clock(observed,expected):
    assert freshness(observed,'2026-09-14T12:00:00Z')==expected

def test_feed_keeps_zero_missing_and_drops_invalid_coordinates():
    fixture=load('seismic_sample.geojson');records=normalize_quakes(fixture)
    assert [r['magnitude'] for r in records]==[4.5,3.2,0,None]
    fixture['features'][0]['geometry']=None
    assert len(normalize_quakes(fixture))==3

@pytest.fixture
def evidence():return {'classification':'SYNTHETIC EXERCISE','evidence':[{'id':'A','value':10,'unit':'cases'}]}

@pytest.fixture
def brief():return {'summary':'Synthetic training example.','evidence_ids':['A'],
    'limitations':['Not observations.'],'review_questions':['Verify the denominator.'],'requires_human_review':True}

def test_real_request_shape_without_credentials(evidence):
    request=prepare(evidence)
    assert request['model']=='gpt-6-astra' and request['store'] is False
    assert request['text']['format']['strict'] is True
    assert 'temperature' not in request
    assert json.loads(request['input'])==evidence
    with pytest.raises(ValueError):prepare(dict(evidence,classification='PRIVATE'))

def test_response_requires_review_known_ids_and_completed_status(evidence,brief):
    response={'status':'completed','output':[{'type':'message','content':[{'type':'output_text','text':json.dumps(brief)}]}]}
    assert parse_response(response,evidence)==brief
    with pytest.raises(ValueError):parse_response(dict(response,status='incomplete'),evidence)
    with pytest.raises(ValueError):parse_response({'status':'completed','output':[{'content':[{'type':'refusal'}]}]},evidence)
    with pytest.raises(ValueError):validate_brief(dict(brief,evidence_ids=['invented']),evidence)
    with pytest.raises(ValueError):validate_brief(dict(brief,requires_human_review=False),evidence)
    with pytest.raises(ValueError):validate_brief(dict(brief,summary=None),evidence)

def test_image_request_is_explicit_and_bounded(tmp_path,evidence):
    path=tmp_path/'map.png';path.write_bytes(b'fixture bytes')
    request=prepare(evidence,path)
    assert request['input'][0]['content'][1]['type']=='input_image'
    assert request['input'][0]['content'][1]['image_url'].startswith('data:image/png;base64,')
    other=tmp_path/'map.svg';other.write_text('<svg/>')
    with pytest.raises(ValueError):prepare(evidence,other)
