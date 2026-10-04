+++
title = "Security Schemes"
weight = 5
description = "Defining reusable security definitions in your Firestone blueprints."
+++

## Defining Security Schemes

Firestone lets you define security schemes (like API keys or bearer tokens) in your resource schema, under `security.scheme`. Each scheme is copied into the `components/securitySchemes` section of the generated OpenAPI specification, and schemes from every resource are kept.

**Example (Bearer Token):**
```yaml
security:
  scheme:
    bearer_auth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

The fields inside each scheme follow the **[OpenAPI Specification: Security Scheme Object](https://spec.openapis.org/oas/v3.0.3#security-scheme-object)**.

## Choosing Which Methods Are Secured

Next to `scheme`, you can list the HTTP methods to secure at each level of the resource:

- `resource`: the collection, e.g. `GET /books` and `POST /books`
- `instance`: one item, e.g. `GET /books/{book_id}`
- `instance_attrs`: one attribute of an item, e.g. `GET /books/{book_id}/title`

The rules for each level are:

- **No list:** every method at that level is secured.
- **A list:** only the methods listed are secured.
- **An empty list (`[]`):** no method at that level is secured.

**Secure everything:**
```yaml
security:
  scheme:
    bearer_auth:
      type: http
      scheme: bearer
```

**Leave reads open, secure writes:**
```yaml
security:
  scheme:
    bearer_auth:
      type: http
      scheme: bearer
  resource:
    - post
  instance:
    - delete
    - put
  instance_attrs: []
```

Here, `GET /books` and `GET /books/{book_id}` are open, creating, updating and deleting need a token, and the attribute endpoints are open.

## More Than One Scheme

When you list several schemes, a request that satisfies **any one** of them is accepted:

```yaml
security:
  scheme:
    bearer_auth:
      type: http
      scheme: bearer
    api_key:
      type: apiKey
      in: header
      name: X-API-Key
```

Each secured operation then accepts either a bearer token or an API key.
