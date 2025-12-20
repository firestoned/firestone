+++
title = "Schema Design"
weight = 2
description = "Leveraging JSON Schema within Firestone: Best practices for defining robust resource blueprints."
+++

## Schema Design with Firestone

Firestone relies entirely on [JSON Schema](https://json-schema.org/) to define the structure, validation, and documentation of your API resources. Your schema *is* your API contract.

**How Firestone Uses Your Schema:**
*   **API Contract:** The schema directly generates the OpenAPI `components/schemas` and request/response bodies.
*   **Validation:** Firestone-generated code (and the OpenAPI spec) enforces all validation rules (`required`, `minLength`, `pattern`, etc.) defined in your schema.
*   **Documentation:** Field descriptions and examples in your schema are propagated directly to the generated OpenAPI documentation and CLI help text.
*   **CLI Arguments:** Schema properties are automatically converted into typed command-line arguments and options.

**Firestone-Specific Considerations:**
*   **`description` is Mandatory:** For high-quality CLI help text and API documentation, every field should have a `description`.
*   **`key` Field:** Ensure your resource schema defines a clear primary key structure, as Firestone uses this for instance lookup paths (e.g., `/users/{user_id}`).
*   **`x-` Extensions:** Firestone may utilize vendor extensions (like `x-hidden: true` to hide fields from CLI output) if supported.

For general best practices on designing robust and reusable JSON Schemas, we recommend these authoritative resources:

*   [**JSON Schema: Getting Started**](https://json-schema.org/learn/getting-started-step-by-step)
*   [**Understanding JSON Schema (Official Guide)**](https://json-schema.org/understanding-json-schema/)
*   [**JSON Schema Best Practices (Stoplight)**](https://stoplight.io/api-design-guide/basics)
*   [**Modeling Data with JSON Schema**](https://json-schema.org/learn/getting-started-step-by-step)

By mastering JSON Schema, you unlock the full power of Firestone's automation.

---
## Next Steps

With your schemas well-defined, it's crucial to protect them.
- **Next:** Dive into **[Security Best Practices](./security-best-practices)**.
