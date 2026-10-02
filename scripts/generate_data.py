"""Rebuild deterministic teaching fixtures. No observations or patient records."""
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'content' / 'data'
DATA.mkdir(parents=True, exist_ok=True)

def write(name, value):
    (DATA / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')

districts = []
populations = [8000, 18000, 12500, 24000, 9000, 30000, 15000, 22000, 7000, 27000, 11000, 20000]
totals = [12, 27, 40, 32, 45, 48, 90, 66, 21, 54, 22, 20]
for i in range(12):
    col, row = i % 4, i // 4
    x, y = -77.30 + col * .13, 38.65 + row * .12
    population, cases = populations[i], totals[i]
    props = dict(id=f'D{i+1:02}', name=f'Exercise district {i+1:02}',
                 population=population, cases=cases, rate_per_100k=cases/population*100000,
                 reporting_fraction=[1.0, .85, .7][i % 3],
                 longitude=x+.065, latitude=y+.06, source='SYNTHETIC exercise v1',
                 observed_at='2026-09-14T12:00:00Z', status='SIMULATED',
                 height_m=round(cases/population*100000*5))
    districts.append(dict(type='Feature', id=props['id'], properties=props,
        geometry=dict(type='Polygon', coordinates=[[[x,y],[x+.12,y],[x+.12,y+.11],[x,y+.11],[x,y]]])))
write('districts.geojson', dict(type='FeatureCollection', features=districts))

facilities=[]
for ident, name, lon, lat, capacity, opened in [
    ('F01','Harbor exercise clinic',-77.23,38.71,70,True),
    ('F02','Central exercise hospital',-77.10,38.83,110,True),
    ('F03','Ridge exercise clinic',-76.84,38.95,55,True),
    ('F04','South exercise shelter',-76.91,38.71,90,False)]:
    facilities.append(dict(type='Feature', id=ident, geometry=dict(type='Point',coordinates=[lon,lat]),
        properties=dict(id=ident,name=name,capacity=capacity,open=opened,status='SIMULATED',
                        source='SYNTHETIC exercise v1',observed_at='2026-09-14T11:30:00Z')))
write('facilities.geojson',dict(type='FeatureCollection',features=facilities))

# Allocate each district's cases over onset days; preserve exact district totals.
daily=[]
weights=[1,1,2,3,5,8,12,16,14,10,7,5,3,2]
for f in districts:
    p=f['properties']; counts=[int(p['cases']*w/sum(weights)) for w in weights]
    remainder=p['cases']-sum(counts)
    for j in sorted(range(14),key=lambda j:-(p['cases']*weights[j]/sum(weights)-counts[j]))[:remainder]:counts[j]+=1
    for j,n in enumerate(counts):
        daily.append(dict(district=p['id'],onset_date=f'2026-09-{j+1:02}',cases=n,
                          reporting_delay_days=1+(j%4),status='SIMULATED'))
write('daily_cases.json',daily)
nodes={f['id']:[f['properties']['longitude'],f['properties']['latitude']] for f in districts}
edges=[]
for i in range(12):
    for j in [i+1,i+4]:
        if j<12 and (j==i+4 or i//4==j//4):
            edges.append(dict(a=f'D{i+1:02}',b=f'D{j+1:02}',minutes=8+(i+j)%8,
                              closed=(i,j) in [(5,6),(6,10),(2,6)]))
write('network.json',dict(nodes=nodes,edges=edges,facility_nodes={'F01':'D01','F02':'D06','F03':'D12','F04':'D04'},
                          source='SYNTHETIC undirected travel-time graph; no real roads'))
write('seismic_sample.geojson',dict(type='FeatureCollection',metadata=dict(title='SYNTHETIC fallback; not a USGS snapshot'),features=[
    dict(type='Feature',id=f'SIM-Q{i}',geometry=dict(type='Point',coordinates=[lon,lat,depth]),
         properties=dict(mag=mag,place=f'Synthetic training event {i}',time=1789387200000+i*3600000,url=None))
    for i,(lon,lat,depth,mag) in enumerate([(-77.1,38.8,8,4.5),(-76.8,38.95,15,3.2),(-77.3,38.7,5,None),(-77,38.9,12,0)])]))
interval='2026-09-14T12:00:00Z/2026-09-14T13:00:00Z'
write('response.czml',[
    dict(id='document',version='1.0',name='SIMULATED supply flight',clock=dict(interval=interval,currentTime=interval.split('/')[0],multiplier=30,range='LOOP_STOP')),
    dict(id='supply-1',name='SIMULATED supply flight — illustrative altitude',availability=interval,
         position=dict(epoch=interval.split('/')[0],cartographicDegrees=[0,-77.23,38.71,1000,900,-77.10,38.83,3500,1800,-76.97,38.90,3500,2700,-76.84,38.95,1000,3600,-76.84,38.95,1000],interpolationAlgorithm='LINEAR',interpolationDegree=1),
         point=dict(pixelSize=14,color=dict(rgba=[255,188,94,255])),
         path=dict(width=3,leadTime=0,trailTime=3600,material=dict(solidColor=dict(color=dict(rgba=[255,188,94,255])))))])
write('manifest.json',dict(version=1,generated_by='scripts/generate_data.py',license='MIT',
    classification='SYNTHETIC — no real districts, facilities, cases, flight or roads',
    scenario_clock='2026-09-14T12:00:00Z',crs='WGS 84 longitude, latitude (degrees)',
    population_definition='Fictional resident population, fixed over a 14-day interval',
    cases_definition='Fictional new cases by onset date, one per person, over 2026-09-01 through 2026-09-14',
    geography='Illustrative grid near Washington, DC; not administrative boundaries',
    caveats=['No operational or clinical use','Reporting fractions are invented sensitivity assumptions',
             '3D heights encode rates, not terrain or buildings','No personal or individual-level health data']))
print(f'Wrote {len(list(DATA.glob("*")))} fixtures to {DATA}')
