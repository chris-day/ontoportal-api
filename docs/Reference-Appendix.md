# Reference Appendix

## Purpose
Provide a glossary, endpoint index, official links, and example raw payloads.

## Glossary (selected terms)
- **Ontology**: structured vocabulary with relationships.
- **Class**: a concept inside an ontology.
- **Mapping**: relationship between terms across ontologies.
- **JSON-LD**: JSON with linked-data semantics.

## Full endpoint list (high-level)
- `/ontologies`
- `/ontologies/:acronym`
- `/ontologies/:acronym/classes`
- `/ontologies/:acronym/classes/roots`
- `/ontologies/:acronym/classes/:cls/children`
- `/ontologies/:acronym/classes/:cls/parents`
- `/search`
- `/annotator`
- `/recommender`

## Official documentation
- API docs: `https://data.bioontology.org/documentation`

## Example raw JSON payload (simplified)
```json
{
  "acronym": "ABA-API-TST",
  "name": "ABA Adult Mouse Brain",
  "@id": "http://data.bioontology.org/ontology/ABA-API-TST",
  "@type": "http://data.bioontology.org/metadata/Ontology",
  "links": {
    "classes": "http://data.bioontology.org/ontologies/ABA-API-TST/classes"
  }
}
```
