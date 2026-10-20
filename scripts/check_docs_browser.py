"""Exercise the generated site in Chromium; screenshots and evidence stay outside site/."""

from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
from threading import Thread
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
EVIDENCE = Path(os.environ.get('DOCS_EVIDENCE_DIR', '/tmp/ontoportal-docs-evidence'))
EVIDENCE.mkdir(parents=True, exist_ok=True)


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args: object) -> None:
        pass


server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(SITE)))
Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}/'
report: dict = {'requests': {}, 'storage': {}, 'errors': [], 'failed_requests': [], 'screenshots': []}


def snapshot(page, name: str) -> None:
    page.wait_for_timeout(450)
    path = EVIDENCE / f'{name}.png'
    page.screenshot(path=str(path), full_page=True)
    report['screenshots'].append(str(path))
    report['requests'][name] = sorted(set(page.evaluate('performance.getEntriesByType("resource").map(x => x.name)')))
    report['storage'][name] = page.evaluate('Object.fromEntries(Object.entries(localStorage))')


with sync_playwright() as playwright:
    executable = os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE')
    browser = playwright.chromium.launch(headless=True, executable_path=executable)
    context = browser.new_context(viewport={'width': 1365, 'height': 900}, device_scale_factor=1)
    page = context.new_page()
    page.on('pageerror', lambda error: report['errors'].append(str(error)))
    page.on('requestfailed', lambda request: report['failed_requests'].append({'url': request.url, 'failure': request.failure}))
    page.goto(base, wait_until='networkidle')
    # The outer host has zero height; inspect its rendered inner dialog.
    consent = page.locator('#__consent .md-consent__inner')
    consent.wait_for(state='visible')
    assert not page.locator('input[name="github"]').is_checked()
    assert page.locator('link[rel="icon"]').get_attribute('href').endswith('assets/images/favicon.png')
    assert page.locator('a.md-source[href="https://github.com/chris-day/ontoportal-api"]').count() >= 1
    assert not page.locator('footer').get_by_text('Made with').count()
    assert page.locator('a[href="#__consent"]').count() >= 1
    assert page.evaluate('async () => { let i = new Image(); i.src = document.querySelector("link[rel=icon]").href; await i.decode(); return i.naturalWidth > 0 && i.naturalHeight > 0 }')
    snapshot(page, 'desktop-before-consent')

    page.get_by_role('button', name='Reject').click()
    page.wait_for_load_state('networkidle')
    assert not consent.is_visible()
    snapshot(page, 'desktop-rejected')
    page.locator('a[href="#__consent"]').first.click()
    consent.wait_for(state='visible')
    assert not page.locator('input[name="github"]').is_checked()
    page.get_by_text('Manage settings').click()
    page.get_by_text('GitHub content', exact=True).click()
    assert page.locator('input[name="github"]').is_checked()
    page.get_by_role('button', name='Accept').click()
    page.wait_for_load_state('networkidle')
    assert not consent.is_visible()
    assert page.evaluate('JSON.parse(Object.entries(localStorage).find(([k]) => k.endsWith("__consent"))?.[1] || "{}").github')
    snapshot(page, 'desktop-accepted')
    page.locator('a[href="#__consent"]').first.click()
    consent.wait_for(state='visible')
    assert page.locator('input[name="github"]').is_checked()
    page.get_by_role('button', name='Reject').click()
    page.wait_for_load_state('networkidle')
    assert not page.evaluate('JSON.parse(Object.entries(localStorage).find(([k]) => k.endsWith("__consent"))?.[1] || "{}").github')
    snapshot(page, 'desktop-revoked')

    for source in ('index', 'Endpoint-Guides-Annotator', 'OpenAPI-Specification', 'Documentation-Maintenance'):
        page.goto(base + source + '.html', wait_until='networkidle')
        assert page.locator('article.md-content__inner h1').count() == 1, source
    page.goto(base, wait_until='networkidle')
    page.locator('[data-md-component="search"] button').first.click()
    # Zensical search renders its input and results inside a shadow root.
    page.evaluate('Array.from(document.querySelectorAll("*")).find(e => e.shadowRoot?.querySelector("input[type=text]"))?.shadowRoot.querySelector("input[type=text]").focus()')
    page.keyboard.type('recommender')
    page.wait_for_timeout(750)
    assert page.evaluate('Array.from(document.querySelectorAll("*")).find(e => e.shadowRoot?.querySelector("input[type=text]"))?.shadowRoot.textContent.includes("Endpoint Guide: Recommender")')

    mobile = browser.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    mobile_page = mobile.new_page()
    mobile_page.goto(base, wait_until='networkidle')
    snapshot(mobile_page, 'mobile-before-consent')
    assert mobile_page.locator('#__consent .md-consent__inner').is_visible()
    mobile.close()
    context.close()
    browser.close()

for state, urls in report['requests'].items():
    third_party = sorted({urlsplit(url).netloc for url in urls if urlsplit(url).netloc not in ('', urlsplit(base).netloc)})
    report.setdefault('third_party', {})[state] = third_party
    if state == 'desktop-accepted':
        assert set(third_party) <= {'api.github.com'}, f'unexpected request after consent: {third_party}'
    else:
        assert not third_party, f'unexpected third-party request in {state}: {third_party}'
assert not report['errors'], report['errors']
assert not [r for r in report['failed_requests'] if urlsplit(r['url']).netloc == urlsplit(base).netloc], report['failed_requests']
(EVIDENCE / 'browser-report.json').write_text(json.dumps(report, indent=2) + '\n')
server.shutdown()
print(f'Browser checks passed; evidence: {EVIDENCE}')
