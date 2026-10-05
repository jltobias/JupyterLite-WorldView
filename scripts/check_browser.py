"""Browser integration checks against a locally served GitHub Pages subpath."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import threading
from playwright.sync_api import sync_playwright, expect
from check_notebook_maps import check_notebook_maps, mock_tiles, assert_tile_referrers

ROOT=Path(__file__).resolve().parents[1];PREFIX='/JupyterLite-WorldView'

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT/'dist'),**kwargs)
    def do_GET(self):
        if self.path.startswith(PREFIX+'/'):self.path=self.path[len(PREFIX):]
        super().do_GET()
    def log_message(self,*args):pass

def main():
    artifacts=ROOT/'artifacts';artifacts.mkdir(exist_ok=True)
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}{PREFIX}'
    try:
        with sync_playwright() as p:
            installed=next((str(x) for x in [Path('C:/Program Files/Google/Chrome/Application/chrome.exe'),Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')] if x.exists()),None)
            opts={'headless':True,'args':['--use-angle=swiftshader','--enable-unsafe-swiftshader']}
            if installed:opts['executable_path']=installed
            browser=p.chromium.launch(**opts)
            check_notebook_maps(browser,base,artifacts)
            page=browser.new_page(viewport={'width':1440,'height':1100});errors=[]
            mock_tiles(page.context)
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(base+'/',wait_until='networkidle');page.screenshot(path=str(artifacts/'landing.png'),full_page=True)
            assert page.locator('h1').inner_text().startswith('See the pattern.')
            # Deterministic coverage of live-feed success and failure states.
            feed='https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson'
            page.route(feed,lambda route:route.fulfill(path=str(ROOT/'content/data/seismic_sample.geojson'),content_type='application/json'))
            page.route('https://api.wheretheiss.at/**',lambda route:route.fulfill(json={'latitude':38.8,'longitude':-77.1,'timestamp':1789387200}))
            page.goto(base+'/dashboard/')
            expect(page.locator('#qcount')).to_have_text('4',timeout=30000)
            assert 'Magnitude unknown' in page.evaluate('layers.quakes.getLayers()[2].getPopup().getContent()')
            page.route(feed,lambda route:route.fulfill(status=503,body='Test outage'))
            page.evaluate('loadQuakes()');expect(page.locator('#qcount')).to_have_text('UNAVAILABLE')
            assert page.evaluate('layers.quakes.getLayers().length')==0
            page.goto(base+'/dashboard/operations.html');page.wait_for_function('window.eocReady === true',timeout=60000)
            expect(page.locator('#cases')).to_have_text('477')
            expect(page.locator('#rows tr')).to_have_count(12)
            page.locator('#metric').select_option('cases');expect(page.locator('#legend')).to_contain_text('25–59 cases')
            page.locator('#day').fill('1');page.locator('#day').dispatch_event('input');assert int(page.locator('#cases').inner_text())<477
            page.locator('#day').fill('14');page.locator('#day').dispatch_event('input')
            page.locator('#metric').select_option('rate_per_100k')
            page.get_by_role('button',name='View D07',exact=True).click();expect(page.locator('#details')).to_contain_text('600')
            with page.expect_download() as info:page.locator('#export').click()
            info.value.save_as(artifacts/'export.geojson');exported=json.loads((artifacts/'export.geojson').read_text())
            assert len(exported['features'])==12
            assert all(abs(f['properties']['height_m']-f['properties']['rate_per_100k']*5)<1e-6 for f in exported['features'])
            page.locator('#import').set_input_files(str(ROOT/'content/data/facilities.geojson'));expect(page.locator('#status')).to_contain_text('IMPORTED 4')
            page.locator('#clear-import').click();expect(page.locator('#status')).to_contain_text('cleared')
            page.locator('#import').set_input_files({'name':'invalid.geojson','mimeType':'application/json','buffer':b'{"type":"FeatureCollection","features":[]}'});expect(page.locator('#status')).to_contain_text('Import rejected')
            page.locator('#clear-import').click();page.locator('#reset').click()
            page.locator('.tablewrap').evaluate('(el)=>el.scrollTop=0')
            page.screenshot(path=str(artifacts/'eoc-desktop.png'),full_page=True)
            page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(artifacts/'eoc-mobile.png'),full_page=True)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            page.set_viewport_size({'width':1440,'height':1100})
            page.goto(base+'/scenes/');page.wait_for_function('window.sceneReady === true',timeout=90000)
            expect(page.locator('#status')).to_contain_text('Scene ready')
            expect(page.locator('#district-buttons button')).to_have_count(12)
            page.locator('#district-buttons').get_by_role('button',name='D07',exact=True).click();expect(page.locator('#details')).to_contain_text('600')
            page.locator('[data-mode="2D"]').click();expect(page.locator('[data-mode="2D"]')).to_have_attribute('aria-pressed','true')
            page.locator('[data-mode="3D"]').click()
            page.locator('#day').fill('3');page.locator('#day').dispatch_event('input');expect(page.locator('#day-label')).to_have_text('3')
            page.locator('#day').fill('14');page.locator('#day').dispatch_event('input')
            page.locator('#flight').uncheck();page.locator('#flight').check()
            page.locator('#import').set_input_files(str(ROOT/'content/data/districts.geojson'));expect(page.locator('#status')).to_contain_text('IMPORTED 12',timeout=30000)
            page.locator('#clear-import').click();page.locator('#reset').click();page.wait_for_timeout(1500)
            page.screenshot(path=str(artifacts/'scene-desktop.png'),full_page=True)
            page.goto(base+'/book/intro.html');expect(page.locator('article h1')).to_contain_text('Geospatial Field Lab')
            page.goto(base+'/book/labs/05_spatial_epidemiology.html');expect(page.locator('article h1')).to_contain_text('Outbreak investigation')
            assert page.locator('img').count()>0
            # Execute real Pyodide notebooks, including notebook 03's map regression.
            # A fresh context prevents saved user files from hiding build defects.
            for filename,export_name in [('00_start_here.ipynb','districts.geojson'),('03_build_your_own_layer.ipynb','my-facilities.geojson'),('05_spatial_epidemiology.ipynb','outbreak.geojson')]:
                lite=browser.new_page(viewport={'width':1440,'height':1000})
                tile_state=mock_tiles(lite.context)
                lite.on('pageerror',lambda e:errors.append(str(e)))
                lite.goto(base+'/lab/index.html?path='+filename)
                lite.get_by_text('Python (Pyodide) | Idle',exact=True).wait_for(timeout=90000)
                lite.get_by_role('menuitem',name='Run',exact=True).click()
                lite.get_by_role('menuitem',name='Run All Cells',exact=True).click()
                lite.get_by_text('Python (Pyodide) | Busy',exact=True).wait_for(timeout=30000)
                lite.get_by_text('Python (Pyodide) | Idle',exact=True).wait_for(timeout=240000)
                # Notebook cells are virtualized; verify the newly written file
                # in the browser filesystem instead of an off-screen output.
                lite.get_by_text('exports',exact=True).dblclick(timeout=30000)
                lite.get_by_text(export_name,exact=True).wait_for(timeout=30000)
                assert lite.locator('.jp-OutputArea-error').count()==0
                if filename.startswith('03_'):
                    # Bring the virtualized map output into view before inspecting it.
                    frame=lite.frame_locator('iframe[title^="SYNTHETIC facilities"]')
                    lite.locator('iframe[title^="SYNTHETIC facilities"]').scroll_into_view_if_needed()
                    expect(frame.locator('#map-status')).to_have_text('Data layer and OpenStreetMap background ready.',timeout=30000)
                    expect(frame.locator('.leaflet-overlay-pane path')).to_have_count(4)
                    assert_tile_referrers(tile_state,base)
                lite.screenshot(path=str(artifacts/(filename+'.png')),full_page=True)
                print('PASS Pyodide:',filename,flush=True)
                lite.close()
            # No page JS exceptions are accepted; network errors are tested separately by the apps.
            assert not errors,errors
            browser.close();print('PASS browser: subpath, controls, tables, downloads, imports, 3D, book, mobile layout, Pyodide')
    finally:server.shutdown();server.server_close()

if __name__=='__main__':main()
