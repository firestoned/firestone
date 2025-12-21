+++
title = "Changelog"
weight = 150
description = "History of changes, improvements, and fixes in the Firestone project."
+++

## Version History

### v0.8.0 (Current)
*   **Feature:** Added support for Python 3.12 and 3.13.
*   **Feature:** Integrated `pdoc-markdown` for auto-generated API documentation.
*   **Improvement:** Migrated documentation site to Zola.
*   **Fix:** Resolved issues with complex schema validation in nested objects.

### v0.7.0
*   **Feature:** Streamlit UI generation now supports custom themes.
*   **Improvement:** Enhanced error messages for invalid YAML blueprints.
*   **Fix:** Fixed a bug where `versionInPath` was ignored for AsyncAPI specs.

### v0.6.0
*   **Feature:** Added support for `oneOf`, `anyOf`, and `allOf` schema composition.
*   **Feature:** New `firestone-lib` package for programmatic generation.
*   **Improvement:** Significant performance improvements for large schemas.

### v0.5.0
*   **Feature:** Initial support for AsyncAPI generation.
*   **Feature:** Added `metadata` block to resource schema.
*   **Change:** Renamed `api_version` to `apiVersion` for consistency.

### v0.4.0
*   **Feature:** CLI generation using Click.
*   **Feature:** Support for Bearer token authentication schemes.

### v0.3.0
*   **Feature:** Initial release of OpenAPI 3.0 generation.
*   **Feature:** Basic resource schema validation.
