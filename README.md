# OntoPortal API and Python client

OpenAPI description and Python client library for OntoPortal/BioPortal APIs.

Read the [documentation](https://chris-day.github.io/ontoportal-api/) for setup, endpoint guides, and API reference. The [documentation source](docs/index.md) is maintained in this repository.

The project is licensed under the [BSD 2-Clause License](LICENSE).

Install the client from this checkout with `python -m pip install -e .`. For a first API request, see the [Python SDK quickstart](docs/Python-SDK-Quickstart.md).

Make targets:
- `openapi-json` regenerates `openapi/ontoportal.json` from `openapi/ontoportal.yaml`.
  - Requires PyYAML (installed with `pip install -e .`).

OntoPortal servers:
- BioPortal: https://data.bioontology.org/ — "The world's most comprehensive repository of biomedical ontologies"
- SIFR BioPortal: https://data.bioportal.lirmm.fr/ — "A repository for French biomedical terminologies and ontologies"
- AgroPortal: https://data.agroportal.lirmm.fr/ — "A vocabulary and ontology repository for agronomy and related domains"
- EcoPortal: https://data.ecoportal.lifewatch.eu/ — "The LifeWatch ERIC repository of semantic resources for ecology and related domains"
- EarthPortal: https://data.earthportal.eu/ — "A semantic artefact repository dedicated to Earth sciences"
- BiodivPortal: https://data.biodivportal.gfbio.org/ — "A semantic artefact repository for biodiversity"
- TechnoPortal: https://data.technoportal.hevs.ch/ — "A repository for the technology sciences domain"

Version: 0.1.21
