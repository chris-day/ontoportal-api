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
from ontoportal_client import Client
client = Client(api_key="YOUR_KEY")
```

### Common usage
```python
results = client.search(q="melanoma", require_exact_match=True)
```

## Notes
The official SDK is currently available for Python. Other languages can call the REST API directly using standard HTTP clients.
