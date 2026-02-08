# Testing and Validation

## Purpose
Explain how to test SDK behavior and validate against the OpenAPI spec.

## Unit testing the client
- Mock the HTTP layer.
- Validate headers, query parameters, and request composition.

## Contract testing with OpenAPI
- Validate requests and responses against `openapi.yaml`.
- Treat schema changes as contract changes.

## Mock servers from the spec
Use OpenAPI tooling to generate mock servers for offline development and deterministic tests.

## Example test data
Maintain fixtures for `/ontologies`, `/search`, and `/annotator` to cover common patterns and edge cases.
