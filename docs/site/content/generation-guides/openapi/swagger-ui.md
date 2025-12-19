+++
title = "Visualizing with Swagger UI"
linkTitle = "Swagger UI"
weight = 4
description = "Instant API visualization using Firestone's built-in Swagger UI server."
+++

## Instant Visualization

Firestone provides a built-in, zero-config way to visualize your API using [Swagger UI](https://swagger.io/tools/swagger-ui/). This is perfect for local development and rapid prototyping.

**Command:**
```bash
firestone generate --resources users.yaml openapi --ui-server
```

**What Happens:**
1.  Firestone generates the OpenAPI spec in memory.
2.  It launches a local web server (default: `http://127.0.0.1:8080`).
3.  It serves a pre-configured Swagger UI instance pointed at your generated spec.

## Hosting Swagger UI in Production

For production, you typically want to serve the documentation alongside your API.

1.  **Generate the Spec File:**
    ```bash
    firestone generate ... openapi > openapi.yaml
    ```
2.  **Serve with your Backend:** Most modern frameworks have easy integrations to serve this file via Swagger UI.
    *   **FastAPI:** Automatic (docs are built-in).
    *   **Flask/Django:** use libraries like `flasgger` or `drf-yasg`.
    *   **Static:** Use the [Swagger UI Docker image](https://hub.docker.com/r/swaggerapi/swagger-ui) and mount your `openapi.yaml`.

For advanced customization (theming, plugins, OAuth2 redirect handling), consult the **[Swagger UI Configuration Docs](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)**.
