"""Write pinned documentation dependency closures from the active .venv."""

from __future__ import annotations

from importlib import metadata
from pathlib import Path
import sys

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).resolve().parents[1]
assert sys.prefix == str(ROOT / '.venv'), 'Run this with the repository .venv Python'


def closure(roots: set[str]) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    pending = list(roots)
    while pending:
        name = pending.pop()
        dist = metadata.distribution(name)
        key = canonicalize_name(dist.metadata['Name'])
        if key in result:
            continue
        result[key] = (dist.metadata['Name'], dist.version)
        for raw in dist.requires or []:
            dependency = Requirement(raw)
            if dependency.marker is None or dependency.marker.evaluate({'extra': ''}):
                pending.append(dependency.name)
    return result


def write(path: str, roots: set[str], comment: str) -> None:
    packages = closure(roots)
    lines = [f'# {comment}']
    lines += [f'{name}=={version}' for name, version in sorted(packages.values(), key=lambda item: item[0].lower())]
    (ROOT / path).write_text('\n'.join(lines) + '\n')
    print(f'{path}: {len(packages)} pinned packages')


write('requirements-docs.txt', {'zensical', 'pip', 'setuptools', 'wheel'}, 'Validated documentation dependency closure on Python 3.14.')
write('requirements-docs-browser.txt', {'playwright'}, 'Optional browser verification dependencies for the same repository .venv.')
