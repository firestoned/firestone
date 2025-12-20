+++
title = "Multi-Resource APIs"
weight = 4
description = "Structuring projects with multiple resource definitions."
+++

## Organizing Large Projects

Real-world APIs consist of many resources (`users`, `posts`, `comments`). Firestone is designed to handle this complexity through a modular file structure.

**Best Practice: One File Per Resource**
Avoid monolithic files. Create a dedicated directory:

```
project/
├── resources/
│   ├── users.yaml
│   ├── posts.yaml
│   ├── comments.yaml
│   └── common/
│       └── definitions.yaml
```

**Generating from a Directory:**
Firestone's CLI natively supports directory inputs. Pass the folder path to `--resources`:

```bash
firestone generate \
    --title "My Platform API" \
    --resources ./resources/ \
    openapi > openapi.yaml
```

Firestone will parse all valid resource files in the directory and merge them into a single, unified specification. This allows independent development of resources while maintaining a cohesive API surface.


# Best Practice: Structure and Manage Multi-Resource APIs

While a single resource schema is great for simple APIs, most real-world applications consist of multiple, interrelated resources (e.g., `users`, `posts`, and `comments`). Firestone is designed to handle this complexity, and following best practices for structuring your multi-resource project is crucial for maintainability and scalability.

## The "One Resource, One File" Principle

The most fundamental best practice for multi-resource APIs is to **define each resource in its own separate YAML file.**

-   **DO** have `users.yaml`, `posts.yaml`, and `comments.yaml`.
-   **DON'T** define all your resources in a single, monolithic `api.yaml`.

This approach provides several advantages:
-   **Clarity and Focus**: Each file has a single, clear purpose, making it easier to understand and edit.
-   **Reduced Cognitive Load**: Developers can focus on one resource at a time without being overwhelmed.
-   **Parallel Development**: Different teams or developers can work on different resource files simultaneously with a lower risk of merge conflicts.

## Project Structure Recommendation

We recommend organizing your resource schemas in a dedicated directory, such as `resources/` or `schemas/`, at the root of your project.

```
your-project/
├── resources/
│   ├── users.yaml
│   ├── posts.yaml
│   ├── comments.yaml
│   └── common.json  # Shared schema definitions
├── .firestone.yaml  # Project configuration (optional)
└── ...
```

## Generating from Multiple Files

When you're ready to generate your API specifications, you simply pass the directory containing your resource files to the `firestone generate` command using the `--resources` flag.

```bash
# Generate a single OpenAPI spec from all resource files
firestone generate \
    --title "My Multi-Resource API" \
    --resources ./resources/ \
    openapi > openapi.yaml
```

Firestone will intelligently combine all the schemas into a single, cohesive OpenAPI specification, complete with all the necessary paths, components, and relationships.

## Reusing Schemas with `$ref`

To avoid duplication and ensure consistency across your resources, you should define common or shared data structures in a separate file (e.g., `common.json`) and reference them using the standard JSON Schema `$ref` keyword.

For example, you might have a standard `Timestamp` or `UUID` format that you want to use in multiple resources.

**`resources/common.json`:**
```json
{
  "schemas": {
    "Timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "An ISO 8601 compliant timestamp."
    },
    "UUID": {
      "type": "string",
      "format": "uuid",
      "description": "A universally unique identifier."
    }
  }
}
```

**`resources/posts.yaml`:**
```yaml
kind: posts
apiVersion: v1
schema:
  type: array
  key:
    name: post_id
    schema:
      $ref: 'common.json#/schemas/UUID'
  items:
    type: object
    properties:
      created_at:
        $ref: 'common.json#/schemas/Timestamp'
      # ... other properties
```

By following these structuring practices, you can build large, complex, and maintainable APIs with Firestone while keeping your project organized and easy to navigate.
