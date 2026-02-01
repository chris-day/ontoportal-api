# ontoportal-api
OpenAPI and client library for OntoPortal/BioPortal APIs.

Make targets:
- `openapi-json` regenerates `openapi/ontoportal.json` from `openapi/ontoportal.yaml`.
  - Requires PyYAML (install with `pip install -e .[dev]`).

OntoPortal servers:
- BioPortal: https://data.bioontology.org/ — "The world's most comprehensive repository of biomedical ontologies"
- SIFR BioPortal: https://data.bioportal.lirmm.fr/ — "A repository for French biomedical terminologies and ontologies"
- AgroPortal: https://data.agroportal.lirmm.fr/ — "A vocabulary and ontology repository for agronomy and related domains"
- EcoPortal: https://data.ecoportal.lifewatch.eu/ — "The LifeWatch ERIC repository of semantic resources for ecology and related domains"
- EarthPortal: https://data.earthportal.eu/ — "A semantic artefact repository dedicated to Earth sciences"
- BiodivPortal: https://data.biodivportal.gfbio.org/ — "A semantic artefact repository for biodiversity"
- TechnoPortal: https://data.technoportal.hevs.ch/ — "A repository for the technology sciences domain"

Version: 0.1.21
