# Error Handling and Limits

## Purpose
Provide robust error handling and rate-limit guidance.

## Common HTTP status codes
- `400` bad request
- `401` missing or invalid API key
- `403` access forbidden
- `404` resource not found
- `429` rate limit exceeded
- `5xx` server error

## Handling 429 rate limits
Use exponential backoff with jitter and reduce concurrency. For high-cost endpoints like Annotator/Recommender, send smaller batches and monitor response time.

## Retry/backoff patterns
- Retry `429` and transient `5xx` errors.
- Use capped exponential backoff with randomized jitter.

## Debugging failed requests
- Validate API key and auth method.
- Ensure class IDs are URL-encoded.
- Test URLs with `curl` and compare response structure.
