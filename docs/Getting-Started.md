# Getting Started

## Purpose
Get from zero to a working API call with authentication, a first search, and environment setup guidance.

## API key setup and authentication
An API key is required for every request. You can provide it in any of these forms:
- Query parameter: `apikey=YOUR_KEY`
- Authorization header: `Authorization: apikey token=YOUR_KEY`
- Browser cookie after providing an `apikey` once

Official docs: `https://data.bioontology.org/documentation`.

### Example (curl, header auth)
```bash
curl -H "Authorization: apikey token=YOUR_KEY" \
  "https://data.bioontology.org/ontologies"
```

## Making the first API call
```bash
curl "https://data.bioontology.org/ontologies?apikey=YOUR_KEY"
```

## Example: searching for a term
```bash
curl "https://data.bioontology.org/search?q=melanoma&apikey=YOUR_KEY"
```

## Environment setup

### Python
```bash
python -m venv .venv
source .venv/bin/activate
pip install requests
```

### Other languages
If you are not using the Python SDK, any HTTP client can call the REST API directly. Use the curl examples on this page as a reference for request structure.

## Notes on rate limits
The platform enforces rate limits. Practical guidance is to monitor response time and reduce concurrency for heavy endpoints like Annotator and Recommender. See NCBO guidance: `https://www.bioontology.org/wiki/Annotator_Optimizing_and_Troublehooting`.
