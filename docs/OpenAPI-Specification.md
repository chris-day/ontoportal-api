# OpenAPI / Swagger Specification

## Purpose
Explain how the OpenAPI 3.1 spec is modeled and how to use it for tooling and validation.

## API base URL
`https://data.bioontology.org`

## Security schemes
The API uses an API key provided via:
- Query parameter `apikey`
- Header `Authorization: apikey token=YOUR_KEY`

## Download and use the OpenAPI YAML
The repository ships `openapi/ontoportal.yaml` and a generated `openapi/ontoportal.json`. Use either with:
- Swagger UI
- Redoc
- Postman

## Swagger UI / Redoc / Postman usage
1) Import `openapi/ontoportal.yaml` or `openapi/ontoportal.json`.
2) Configure the API key.
3) Use sample endpoints like `/search` and `/ontologies`.

## Schema modeling approach
- JSON-LD fields (`@id`, `@type`, `@context`) are represented explicitly.
- Hypermedia `links` are modeled as objects with relation URLs.
- List endpoints expose `collection` and paging metadata.

## Assumptions (where official docs are implicit)
- Default content type is JSON-LD, even if clients treat it as normal JSON.
- Paging is supported via `page`/`pagesize` and hypermedia links.
- The published API can differ from this repository's model; validate endpoint behavior against the live API before relying on optional parameters.
