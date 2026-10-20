# Architecture Overview

## Purpose
Explain system context, SDK structure, hypermedia behavior, and error handling strategy.

## System context
Client SDKs communicate with the OntoPortal REST API, which exposes ontologies and classes as JSON-LD resources. The API uses hypermedia links for navigation.

## Client library architecture
- **HTTP layer**: authentication, timeouts, retries, and transport details.
- **Client methods**: ontology, class, search, annotator, and recommender requests are exposed by `OntoPortalClient`.
- **Models**: `TypedDict` definitions describe expected response shapes; the client returns decoded JSON rather than model instances.

## Hypermedia (HATEOAS)
Responses include `@id`, `@type`, and `links` objects. Clients should follow these links instead of hard-coding URL patterns.

## Error handling and retry strategy
- Treat `4xx` as client errors, `5xx` as server errors.
- The HTTP client retries `429` and transient server errors with capped backoff and jitter.
- Prefer paging via `links.nextPage` and `links.prevPage` when present.
