'use strict';
(async function(){
  const status=document.getElementById('status');
  try{
    const [districts,daily,flight]=await Promise.all(['districts.geojson','daily_cases.json','response.czml'].map(f=>WV.fetchJSON('../data/'+f)));
    Cesium.Ion.defaultAccessToken='';
    const viewer=new Cesium.Viewer('globe',{baseLayer:false,baseLayerPicker:false,geocoder:false,homeButton:false,sceneModePicker:false,navigationHelpButton:true,navigationInstructionsInitiallyVisible:false,animation:true,timeline:true,infoBox:false,requestRenderMode:true,maximumRenderTimeChange:1});
    viewer.scene.globe.baseColor=Cesium.Color.fromCssColorString('#163c4b');
    Cesium.TileMapServiceImageryProvider.fromUrl(Cesium.buildModuleUrl('Assets/Textures/NaturalEarthII')).then(p=>viewer.imageryLayers.addImageryProvider(p)).catch(()=>{status.textContent='Imagery unavailable; showing ellipsoid with exercise layers.';});
    const source=await Cesium.GeoJsonDataSource.load(districts,{clampToGround:false});await viewer.dataSources.add(source);
    const route=await Cesium.CzmlDataSource.load(flight);await viewer.dataSources.add(route);viewer.clockTrackedDataSource=route;viewer.clock.shouldAnimate=false;viewer.timeline.zoomTo(route.clock.startTime,route.clock.stopTime);
    let current,selected='D07',imported;
    function details(id){selected=id;WV.showDetails(current.features.find(f=>f.id===id)||current.features[0]);}
    function update(){const day=Number(document.getElementById('day').value);document.getElementById('day-label').textContent=day;current=WV.atDay(districts,daily,day);for(const f of current.features){const entity=source.entities.getById(f.id),rate=f.properties.rate_per_100k;entity.polygon.height=0;entity.polygon.extrudedHeight=rate*5;entity.polygon.material=Cesium.Color.fromCssColorString(WV.color(rate)).withAlpha(.87);entity.polygon.outline=true;entity.polygon.outlineColor=Cesium.Color.fromCssColorString('#173449');}details(selected);viewer.scene.requestRender();}
    function frame(){viewer.flyTo(source,{duration:1,offset:new Cesium.HeadingPitchRange(Cesium.Math.toRadians(-25),Cesium.Math.toRadians(-40),75000)});}
    update();frame();WV.showLegend('rate_per_100k');
    for(const f of districts.features){const b=document.createElement('button');b.textContent=f.id;b.onclick=()=>details(f.id);document.getElementById('district-buttons').append(b);}
    viewer.selectedEntityChanged.addEventListener(entity=>{if(!entity)return;if(current.features.some(f=>f.id===entity.id))details(entity.id);else if(entity.properties)WV.showDetails({properties:entity.properties.getValue(viewer.clock.currentTime)},true);else document.getElementById('details').textContent='SIMULATED supply flight · illustrative ellipsoid altitude; use the timeline to animate.';});
    document.getElementById('day').oninput=update;document.getElementById('reset').onclick=frame;
    viewer.scene.morphComplete.addEventListener(()=>{document.querySelectorAll('[data-mode]').forEach(b=>b.disabled=false);frame();});
    document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-mode]').forEach(x=>{x.setAttribute('aria-pressed',String(x===b));x.disabled=true;});if(b.dataset.mode==='3D')viewer.scene.morphTo3D(1);else if(b.dataset.mode==='2D')viewer.scene.morphTo2D(1);else viewer.scene.morphToColumbusView(1);});
    document.getElementById('flight').onchange=e=>{route.show=e.target.checked;viewer.scene.requestRender();};
    document.getElementById('import').onchange=async e=>{try{const data=await WV.readImport(e.target.files[0]);const next=await Cesium.GeoJsonDataSource.load(data,{stroke:Cesium.Color.MEDIUMPURPLE,fill:Cesium.Color.MEDIUMPURPLE.withAlpha(.3),clampToGround:false});for(const entity of next.entities.values){if(entity.polygon){const raw=entity.properties?.height_m?.getValue();entity.polygon.height=0;entity.polygon.extrudedHeight=typeof raw==='number'&&Number.isFinite(raw)?Math.max(0,Math.min(100000,raw)):0;}}await viewer.dataSources.add(next);if(imported)viewer.dataSources.remove(imported,true);imported=next;viewer.flyTo(imported);status.textContent='IMPORTED '+data.features.length+' features · source claims unverified.';}catch(error){status.textContent='Import rejected: '+error.message;}};
    document.getElementById('clear-import').onclick=()=>{if(imported)viewer.dataSources.remove(imported,true);imported=null;document.getElementById('import').value='';status.textContent='Imported layer cleared.';viewer.scene.requestRender();};
    status.textContent='Scene ready · SYNTHETIC districts and flight · no terrain service.';window.sceneReady=true;
  }catch(error){status.textContent='3D unavailable: '+error.message+'. Open the 2D EOC or Lab 07 for the data and charts.';}
})();
