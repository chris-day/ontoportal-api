from __future__ import annotations

from urllib.parse import quote, urlparse, parse_qs


def encode_class_iri(iri: str) -> str:
    return quote(iri, safe="")


def extract_links(payload: dict) -> dict:
    if not isinstance(payload, dict):
        return {}
    links = payload.get("_links") or payload.get("links")
    return links if isinstance(links, dict) else {}


def get_link_href(links: dict, rel: str) -> str | None:
    if not links or rel not in links:
        return None
    target = links[rel]
    if isinstance(target, str):
        return target
    if isinstance(target, dict):
        return target.get("href") or target.get("url")
    return None


def split_url(href: str) -> tuple[str, dict]:
    parsed = urlparse(href)
    params = {k: v[0] for k, v in parse_qs(parsed.query).items()}
    path = parsed.path
    return path, params
