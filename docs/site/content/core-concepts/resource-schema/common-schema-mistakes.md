+++
title = "Common Schema Mistakes"
weight = 53
description = "Troubleshooting common errors in Firestone resource definitions."
+++

## Debugging Firestone Schemas

While Firestone uses standard JSON Schema, its specific DSL requirements can sometimes trip you up.

**Common Firestone-Specific Errors:**

1.  **Missing `key` Field:**
    *   **Error:** CLI fails to generate instance commands; OpenAPI paths missing `{id}`.
    *   **Fix:** Ensure your resource schema includes a `key` object defining the primary identifier.
    ```yaml
    key:
      name: user_id
      schema: { type: string }
    ```

2.  **Invalid Method Names:**
    *   **Error:** Generation succeeds but endpoints are missing.
    *   **Fix:** Use lowercase HTTP verbs in the `methods` block (`get`, `post`, `put`, `delete`).

3.  **Missing `description` Fields:**
    *   **Error:** Empty help text in CLI; blank descriptions in Swagger UI.
    *   **Fix:** Populate `description` for every property and metadata field.

4.  **Incorrect `type: array` for Resources:**
    *   **Error:** "Resource must be an array".
    *   **Fix:** Top-level resources in Firestone are collections, so the root schema `type` must be `array`, and the item definition goes in `items`.

**Debugging Tips:**
*   **Use `--debug`:** Run `firestone --debug generate ...` to see detailed tracebacks.
*   **Validate Schema:** Use an online JSON Schema validator to check syntax errors before running Firestone.
