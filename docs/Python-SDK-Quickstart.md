# Python SDK Quickstart

## Purpose
Provide a minimal, reusable setup snippet for the official Python client SDK.

## Install
```bash
pip install ontoportal-client
```

## Initialize
```python
from ontoportal_client import ClientConfig, OntoPortalClient

config = ClientConfig(api_key="YOUR_KEY")
client = OntoPortalClient(config)
```

## Notes
- The SDK reads environment variables via `ClientConfig.from_env()` if you prefer not to hard-code keys.
- Default base URL is `https://data.bioontology.org`.
