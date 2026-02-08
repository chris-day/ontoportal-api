# Endpoint Guide: Search

## Intro
Back to the endpoint index: [Endpoint Guides](Endpoint-Guides.md).

## Python SDK quickstart
Need setup help? See [Python SDK Quickstart](Python-SDK-Quickstart.md). Minimal init:
```python
from ontoportal_client import ClientConfig, OntoPortalClient

client = OntoPortalClient(ClientConfig(api_key="YOUR_KEY"))
```

## Purpose
Explain full-text term search across ontologies.

## What the endpoint does
`/search` performs full-text search across selected ontologies and returns a collection of class matches.

## Example request
```bash
curl "https://data.bioontology.org/search?q=melanoma&apikey=YOUR_KEY"
```

## Python example (ontoportal-client)
```python
from ontoportal_client import ClientConfig, OntoPortalClient

config = ClientConfig(api_key="YOUR_KEY")
client = OntoPortalClient(config)

results = client.search("melanoma", require_exact_match=False)
```

## Example response (simplified)
```json
{
  "collection": [
    {
      "prefLabel": "Melanoma",
      "links": {
        "ontology": "https://data.bioontology.org/ontologies/NCIT"
      }
    }
  ],
  "page": 1
}
```

## Field explanations
- `collection`: matching classes.
- `page` / `pagesize`: paging controls.
- `links.ontology`: link to the ontology that contains the class.

## Common pitfalls
- Expecting search to be scoped without `ontologies` or `roots` filters.
- Forgetting `require_exact_match` when doing precise lookups.
