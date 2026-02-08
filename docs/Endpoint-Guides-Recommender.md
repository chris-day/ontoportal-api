# Endpoint Guide: Recommender

## Intro
Back to the endpoint index: [Endpoint Guides](Endpoint-Guides).

## Python SDK quickstart
Need setup help? See [Python SDK Quickstart](Python-SDK-Quickstart). Minimal init:
```python
from ontoportal_client import ClientConfig, OntoPortalClient

client = OntoPortalClient(ClientConfig(api_key="YOUR_KEY"))
```

## Purpose
Explain how to rank ontologies relevant to a text or keyword list.

## What the endpoint does
`/recommender` returns ranked ontologies based on input text or keywords.

## Example request (keywords)
```bash
curl "https://data.bioontology.org/recommender?input=melanoma,tumor,melanocyte&input_type=2&apikey=YOUR_KEY"
```

## Python example (ontoportal-client)
```python
from ontoportal_client import ClientConfig, OntoPortalClient

config = ClientConfig(api_key="YOUR_KEY")
client = OntoPortalClient(config)

recommendations = client.recommender(
    "melanoma,tumor,melanocyte",
    input_type=2,
)
```

## Example response (simplified)
```json
[
  {
    "ontology": { "acronym": "NCIT" },
    "score": 0.87
  }
]
```

## Field explanations
- `input_type=1` for free text, `input_type=2` for keyword list.
- `score`: ranking score from Recommender.
- `wc`, `wa`, `wd`, `ws`: optional weights for coverage, acceptance, detail, and specialization.

## Common pitfalls
- Using keyword lists without `input_type=2`.
- Large inputs causing long runtimes.
