+++
title = "Versioning Strategies"
linkTitle = "Versioning"
weight = 4
description = "Managing API evolution using Firestone's built-in versioning controls."
+++

## API Versioning with Firestone

Firestone provides built-in mechanisms to handle API versioning directly from your resource schema. This allows you to manage lifecycle changes declaratively.

**Core Fields:**

*   **`apiVersion`**: (Required) The semantic version of the resource definition (e.g., `v1`, `v2`).
*   **`versionInPath`**: (Optional) A boolean flag.
    *   `true`: Firestone prepends the `apiVersion` to the generated URL paths (e.g., `/v1/users`).
    *   `false`: The URL path remains clean (`/users`). You must handle versioning via headers or query parameters in your backend or gateway.

**Strategy: URL Path Versioning (Recommended)**
Enable `versionInPath: true` to adopt the most explicit and common versioning strategy.
1.  Define `apiVersion: v1` in `users_v1.yaml`. Output: `/v1/users`
2.  Define `apiVersion: v2` in `users_v2.yaml`. Output: `/v2/users`
3.  Generate a combined OpenAPI spec to support both versions concurrently during migration.

For a broader discussion on API versioning strategies (Header vs. URL vs. Query Param), consult these resources:

*   **[API Versioning (Stripe)](https://stripe.com/blog/api-versioning)** - Deep dive into rolling versions.
*   **[Rest API Versioning Strategies (RestfulAPI.net)](https://restfulapi.net/versioning/)** - Comparison of common patterns.
*   **[Google API Design: Versioning](https://cloud.google.com/apis/design/versioning)** - Guidelines for semantic versioning in APIs.

Firestone's configuration supports your chosen strategy while automating the tedious path rewriting.

