# Architecture Overview

## Purpose
Explain system context, SDK structure, hypermedia behavior, and error handling strategy.

## System context
Client SDKs communicate with the OntoPortal REST API, which exposes ontologies and classes as JSON-LD resources. The API uses hypermedia links for navigation.

## Client library architecture
- **HTTP layer**: authentication, timeouts, retries, and transport details.
- **Endpoint modules**: `/ontologies`, `/classes`, `/search`, `/annotator`, `/recommender`.
- **Models**: typed data objects for ontology metadata, class details, and annotations.

## Hypermedia (HATEOAS)
Responses include `@id`, `@type`, and `links` objects. Clients should follow these links instead of hard-coding URL patterns.

## Error handling and retry strategy
- Treat `4xx` as client errors, `5xx` as server errors.
- Retry `429` with exponential backoff and jitter.
- Prefer paging via `links.nextPage` and `links.prevPage` when present.
