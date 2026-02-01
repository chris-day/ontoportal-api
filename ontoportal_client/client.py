from __future__ import annotations

from typing import Any, Iterable

from .config import ClientConfig
from .http import HttpClient
from .utils import encode_class_iri, extract_links, get_link_href, split_url


class OntoPortalClient:
    def __init__(self, config: ClientConfig | None = None, http: HttpClient | None = None):
        self.config = config or ClientConfig.from_env()
        self.http = http or HttpClient(self.config)

    # Ontologies
    def list_ontologies(self, *, params: dict | None = None):
        return self.http.request("GET", "/ontologies", params=params)

    def get_ontology(self, acronym: str):
        return self.http.request("GET", f"/ontologies/{acronym}")

    # Classes
    def list_classes(self, acronym: str, *, params: dict | None = None):
        return self.http.request("GET", f"/ontologies/{acronym}/classes", params=params)

    def get_class(self, acronym: str, class_iri: str):
        encoded = encode_class_iri(class_iri)
        return self.http.request("GET", f"/ontologies/{acronym}/classes/{encoded}")

    # Search
    def search(
        self,
        q: str,
        *,
        ontologies: list[str] | None = None,
        page: int | None = None,
        pagesize: int | None = None,
        include: list[str] | None = None,
        **params: Any,
    ):
        query = {"q": q}
        if ontologies:
            query["ontologies"] = ",".join(ontologies)
        if page is not None:
            query["page"] = page
        if pagesize is not None:
            query["pagesize"] = pagesize
        if include:
            query["include"] = ",".join(include)
        query.update(params)
        return self.http.request("GET", "/search", params=query)

    # Annotator
    def annotator(
        self,
        text: str,
        *,
        ontologies: list[str] | None = None,
        semantic_types: list[str] | None = None,
        **params: Any,
    ):
        query = {"text": text}
        if ontologies:
            query["ontologies"] = ",".join(ontologies)
        if semantic_types:
            query["semantic_types"] = ",".join(semantic_types)
        query.update(params)
        return self.http.request("GET", "/annotator", params=query)

    # Recommender
    def recommender(self, input_text: str, **params: Any):
        query = {"input": input_text}
        query.update(params)
        return self.http.request("GET", "/recommender", params=query)

    # Hypermedia helpers
    def follow_link(self, payload: dict, rel: str):
        links = extract_links(payload)
        href = get_link_href(links, rel)
        if not href:
            return None
        if href.startswith("http://") or href.startswith("https://"):
            return self.http.request_url("GET", href)
        return self.http.request("GET", href)

    # Pagination
    def paginate(self, path: str, *, params: dict | None = None) -> Iterable[Any]:
        params = dict(params or {})
        url_path = path
        while True:
            response = self.http.request("GET", url_path, params=params)
            if isinstance(response, list):
                for item in response:
                    yield item
            elif isinstance(response, dict) and "collection" in response:
                for item in response.get("collection") or []:
                    yield item
            elif isinstance(response, dict) and "results" in response:
                for item in response.get("results") or []:
                    yield item
            else:
                yield response

            next_href = None
            if isinstance(response, dict):
                links = extract_links(response)
                next_href = get_link_href(links, "nextPage") or get_link_href(links, "next")

            if next_href:
                if next_href.startswith("http://") or next_href.startswith("https://"):
                    url_path, params = split_url(next_href)
                else:
                    url_path = next_href
                    params = {}
                continue

            if isinstance(response, dict) and "page" in response and "pageCount" in response:
                try:
                    page = int(response["page"])
                    page_count = int(response["pageCount"])
                except (ValueError, TypeError):
                    break
                if page < page_count:
                    params = dict(params)
                    params["page"] = page + 1
                    continue

            break
