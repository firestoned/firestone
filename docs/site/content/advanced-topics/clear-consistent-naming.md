+++
title = "Naming Conventions"
weight = 2
description = "How naming in your Firestone schema impacts your generated API, CLI, and code."
+++

## Naming in Firestone: Impact and Conventions

In Firestone, the names you choose in your resource schema are propagated everywhere. A single name in your YAML file determines URLs, CLI commands, variable names in generated code, and documentation headers.

**Firestone Mapping Reference:**

| Schema Field | Maps To... | Example |
| :--- | :--- | :--- |
| **`kind`** | **URL Path** (Collection) | `kind: users` -> `/users` |
| | **CLI Command Group** | `my-cli users ...` |
| | **Code Class Name** | `class UsersApi` |
| **`properties` (keys)** | **JSON Fields** | `{"first_name": "..."}` |
| | **CLI Options** | `--first-name` |
| | **Code Variables** | `user.first_name` |

**Recommended Style:**
*   **Resources (`kind`):** Plural nouns, kebab-case (e.g., `user-profiles`).
*   **Properties:** snake_case (e.g., `created_at`). This is standard for JSON and Python.

For comprehensive naming guidelines, refer to:

*   [**Google API Design Guide: Naming Conventions**](https://cloud.google.com/apis/design/naming_convention)
*   [**Microsoft REST API Guidelines: Naming**](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md)

Consistently applied naming conventions make your generated tools intuitive and predictable.
