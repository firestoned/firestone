+++
title = "Client & Server Generation"
weight = 4
description = "Using Firestone outputs to drive code generation tools."
+++

## The Generation Pipeline

Firestone produces standard specifications (OpenAPI, AsyncAPI) as artifacts. These artifacts are the fuel for downstream code generation tools.

**The Workflow:**
1.  **Design:** Define resource in Firestone YAML.
2.  **Spec:** `firestone generate ... openapi > spec.yaml`
3.  **Code:** `openapi-generator generate -i spec.yaml ...`

**Recommended Tools:**

*   **[OpenAPI Generator](https://openapi-generator.tech/)**: The industry standard. Supports 50+ languages.
    *   *Client SDKs:* Python, TypeScript, Java, Swift.
    *   *Server Stubs:* FastAPI, Spring Boot, Go Gin.
*   **[AsyncAPI Generator](https://www.asyncapi.com/tools/generator)**: For event-driven code.
    *   *Outputs:* Node.js, Python, Java event handlers.

Firestone focuses on creating the *perfect spec* so these tools can generate the *perfect code*.
