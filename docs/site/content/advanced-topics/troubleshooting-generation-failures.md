+++
title = "Generation Failures"
weight = 1
description = "Diagnosing issues when running firestone generate."
+++

## Troubleshooting Generation

If `firestone generate` fails, use the `--debug` flag to get a full stack trace and verbose logging:

```bash
firestone --debug generate --resources . openapi
```

**Common Error Categories:**

1.  **YAML/JSON Syntax:**
    *   *Symptom:* `ScannerError` or `ParserError`.
    *   *Fix:* Check indentation and special characters. Use a linter.

2.  **Schema Validation:**
    *   *Symptom:* `ValidationError: 'properties' is a required property`.
    *   *Fix:* Your resource does not conform to the JSON Schema spec. Ensure `items` has `type: object`.

3.  **Firestone DSL:**
    *   *Symptom:* `KeyError: 'kind'`.
    *   *Fix:* You are missing a required Firestone top-level field (`kind`, `apiVersion`).

4.  **Ref Resolution:**
    *   *Symptom:* `RefResolutionError`.
    *   *Fix:* Check your `$ref` paths. Paths are relative to the file containing the reference.