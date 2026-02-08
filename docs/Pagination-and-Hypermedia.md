# Pagination and Hypermedia

## Purpose
Explain how to navigate large collections and why hypermedia links matter.

## links usage
Most collection resources include a `links` object with relation URLs (for example, `children`, `parents`, or `submissions`).

## next/prev page navigation
- Use `page` and `pagesize` query parameters for pagination.
- Follow `links.nextPage` and `links.prevPage` when present.

## Why hypermedia navigation matters
Hypermedia reduces client coupling to URL patterns. If URLs change, links in responses remain the source of truth.

## Avoid hard-coded URLs
Prefer URLs from `links` instead of manually composing paths.
