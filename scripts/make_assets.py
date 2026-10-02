"""Recreate original vector artwork and data-driven Matplotlib figures."""
from pathlib import Path
import json
import math
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'assets';ASSETS.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'content'))
from worldview_lab import load, wilson_interval

svg=['''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 690" role="img" aria-labelledby="title desc">
<title id="title">WorldView / JupyterLite — Geospatial field lab</title><desc id="desc">Original conceptual illustration connecting a globe, a district map, an epidemic curve and extruded columns. Learn to observe, calculate, explain and review. All illustrated marks are synthetic, not live intelligence.</desc>
<defs><radialGradient id="halo"><stop stop-color="#155263"/><stop offset="1" stop-color="#091722"/></radialGradient><linearGradient id="sphere" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#205361"/><stop offset="1" stop-color="#0a2433"/></linearGradient><clipPath id="clip"><circle cx="1110" cy="294" r="206"/></clipPath></defs>
<rect width="1440" height="690" rx="22" fill="#091722"/><ellipse cx="1060" cy="320" rx="400" ry="315" fill="url(#halo)"/>
<g font-family="Segoe UI,Arial,sans-serif"><text x="64" y="73" fill="#67dbd0" font-size="15" letter-spacing="4">THE GEOSPATIAL FIELD LAB</text>
<text x="60" y="158" fill="#f2f7f8" font-size="77" font-weight="700" letter-spacing="-3">WORLDVIEW</text><text x="64" y="210" fill="#a2b8c1" font-size="33" letter-spacing="8">× JUPYTERLITE</text>
<text x="64" y="291" fill="#e0edef" font-size="28">See the pattern.</text><text x="64" y="331" fill="#e0edef" font-size="28">Understand the evidence.</text>
<text x="64" y="387" fill="#91acb9" font-size="17">Emergency operations · Spatial epidemiology</text><text x="64" y="415" fill="#91acb9" font-size="17">Global health · GPT-6 Astra assisted analysis</text>
<rect x="64" y="464" width="181" height="34" rx="17" fill="#193c49"/><text x="83" y="487" fill="#67dbd0" font-size="13">11 EXECUTABLE LABS</text><rect x="258" y="464" width="173" height="34" rx="17" fill="#193c49"/><text x="277" y="487" fill="#67dbd0" font-size="13">2D + 3D + TIME</text>
<circle cx="1110" cy="294" r="207" fill="url(#sphere)" stroke="#44969b" stroke-width="1.5"/>
<g clip-path="url(#clip)" fill="none" stroke="#4b9e9f" stroke-opacity=".36">''']
for rx in [45,105,164,202]:svg.append(f'<ellipse cx="1110" cy="294" rx="{rx}" ry="206"/>')
for y,rx in [(140,135),(200,183),(260,203),(330,202),(390,182),(448,135)]:svg.append(f'<ellipse cx="1110" cy="{y}" rx="{rx}" ry="18"/>')
svg.append('''</g><path d="M956 195 Q1117 95 1268 344 M976 365 Q1075 500 1240 220" stroke="#f4bc65" stroke-width="2" stroke-dasharray="5 8" fill="none"/>
<g fill="#67dbd0" stroke="#b7ffed" stroke-width="2"><circle cx="976" cy="365" r="6"/><circle cx="1240" cy="220" r="6"/><circle cx="956" cy="195" r="6"/><circle cx="1268" cy="344" r="6"/></g>
<rect x="715" y="125" width="228" height="185" rx="10" fill="#102734" stroke="#37616e"/><text x="735" y="155" fill="#9cbac6" font-size="12" letter-spacing="2">COMPARE / PLACE</text>''')
for i,value in enumerate([0,1,0,2,1,2,1,0,1,0,0,1]):
    x,y=736+(i%4)*47,172+(i//4)*36
    svg.append(f'<rect x="{x}" y="{y}" width="40" height="29" rx="3" fill="{["#54c9c1","#f4bc65","#ef806f"][value]}" opacity=".83"/>')
svg.append('''<rect x="734" y="353" width="285" height="151" rx="10" fill="#102734" stroke="#37616e"/><text x="754" y="382" fill="#9cbac6" font-size="12" letter-spacing="2">INVESTIGATE / TIME</text>''')
for i,v in enumerate([9,15,24,31,46,63,75,66,54,34,20,12]):svg.append(f'<rect x="{755+i*20}" y="{479-v}" width="13" height="{v}" rx="2" fill="#67dbd0" opacity=".86"/>')
svg.append('<rect x="1148" y="416" width="214" height="116" rx="10" fill="#102734" stroke="#37616e"/>')
for x,h in [(1177,28),(1227,64),(1277,43)]:svg.append(f'<path d="M{x} 510 v-{h} l18 -10 18 10 v{h} l-18 10Z" fill="#a18acf"/><path d="M{x+18} {500-h} v{h+20} l18 -10 v-{h}Z" fill="#735d9d"/>')
svg.append('''<path d="M64 550 H1376" stroke="#2a4552"/><text x="64" y="599" fill="#67dbd0" font-size="17">01  OBSERVE</text><text x="353" y="599" fill="#67dbd0" font-size="17">02  CALCULATE</text><text x="689" y="599" fill="#67dbd0" font-size="17">03  EXPLAIN</text><text x="1020" y="599" fill="#67dbd0" font-size="17">04  REVIEW</text><text x="64" y="643" fill="#809daa" font-size="13">Inspired by World View · Kevin (Khoa) To · MIT</text><text x="1014" y="643" fill="#809daa" font-size="13">CONCEPTUAL / SYNTHETIC ARTWORK</text></g></svg>''')
(ASSETS/'worldview-splash.svg').write_text(''.join(svg),encoding='utf-8')

steps=[('01 / OBSERVE','2D + 3D views','Source · time · denominator'),('02 / CALCULATE','Python + GIS','Distances · rates · graphs'),('03 / EXPLAIN','Optional Astra','Evidence IDs · uncertainty'),('04 / REVIEW','Domain specialist','Verify · revise · hand off')]
diagram=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 230" role="img" aria-labelledby="t d"><title id="t">Evidence workflow</title><desc id="d">Maps and verified calculations support optional Astra explanations and human review. Evidence and provenance travel with each step.</desc><rect width="1200" height="230" rx="14" fill="#091722"/><g font-family="Segoe UI,Arial,sans-serif">']
for i,(a,b,c) in enumerate(steps):
    x=24+i*296
    diagram.append(f'<rect x="{x}" y="30" width="264" height="150" rx="10" fill="#112533" stroke="#294452"/><text x="{x+18}" y="63" fill="#67dbd0" font-size="14">{a}</text><text x="{x+18}" y="104" fill="#eff8fa" font-size="22">{b}</text><text x="{x+18}" y="142" fill="#a2b8c1" font-size="13">{c}</text>')
    if i<3:diagram.append(f'<path d="M{x+270} 99 h18 m-5 -5 5 5 -5 5" stroke="#67dbd0" fill="none"/>')
diagram.append('<text x="24" y="211" fill="#a2b8c1" font-size="13">Reproducible evidence → explicit assumptions → reviewable claims. No browser API keys; no autonomous dispatch.</text></g></svg>')
(ASSETS/'evidence-workflow.svg').write_text(''.join(diagram),encoding='utf-8')

plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','font.size':10})
features=load('districts.geojson')['features'];daily=load('daily_cases.json')
fig,axs=plt.subplots(1,3,figsize=(15,4.7),layout='constrained')
for f in features:
    p=f['properties'];rate=p['rate_per_100k'];color='#54c9c1' if rate<200 else '#f4bc65' if rate<400 else '#ef806f'
    axs[0].add_patch(Polygon(f['geometry']['coordinates'][0],facecolor=color,edgecolor='white',linewidth=2))
    axs[0].text(p['longitude'],p['latitude'],p['id'],ha='center',va='center',fontsize=9)
axs[0].autoscale();axs[0].set(xlabel='Longitude (degrees)',ylabel='Latitude (degrees)',title='Place / 14-day cases per 100k')
axs[0].ticklabel_format(useOffset=False);axs[0].text(.02,-.27,'Teal <200 · amber 200–399 · coral ≥400',transform=axs[0].transAxes,fontsize=9)
counts=[sum(r['cases'] for r in daily if int(r['onset_date'][-2:])==d) for d in range(1,15)]
axs[1].bar(range(1,15),counts,color='#168f98');axs[1].set(xlabel='September 2026 onset day',ylabel='New cases',title='Time / epidemic curve')
rates=[f['properties']['rate_per_100k'] for f in features];ci=[wilson_interval(f['properties']['cases'],f['properties']['population']) for f in features]
axs[2].errorbar(rates,[f['id'] for f in features],xerr=[[r-lo for r,(lo,hi) in zip(rates,ci)],[hi-r for r,(lo,hi) in zip(rates,ci)]],fmt='o',color='#168f98',capsize=2)
axs[2].set(xlabel='New cases per 100,000 residents',title='Uncertainty / Wilson 95% intervals')
fig.suptitle('SYNTHETIC EXERCISE  |  12 fictional districts · 14-day interval · independent binomial teaching assumption',fontsize=13)
fig.savefig(ASSETS/'outbreak-atlas.png',dpi=170);plt.close(fig)
print('Created original splash, workflow infographic, and outbreak atlas')
