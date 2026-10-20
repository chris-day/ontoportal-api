# OntoPortal API and Python Client

## Purpose
This documentation covers the OntoPortal/BioPortal REST API, this repository's OpenAPI description, and its Python client. It serves application developers, API integrators, and ontology data specialists.

## What is OntoPortal / BioPortal?
OntoPortal is a platform for hosting and accessing biomedical ontologies. Its REST API exposes ontologies, classes (concepts), mappings, annotations, and recommendations as hypermedia-linked resources. Official API docs: `https://data.bioontology.org/documentation`.

## What this project delivers
- A reusable client SDK (Python) for the OntoPortal/BioPortal REST API.
- An OpenAPI 3.1 description with modeled schemas, parameters, and hypermedia behavior.

## How this documentation is organized
- **Getting Started**: auth, first call, environment setup.
- **Architecture**: system context, SDK design, error handling strategy.
- **OpenAPI**: base URL, security schemes, Swagger/Redoc/Postman usage.
- **Endpoint Guides**: per-endpoint details and pitfalls.
- **Recipes**: task-oriented usage patterns.
- **Semantics**: ontology concepts and JSON-LD interpretation.
- **Operations**: pagination, errors, testing, release strategy, contribution.

## Quick links
- [Getting Started](Getting-Started.md)
- [OpenAPI Specification](OpenAPI-Specification.md)
- [Python SDK Quickstart](Python-SDK-Quickstart.md)
- [Endpoint Guides](Endpoint-Guides.md)
- [Usage Patterns](Usage-Patterns.md)
- [Client SDK Documentation](Client-SDK-Documentation.md)
- [Data and Semantics](Data-and-Semantics.md)
- [Documentation maintenance and privacy](Documentation-Maintenance.md)
