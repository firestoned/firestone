+++
title = "OpenAPI Spec Structure"
linkTitle = "Spec Structure"
weight = 3
description = "Mapping Firestone resource blueprints to OpenAPI 3.x components."
+++

## From Blueprint to OpenAPI

Firestone automates the creation of a verbose OpenAPI 3.x specification from your concise resource blueprint. Understanding this mapping helps you predict the output.

**Mapping Reference:**

| Firestone Resource Field | OpenAPI 3.x Section |
| :--- | :--- |
| **`kind`** | **`tags`** (Groups operations) |
| **`methods`** | **`paths`** (Defines `/resource` and `/resource/{id}` endpoints) |
| **`schema.items`** | **`components/schemas`** (Reusable data models) |
| **`default_query_params`** | **`components/parameters`** |
| **`security`** | **`security`** (Global or operation-level) |
| **`metadata.description`** | **`info.description`** or Tag description |

**Key Benefit:**
Firestone handles the repetitive boilerplate of defining schemas, references (`$ref`), and standard error responses, ensuring your spec is always syntactically valid and structure-compliant.

For a detailed reference of the target specification format:
*   [**OpenAPI Specification 3.0.3**](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md)
*   [**OpenAPI Map (Visual Guide)**](https://openapi-map.apihandyman.io/)

