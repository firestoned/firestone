+++
title = "Custom Response Codes"
weight = 51
description = "Documenting non-standard HTTP status codes in Firestone."
+++

## Beyond 200 OK

Firestone generates standard responses (`200`, `201`, `204`, `400`, `500`). You can document additional status codes (like `409 Conflict` or `429 Too Many Requests`) using the `descriptions` block.

**Method 1: Documentation Only**
Add a markdown list to the description. Firestone parses this for human-readable docs.

```yaml
descriptions:
  resource:
    post:
      description: |
        Creates a user.
        **Returns:**
        - `201` - Created
        - `409` - Email exists
```

**Method 2: Full OpenAPI Definition (`x-responses`)**
To inject structured response objects into the OpenAPI `responses` section, use the `x-responses` extension.

```yaml
descriptions:
  resource:
    post:
      x-responses:
        '409':
          description: Conflict
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
```

This ensures your client SDKs can generate specific exception classes for these error codes.
