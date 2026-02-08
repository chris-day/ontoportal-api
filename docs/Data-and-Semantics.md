# Data and Semantics

## Purpose
Explain ontology metadata, class structure, and how JSON-LD maps to semantic meaning.

## Ontology metadata fields
Ontology resources include identifiers, labels, versioning info, and links to submissions and class collections.

## Class / concept structure
Classes may include:
- `prefLabel`: preferred human-readable label
- `synonym`: alternate labels
- `definition`: descriptive text
- `semanticType`, `cui`: optional domain-specific metadata
- `links` for parents, children, ancestors, descendants

## prefLabel vs synonyms vs definitions
- `prefLabel` is the canonical label used for UI or display.
- `synonym` contains equivalent or related labels.
- `definition` provides a description if present.

## JSON structure vs semantic meaning
JSON-LD fields (`@id`, `@type`) connect API responses to linked-data semantics. Clients can treat responses as plain JSON but still benefit from URI-based identity.

## Mapping API responses to RDF/ontology concepts
- `@id` corresponds to the class IRI.
- `@type` represents the resource type.
- Hypermedia links represent relationships in the ontology.
