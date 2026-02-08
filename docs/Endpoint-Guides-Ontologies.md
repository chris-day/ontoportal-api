# Endpoint Guide: Ontologies

## Intro
Back to the endpoint index: [Endpoint Guides](Endpoint-Guides).

## Python SDK quickstart
Need setup help? See [Python SDK Quickstart](Python-SDK-Quickstart). Minimal init:
```python
from ontoportal_client import ClientConfig, OntoPortalClient

client = OntoPortalClient(ClientConfig(api_key="YOUR_KEY"))
```

## Purpose
Describe how to list and retrieve ontology metadata, submissions, and related resources.

## What the endpoint does
`/ontologies` is the canonical collection of ontology resources. Each ontology has links to submissions and classes.

## Example request
```bash
curl "https://data.bioontology.org/ontologies?apikey=YOUR_KEY"
```

## Python example (ontoportal-client)
```python
from ontoportal_client import ClientConfig, OntoPortalClient

config = ClientConfig(api_key="YOUR_KEY")
client = OntoPortalClient(config)

ontologies = client.list_ontologies()
ncit = client.get_ontology("NCIT")
```

## Example response (simplified)
```json
{
  "acronym": "NCIT",
  "name": "NCI Thesaurus",
  "@id": "https://data.bioontology.org/ontologies/NCIT",
  "@type": "http://data.bioontology.org/metadata/Ontology",
  "links": {
    "submissions": "https://data.bioontology.org/ontologies/NCIT/submissions",
    "classes": "https://data.bioontology.org/ontologies/NCIT/classes"
  }
}
```

## Field explanations
- `acronym`: short identifier used in URLs.
- `@id`: canonical ontology resource URL.
- `links`: navigation to related resources.

## Common pitfalls
- Missing API key.
- Ignoring `links` and hard-coding URLs.
