# Endpoint Guide: Annotator

## Intro
Back to the endpoint index: [Endpoint Guides](Endpoint-Guides.md).

## Python SDK quickstart
Need setup help? See [Python SDK Quickstart](Python-SDK-Quickstart.md). Minimal init:
```python
from ontoportal_client import ClientConfig, OntoPortalClient

client = OntoPortalClient(ClientConfig(api_key="YOUR_KEY"))
```

## Purpose
Explain how to annotate free text with ontology concepts.

## What the endpoint does
`/annotator` analyzes text and returns matched ontology classes plus character offsets.

## Example request
```bash
curl "https://data.bioontology.org/annotator?text=Melanoma%20is%20a%20malignant%20tumor&apikey=YOUR_KEY"
```

## Python example (ontoportal-client)
```python
from ontoportal_client import ClientConfig, OntoPortalClient

config = ClientConfig(api_key="YOUR_KEY")
client = OntoPortalClient(config)

annotations = client.annotator(
    "Melanoma is a malignant tumor",
    ontologies=["NCIT"],
    longest_only=True,
)
```

## Example response (simplified)
```json
[
  {
    "annotatedClass": {
      "prefLabel": "Melanoma",
      "@id": "https://data.bioontology.org/ontologies/NCIT/classes/http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FNCIT%2FC3224"
    },
    "annotations": [
      { "text": "Melanoma", "from": 0, "to": 8 }
    ]
  }
]
```

## Field explanations
- `annotatedClass`: matched class resource.
- `annotations`: text offsets where the class matched.

## Common pitfalls
- Not constraining ontologies for performance.
- Ignoring settings like `exclude_synonyms` and `longest_only`.
