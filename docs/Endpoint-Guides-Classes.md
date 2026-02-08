# Endpoint Guide: Classes (Concepts)

## Intro
Back to the endpoint index: [Endpoint Guides](Endpoint-Guides.md).

## Python SDK quickstart
Need setup help? See [Python SDK Quickstart](Python-SDK-Quickstart.md). Minimal init:
```python
from ontoportal_client import ClientConfig, OntoPortalClient

client = OntoPortalClient(ClientConfig(api_key="YOUR_KEY"))
```

## Purpose
Explain how to access classes and traverse ontology hierarchies.

## What the endpoint does
Class endpoints support roots, parents, children, ancestors, and descendants.

## Example request
```bash
curl "https://data.bioontology.org/ontologies/NCIT/classes/roots?apikey=YOUR_KEY"
```

## Python example (ontoportal-client)
```python
from ontoportal_client import ClientConfig, OntoPortalClient

config = ClientConfig(api_key="YOUR_KEY")
client = OntoPortalClient(config)

classes = client.list_classes("NCIT")
melanoma = client.get_class("NCIT", "http://purl.bioontology.org/ontology/NCIT/C3224")
```

## Example response (simplified)
```json
{
  "@id": "https://data.bioontology.org/ontologies/NCIT/classes/http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FNCIT%2FC000000",
  "prefLabel": "Neoplasm",
  "links": {
    "children": "https://data.bioontology.org/ontologies/NCIT/classes/.../children"
  }
}
```

## Field explanations
- `prefLabel`: preferred name.
- `synonym`, `definition`, `semanticType`: descriptive metadata when available.
- `links.children`, `links.parents`, `links.ancestors`: navigation targets.

## Common pitfalls
- Class IDs must be URL-encoded.
- Hierarchies can be DAGs, not simple trees.
