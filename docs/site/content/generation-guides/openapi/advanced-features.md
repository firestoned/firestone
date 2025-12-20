+++
title = "Advanced OpenAPI Features"
linkTitle = "Advanced Features"
weight = 6
description = "Unlock the full potential of Firestone's OpenAPI generation."
+++

## Fine-Tuning Your Spec

Firestone automates the basics, but supports advanced OpenAPI features through pass-through mechanisms and smart defaults.

### Key Capabilities

*   **[Custom Response Codes](response-code-customization.md):** Document `409 Conflict`, `201 Created`, etc.
*   **[OpenAPI Extensions](openapi-extensions.md):** Add `x-` fields for gateways and tooling.
*   **[Schema Reuse](../../advanced-topics/schema-references-and-reuse):** Use `$ref` for modular data models.

### Schema Composition
Firestone supports `oneOf`, `anyOf`, and `allOf` directly in your `schema.items` definition.

```yaml
schema:
  items:
    oneOf:
      - $ref: '#/components/schemas/Dog'
      - $ref: '#/components/schemas/Cat'
```

### Webhooks
While Firestone doesn't have a top-level `webhooks` DSL yet, you can define webhook payload schemas in your resource and reference them in a manually merged OpenAPI file or via post-processing.

