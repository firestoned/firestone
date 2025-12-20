+++
title = "Resource Schema"
weight = 20
description = "Master the core of Firestone: defining your APIs and data models using a powerful, JSON Schema-based resource blueprint."
+++

## The Heart of Firestone: Resource Definitions

At the core of `firestone` lies the concept of a **resource schema**: a declarative blueprint that defines your API's data models, available operations (GET, POST, etc.), and overall structure. This schema is your single source of truth, from which `firestone` automatically generates OpenAPI specifications, AsyncAPI specifications, CLI tools, and Streamlit UIs.

This section is dedicated to mastering the `firestone` resource schema syntax. By understanding how to effectively define your resources, you gain unparalleled control over the generated output, ensuring consistency, reducing boilerplate, and accelerating your API development workflow.

## What You'll Learn Here

This section provides a comprehensive guide to defining resources using `firestone`'s schema.

### 1. [API Versioning](./apiversion)
Understanding and defining the API version for your resources.

### 2. [AsyncAPI Configuration](./asyncapi)
How to embed AsyncAPI-specific configurations within your resource schema for event-driven APIs.

### 3. [Key Definitions](./key)
Defining primary keys and unique identifiers for your resources.

### 4. [Descriptions](./descriptions)
Adding human-readable descriptions to your resources, properties, and methods for better documentation.

### 5. [Items Schema](./items)
Defining the schema for individual items within a collection-based resource.

### 6. [Kind and Metadata](./kind)
Understanding the `kind` field and other metadata for resource identification.

### 7. [Methods Configuration](./methods)
Specifying the HTTP methods (GET, POST, PUT, DELETE, etc.) available for your resources and instances.

### 8. [Query Parameters](./query-params)
Defining custom query parameters for filtering, sorting, and pagination.

### 9. [Schema Object](./schema)
The core JSON Schema object where you define the structure and validation rules for your resource's data.

### 10. [Security Definitions](./security)
Integrating security schemes (API keys, OAuth2, etc.) directly into your resource schema.

### 11. [Schema Composition](./schema-composition)
Using `allOf`, `anyOf`, and `oneOf` for advanced data modeling.

### 12. [Complex Nested Resources](./complex-nested-resources)
Strategies for handling deep object hierarchies.

### 13. [Common Schema Mistakes](./common-schema-mistakes)
Troubleshooting guide for frequent errors.

### 14. [Version in Path](./version-in-path)
Controlling whether the API version is included in the URL path.

## Next Steps

Ready to design your API's foundation?
- **Next:** Start with **[API Versioning](./apiversion)**.