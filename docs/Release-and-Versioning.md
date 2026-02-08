# Release and Versioning

## Purpose
Define how the OpenAPI spec and SDKs are versioned and kept compatible.

## Versioning the OpenAPI spec
Use semantic versioning for the spec: major for breaking changes, minor for additive changes, patch for corrections.

## SDK version alignment
SDK versions should track the spec version and communicate compatibility in release notes.

## Backwards compatibility strategy
- Avoid removing fields; deprecate first.
- Add new fields as optional with safe defaults.
- Keep parameter semantics stable.

## Change log structure
Use a standard format:
- Added
- Changed
- Deprecated
- Removed
- Fixed
