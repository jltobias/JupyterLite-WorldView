'use strict';
(async function(){
  const status=document.getElementById('status');
  try{
    const [districts,daily,facilities]=await Promise.all(['districts.geojson','daily_cases.json','facilities.geojson'].map(f=>WV.fetchJSON('../data/'+f)));
    const map=L.map('map').setView([38.84,-77.03],10);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>'}).addTo(map);
    let districtLayer,imported,current,selected='D07';
    const facilityLayer=L.geoJSON(facilities,{pointToLayer:(f,ll)=>L.circleMarker(ll,{radius:7,color:f.properties.open?'#fff':'#555',fillColor:'#102936',fillOpacity:1,weight:3}),onEachFeature:(f,l)=>l.on('click',()=>WV.showDetails(f))}).addTo(map);
    function choose(f){selected=f.id;WV.showDetails(f);}
    function update(){
      const day=Number(document.getElementById('day').value),metric=document.getElementById('metric').value;
      document.getElementById('day-label').textContent=day;current=WV.atDay(districts,daily,day);
      if(districtLayer)map.removeLayer(districtLayer);
      districtLayer=L.geoJSON(current,{style:f=>({fillColor:WV.color(f.properties[metric],metric),fillOpacity:.65,color:'#15364a',weight:2}),onEachFeature:(f,l)=>{l.bindTooltip(f.properties.id+': '+f.properties[metric].toFixed(1));l.on('click',()=>choose(f));}}).addTo(map);
      facilityLayer.bringToFront();if(imported)imported.bringToFront();const s=WV.summary(current);
      for(const [id,value] of Object.entries({cases:s.cases.toLocaleString(),population:s.population.toLocaleString(),rate:s.rate.toFixed(1)}))document.getElementById(id).textContent=value;
      WV.showLegend(metric);choose(current.features.find(f=>f.id===selected)||current.features[0]);const tbody=document.getElementById('rows');tbody.replaceChildren();
      for(const f of current.features){const tr=document.createElement('tr'),p=f.properties;for(const val of [p.id,p.cases,p.population,p.rate_per_100k.toFixed(1)]){const td=document.createElement('td');td.textContent=val;tr.append(td);}const td=document.createElement('td'),button=document.createElement('button');button.textContent='View '+p.id;button.onclick=()=>choose(f);td.append(button);tr.append(td);tbody.append(tr);}
      const counts=Array.from({length:14},(_,i)=>daily.filter(r=>Number(r.onset_date.slice(-2))===i+1).reduce((s,r)=>s+r.cases,0)),max=Math.max(...counts,1);
      document.getElementById('curve').innerHTML='<text x="0" y="12">'+max+' cases</text>'+counts.map((n,i)=>`<rect x="${35+i*34}" y="${125-n/max*100}" width="23" height="${n/max*100}" fill="${i<day?'#67dbd0':'#405766'}"><title>Sep ${i+1}: ${n} new cases</title></rect><text x="${39+i*34}" y="145">${i+1}</text>`).join('');
    }
    update();map.fitBounds(districtLayer.getBounds());status.textContent='Scenario loaded · all exercise layers are SYNTHETIC.';
    document.getElementById('day').oninput=update;document.getElementById('metric').onchange=update;
    document.getElementById('facilities').onchange=e=>e.target.checked?facilityLayer.addTo(map):map.removeLayer(facilityLayer);
    document.getElementById('reset').onclick=()=>map.fitBounds(districtLayer.getBounds());document.getElementById('export').onclick=()=>WV.download('exercise-day-'+document.getElementById('day').value+'.geojson',current);
    document.getElementById('import').onchange=async e=>{try{const data=await WV.readImport(e.target.files[0]);const next=L.geoJSON(data,{style:{color:'#c2a6ff',weight:3,fillOpacity:.18},pointToLayer:(f,ll)=>L.circleMarker(ll,{color:'#9f6ee4',radius:9}),onEachFeature:(f,l)=>l.on('click',()=>WV.showDetails(f,true))});if(imported)map.removeLayer(imported);imported=next.addTo(map);map.fitBounds(imported.getBounds());status.textContent='IMPORTED '+data.features.length+' features · source claims unverified.';}catch(error){status.textContent='Import rejected: '+error.message;}};
    document.getElementById('clear-import').onclick=()=>{if(imported)map.removeLayer(imported);imported=null;document.getElementById('import').value='';status.textContent='Imported layer cleared.';update();};window.eocReady=true;
  }catch(error){status.textContent='Map unavailable: '+error.message+'. Run the notebooks for local tables and figures.';}
})();
