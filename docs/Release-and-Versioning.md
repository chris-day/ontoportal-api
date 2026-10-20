# Release and Versioning

## Purpose
Describe a proposed versioning approach for the OpenAPI description and Python client. These guidelines do not represent an enforced release process.

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
