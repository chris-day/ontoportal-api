# Client SDK Documentation

## Purpose
Provide install and usage guidance for the Python client library.

## Python client

### Installation
```bash
pip install ontoportal-client
```

### Client initialization
```python
from ontoportal_client import ClientConfig, OntoPortalClient
client = OntoPortalClient(ClientConfig(api_key="YOUR_KEY"))
```

### Common usage
```python
results = client.search("melanoma", require_exact_match=True)
```

## Notes
This repository provides a Python client. Other languages can call the REST API directly using standard HTTP clients.
