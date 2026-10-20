"""Check the built Zensical site and migration coverage with the standard library."""

from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import tomllib
from urllib.parse import unquote, urlsplit
import hashlib

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DOCS = ROOT / "docs"
CONFIG = tomllib.loads((ROOT / "zensical.toml").read_text())['project']
MANIFEST = json.loads((ROOT / "migration-manifest.json").read_text())
ERRORS: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def nav_paths(entries: list) -> list[str]:
    result: list[str] = []
    for entry in entries:
        if isinstance(entry, str):
            result.append(entry)
        else:
            for child in entry.values():
                result.extend(nav_paths(child if isinstance(child, list) else [child]))
    return result


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get('id'):
            self.ids.add(values['id'])
        for key in ('href', 'src'):
            if values.get(key):
                self.refs.append(values[key])


sources = {p.name for p in DOCS.glob('*.md')}
navigation = nav_paths(CONFIG['nav'])
llm_sections = CONFIG['plugins']['llmstxt']['sections']
llm_sources = [p for group in llm_sections.values() for p in group]
for label, paths in [('navigation', navigation), ('LLM sections', llm_sources)]:
    counts = Counter(paths)
    check(set(paths) == sources, f'{label}: missing {sorted(sources - set(paths))}, extra {sorted(set(paths) - sources)}')
    check(all(n == 1 for n in counts.values()), f'{label}: duplicate pages {sorted(p for p, n in counts.items() if n != 1)}')

pages: dict[Path, Page] = {}
for source in sources:
    html = SITE / (Path(source).stem + '.html')
    check(html.is_file(), f'missing rendered page: {html}')
    if html.is_file():
        page = Page()
        page.feed(html.read_text())
        pages[html] = page

for html, page in pages.items():
    for ref in page.refs:
        uri = urlsplit(ref)
        if uri.scheme or uri.netloc or ref.startswith('//'):
            continue
        target = (html.parent / unquote(uri.path)).resolve() if uri.path else html
        if target.is_dir():
            target /= 'index.html'
        check(target.is_relative_to(SITE.resolve()) and target.is_file(), f'{html.name}: missing {ref}')
        if uri.fragment and target.suffix == '.html' and target in pages:
            check(unquote(uri.fragment) in pages[target].ids, f'{html.name}: missing anchor {ref}')

llms = SITE / 'llms.txt'
check(llms.is_file(), 'llms.txt missing')
if llms.is_file():
    data = llms.read_text()
    links = re.findall(r'\]\(<([^>]+)>\)', data)
    base = CONFIG['site_url'].rstrip('/') + '/'
    check(len(links) == len(llm_sources), 'llms.txt has wrong number of links')
    check(set(links) == {base + s for s in llm_sources}, 'llms.txt links do not match source pages and site_url')
    for name in llm_sources:
        check((SITE / name).is_file(), f'Markdown export missing: {name}')
    for section in llm_sections:
        check('## ' + section in data, f'llms.txt section missing: {section}')
check((SITE / 'llms-full.txt').is_file(), 'llms-full.txt missing')
check((SITE / 'assets/images/favicon.png').read_bytes() == (DOCS / 'assets/images/favicon.png').read_bytes(), 'favicon differs in build')

for record in MANIFEST['sources']:
    src = Path(record['source'])
    external = src.is_absolute()
    if not src.is_absolute():
        src = ROOT / src
    # CI has only this repository, not the separate Wiki or supplied favicon.
    if not external and record['disposition'] not in ('exclude',):
        check(src.is_file(), f'migration source missing: {src}')
    if src.is_file() and record['disposition'] == 'exclude':
        check(hashlib.sha256(src.read_bytes()).hexdigest() == record['sha256'], f'excluded file changed: {src}')
    destination = record['destination']
    if destination and record['disposition'] not in ('legacy-config', 'exclude'):
        check((ROOT / destination).is_file(), f'migration destination missing: {destination}')

for path in SITE.rglob('*'):
    if path.is_file() and path.suffix in ('.html', '.md', '.txt', '.json'):
        data = path.read_text(errors='replace')
        check('codex resume' not in data and '/var/software/gitrepos/' not in data, f'sensitive local text in {path}')
check(not (SITE / 'helper.txt').exists(), 'excluded helper.txt appears in site')

if ERRORS:
    print('\n'.join('ERROR: ' + message for message in ERRORS), file=sys.stderr)
    sys.exit(1)
print(f'Documentation checks passed: {len(pages)} pages, {len(llm_sources)} LLM exports, {len(MANIFEST["sources"])} mapped sources')
