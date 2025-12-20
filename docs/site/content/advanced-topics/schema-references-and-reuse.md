+++
title = "Schema References & Reuse"
linkTitle = "Schema Reuse"
weight = 2
description = "Building modular blueprints with $ref resolution."
+++

## Modular Schemas with `$ref`

Firestone leverages the JSON Schema `$ref` keyword to allow you to split your API definitions into modular, reusable files.

**How Firestone Handles Refs:**
During generation, Firestone (via `firestone-lib`) resolves all references to create a self-contained specification or a properly linked output.

**Supported Reference Types:**
1.  **Local References:** ` $ref: '#/components/schemas/Address'` (referencing definitions within the same file).
2.  **File References:** `$ref: './common/address.yaml'` (referencing external files).
3.  **URL References:** `$ref: 'https://example.com/schema.json'` (fetching remote schemas).

**Best Practice:**
Create a `common/` directory for shared data models (Error, Address, UserID) and reference them across your resource files. This ensures consistency and reduces duplication.

For details on structuring schemas and using composition keywords (`allOf`, `oneOf`, `anyOf`), refer to:

*   [**Structuring JSON Schema**](https://json-schema.org/understanding-json-schema/structuring.html)
*   [**Schema Composition**](https://json-schema.org/understanding-json-schema/reference/combining.html)
