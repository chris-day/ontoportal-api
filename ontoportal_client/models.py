from __future__ import annotations

from typing import NotRequired, TypedDict, List, Dict, Any


class Link(TypedDict, total=False):
    href: str
    url: str


class Links(TypedDict, total=False):
    nextPage: Link | str
    prevPage: Link | str
    children: Link | str
    parents: Link | str
    ancestors: Link | str
    descendants: Link | str


class Ontology(TypedDict, total=False):
    acronym: str
    name: str
    description: str
    ontologyType: str
    status: str
    administeredBy: str
    resourceType: str
    links: Links


class OntologyClass(TypedDict, total=False):
    id: str
    prefLabel: str
    synonym: List[str]
    definition: List[str]
    links: Links


class SearchResult(TypedDict, total=False):
    prefLabel: str
    synonym: List[str]
    definition: List[str]
    ontology: str
    annotatedClass: Dict[str, Any]
    links: Links


class Annotation(TypedDict, total=False):
    text: str
    matchType: str
    annotatedClass: Dict[str, Any]
    annotations: List[Dict[str, Any]]


class RecommenderResult(TypedDict, total=False):
    ontology: Ontology
    score: float
    coverageResult: Dict[str, Any]
    specializationResult: Dict[str, Any]
    acceptanceResult: Dict[str, Any]
    detail: Dict[str, Any]
