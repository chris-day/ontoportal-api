# Contributing Guide

## Purpose
Explain how to contribute to the SDKs and OpenAPI spec safely.

## Repository structure
- `openapi/` for the OpenAPI spec
- `ontoportal_client/` for SDK code
- `tests/` for test suites

## How to update the OpenAPI spec
- Extract endpoints and parameters from the official docs.
- Model JSON-LD fields and hypermedia links.
- Add or update response examples with real API shapes.

## Coding standards
- Keep naming consistent across languages.
- Add tests for new endpoints.

## Adding new endpoints
- Define path, parameters, and responses.
- Update SDK endpoints and add tests.

## Updating schemas safely
- Prefer additive changes.
- Use `nullable` or optional fields for uncertain properties.
