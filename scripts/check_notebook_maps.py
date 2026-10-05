"""Browser regressions for the actual notebook renderer, without live tile traffic."""
from pathlib import Path
import copy
import sys
from unittest.mock import patch
from urllib.parse import urlsplit
from playwright.sync_api import expect

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'content'))
from worldview_lab import load, map_layer

TILE = '''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256">
<rect width="256" height="256" fill="#e5edf0"/>
<path d="M0 128H256M128 0V256" stroke="#bacbd3"/>
<text x="12" y="28" fill="#526675" font-size="14">TEST TILE</text></svg>'''


def mock_tiles(context):
    """Intercept at context level, including notebook iframe requests."""
    state = {'failed': False, 'requests': []}

    def respond(route):
        state['requests'].append(route.request.headers)
        if state['failed']:
            route.fulfill(status=403, body='Test: access blocked')
        else:
            route.fulfill(content_type='image/svg+xml', body=TILE)

    context.route('https://tile.openstreetmap.org/**', respond)
    context.route('https://*.basemaps.cartocdn.com/**',
                  lambda r: r.fulfill(content_type='image/svg+xml', body=TILE))
    return state


def assert_tile_referrers(state, base):
    origin = urlsplit(base)
    expected = f'{origin.scheme}://{origin.netloc}/'
    assert state['requests'], 'The map made no tile requests'
    assert all(r.get('referer') == expected for r in state['requests']), state['requests']


def check_notebook_maps(browser, base, artifacts):
    context = browser.new_context(viewport={'width':1000, 'height':650})
    state = mock_tiles(context)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    sites = load('facilities.geojson')

    def show(collection=sites, **kwargs):
        with patch('IPython.display.display') as display:
            map_layer(collection, value='capacity', **kwargs)
        markup = display.call_args.args[0]['text/html']
        context.route(base + '/map-regression.html', lambda r: r.fulfill(
            content_type='text/html', body='<!doctype html><meta charset="utf-8">' + markup))
        page.goto(base + '/map-regression.html')
        frame = page.frame_locator('iframe')
        expect(frame.locator('.leaflet-overlay-pane path')).to_have_count(4, timeout=30000)
        return frame

    frame = show()
    expect(frame.locator('#map-status')).to_have_text('Data layer and OpenStreetMap background ready.')
    assert_tile_referrers(state, base)
    expect(frame.locator('.leaflet-control-attribution')).to_contain_text('OpenStreetMap contributors')
    page.screenshot(path=str(artifacts / 'notebook-map.png'), animations='disabled')

    frame.locator('#basemap').uncheck()
    expect(frame.locator('.leaflet-tile-pane img')).to_have_count(0)
    expect(frame.locator('#map-status')).to_contain_text('Background map off')
    state['failed'] = True
    frame = show()
    expect(frame.locator('#map-status')).to_contain_text('Background map unavailable')
    expect(frame.locator('#basemap')).not_to_be_checked()
    expect(frame.locator('.leaflet-tile-pane img')).to_have_count(0)
    expect(frame.locator('.leaflet-overlay-pane path')).to_have_count(4)
    frame.locator('.leaflet-overlay-pane path').first.click()
    expect(frame.locator('.leaflet-popup-content')).to_contain_text(sites['features'][0]['properties']['name'])
    page.screenshot(path=str(artifacts / 'notebook-map-outage.png'), animations='disabled')
    state['failed'] = False
    frame.locator('#basemap').check()
    expect(frame.locator('#map-status')).to_have_text('Data layer and OpenStreetMap background ready.')

    # Labels and GeoJSON must remain inert even though authored JS is trusted.
    malicious = copy.deepcopy(sites)
    label = '</script><script>window.injected=true</script><img src=x onerror="window.injected=true"> FIELD $payload'
    malicious['features'][0]['properties']['name'] = label
    requests_before = len(state['requests'])
    frame = show(malicious, title=label, basemap=False)
    expect(frame.locator('header')).to_contain_text(label)
    frame.locator('.leaflet-overlay-pane path').first.click()
    expect(frame.locator('.leaflet-popup-content pre')).to_contain_text('FIELD $payload')
    assert frame.locator('body').evaluate('(body) => window.injected') is None
    expect(frame.locator('header img, .leaflet-popup-content img')).to_have_count(0)
    assert len(state['requests']) == requests_before, 'basemap=False requested tiles'
    assert not errors, errors
    context.close()
    print('PASS notebook maps: real Referer, attribution, 403 fallback, retry, data-only, escaped labels', flush=True)
