+++
title = "Authentication Patterns"
linkTitle = "Authentication"
weight = 5
description = "Defining authentication schemes in Firestone and integrating with security proxies."
+++

## Authentication in Firestone

Firestone allows you to define the *contract* for authentication directly within your resource blueprints. By configuring the `security` block, you instruct Firestone to:

1.  **Generate OpenAPI Security Definitions:** Your security schemes (API Key, Bearer Token, OAuth2) are automatically added to the `components/securitySchemes` section of the OpenAPI spec.
2.  **Apply Security to Operations:** You can enforce specific security requirements globally, per-resource, or per-method (e.g., allow public `GET` but secured `POST`).

**Firestone Configuration Example:**
```yaml
security:
  scheme:
    bearer_auth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  resource:
    - post # Only secure the POST method for the resource collection
  instance:
    - put
    - delete
```

**Integration with `forevd`:**
While Firestone defines the auth contract, the `firestoned` ecosystem includes [**forevd**](https://github.com/firestoned/forevd), an authentication proxy that enforces these contracts. `forevd` handles the complexity of validation (JWT, mTLS, OIDC) so your generated API code remains focused on business logic.

For a deep dive into standard authentication patterns and security protocols, refer to these industry resources:

*   [**Authentication vs. Authorization (Auth0)**](https://auth0.com/docs/get-started/identity-fundamentals/authentication-and-authorization)
*   [**OAuth 2.0 Simplified**](https://www.oauth.com/)
*   [**JSON Web Tokens (JWT.io)**](https://jwt.io/introduction)
*   [**API Keys Best Practices (Google Cloud)**](https://cloud.google.com/docs/authentication/api-keys)

By defining your security requirements in Firestone, you ensure your API documentation and specifications accurately reflect your security posture.

---
## Next Steps

You've learned how to secure your APIs. Now, let's explore advanced techniques for managing and retrieving large datasets efficiently.
- **Next:** Dive into advanced data retrieval in **[Pagination and Filtering Beyond the Basics](./pagination-and-filtering-beyond-basics)**.
