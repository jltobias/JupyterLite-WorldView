/* Original teaching utilities, MIT. No external network or model calls here. */
(function(root){
  'use strict';
  const COLORS=['#54c9c1','#f4bc65','#ef806f'];
  function validateGeoJSON(data){
    if(!data||data.type!=='FeatureCollection'||!Array.isArray(data.features))throw Error('Expected a GeoJSON FeatureCollection.');
    if(data.features.length===0||data.features.length>2000)throw Error('Import 1–2,000 features.');
    let count=0;
    for(const f of data.features){
      if(f.type!=='Feature'||!f.geometry||!f.properties)throw Error('Each feature needs geometry and properties.');
      for(const field of ['name','source','status','observed_at'])if(typeof f.properties[field]!=='string'||!f.properties[field].trim())throw Error('Missing text property: '+field);
      const g=f.geometry;let positions;
      if(g.type==='Point')positions=[g.coordinates];
      else if(g.type==='Polygon'&&Array.isArray(g.coordinates)&&g.coordinates.length){positions=[];for(const ring of g.coordinates){if(!Array.isArray(ring)||ring.length<4||JSON.stringify(ring[0])!==JSON.stringify(ring[ring.length-1]))throw Error('Polygon rings must be closed with at least four positions.');if(ring.length>100000)throw Error('Too many positions.');positions.push(...ring);}}
      else throw Error('This lab supports Point and Polygon geometry only.');
      for(const pos of positions){count++;if(!Array.isArray(pos)||pos.length<2||!pos.every(Number.isFinite)||Math.abs(pos[0])>180||Math.abs(pos[1])>90)throw Error('Invalid longitude/latitude coordinate.');if(count>100000)throw Error('Geometry exceeds 100,000 positions.');}
    }return data;
  }
  async function fetchJSON(url){const r=await fetch(url);if(!r.ok)throw Error('HTTP '+r.status+' loading '+url);return r.json();}
  function atDay(districts,daily,day){const totals={};for(const r of daily)if(Number(r.onset_date.slice(-2))<=day)totals[r.district]=(totals[r.district]||0)+r.cases;return {...districts,features:districts.features.map(f=>({...f,properties:{...f.properties,cases:totals[f.id]||0,rate_per_100k:(totals[f.id]||0)/f.properties.population*100000,height_m:(totals[f.id]||0)/f.properties.population*500000,day}}))};}
  function color(value,metric='rate_per_100k'){const b=metric==='cases'?[25,60]:metric==='reporting_fraction'?[.8,.95]:[200,400];return metric==='reporting_fraction'?(value<b[0]?COLORS[2]:value<b[1]?COLORS[1]:COLORS[0]):value<b[0]?COLORS[0]:value<b[1]?COLORS[1]:COLORS[2];}
  function legend(metric){return metric==='cases'?['<25 cases','25–59 cases','≥60 cases']:metric==='reporting_fraction'?['≥95% assumed','80–94% assumed','<80% assumed']:['<200 per 100k','200–399 per 100k','≥400 per 100k'];}
  function showLegend(metric){const el=document.getElementById('legend');el.replaceChildren();legend(metric).forEach((text,i)=>{const span=document.createElement('span');span.textContent=text;span.style.setProperty('--swatch',COLORS[i]);el.append(span);});}
  function showDetails(feature,imported=false){document.getElementById('details').textContent=(imported?'IMPORTED — source claims unverified\n':'SYNTHETIC exercise\n')+JSON.stringify(feature.properties,null,2);}
  function summary(data){const rows=data.features.map(f=>f.properties);const cases=rows.reduce((s,r)=>s+r.cases,0),population=rows.reduce((s,r)=>s+r.population,0);return {cases,population,rate:cases/population*100000};}
  function download(name,value){const blob=new Blob([JSON.stringify(value,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  async function readImport(file){if(!file)throw Error('Choose a GeoJSON file.');if(file.size>2*1024*1024)throw Error('File limit: 2 MB.');return validateGeoJSON(JSON.parse(await file.text()));}
  root.WV={COLORS,validateGeoJSON,fetchJSON,atDay,color,legend,showLegend,showDetails,summary,download,readImport};
})(globalThis);
