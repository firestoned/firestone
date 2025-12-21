+++
title = "Security Schemes"
weight = 5
description = "Defining reusable security definitions in your Firestone blueprints."
+++

## Defining Security Schemes

Firestone allows you to define reusable security schemes (like API Keys, OAuth2 flows, or OpenID Connect) directly in your resource schema using the `securitySchemes` block. These definitions are mapped directly to the `components/securitySchemes` section of the generated OpenAPI specification.

**Syntax:**
The syntax mirrors the OpenAPI Specification for Security Schemes.

**Example (API Key & Bearer Token):**
```yaml
securitySchemes:
  ApiKeyAuth:
    type: apiKey
    in: header
    name: X-API-Key
  BearerAuth:
    type: http
    scheme: bearer
    bearerFormat: JWT
```

**Applying Security:**
Once defined, you apply these schemes using the `security` keyword at the global, resource, or method level.

```yaml
security:
  - BearerAuth: [] # Applies to all methods by default
```

For a complete reference of supported fields and types (http, apiKey, oauth2, openIdConnect), refer to the **[OpenAPI Specification: Security Scheme Object](https://spec.openapis.org/oas/v3.0.3#security-scheme-object)**.
