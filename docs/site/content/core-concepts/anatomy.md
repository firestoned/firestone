---
title: "Resource Schema Anatomy"
linkTitle: "Resource Schema Anatomy"
weight: 1
description: >
  Understanding the structure and sections of a firestone resource YAML file.
---

## Overview

A firestone resource file is a YAML document that combines **metadata** about your resource with a **JSON Schema** defining its structure. This document explains every section and how they work together.

## The Complete Structure

Here's a fully annotated resource file showing all major sections:

```yaml
# ============================================================================
# METADATA SECTION - Describes the resource
# ============================================================================

kind: addressbook                          # Resource name (becomes /addressbook in API)
apiVersion: v1                             # API version
metadata:
  description: An addressbook resource     # Human-readable description
versionInPath: false                       # Include version in URL? (/v1/addressbook)

# ============================================================================
# DEFAULT QUERY PARAMETERS - Available on all operations
# ============================================================================

default_query_params:
  - name: limit
    description: Maximum number of items to return
    in: query
    schema:
      type: integer
      default: 20

  - name: offset
    description: Number of items to skip
    in: query
    schema:
      type: integer
      default: 0

# ============================================================================
# ASYNCAPI CONFIGURATION - For WebSocket channel generation
# ============================================================================

asyncapi:
  servers:
    dev:
      url: ws://localhost
      protocol: ws
      description: Development WebSocket server
  channels:
    resources: true         # Generate channel for /addressbook
    instances: true         # Generate channel for /addressbook/{id}
    instance_attrs: true    # Generate channels for /addressbook/{id}/field

# ============================================================================
# DESCRIPTIONS - Human-readable operation descriptions
# ============================================================================

descriptions:
  resource:
    get: List all addresses in this addressbook
    post: Create a new address in this addressbook
    delete: Delete all addresses from this addressbook
  instance:
    get: Get a specific address from this addressbook
    put: Update an existing address in this addressbook
    delete: Delete an address from this addressbook

# ============================================================================
# METHODS - Which HTTP operations to expose
# ============================================================================

methods:
  resource:                # Operations on /addressbook
    - get
    - post
  instance:               # Operations on /addressbook/{address_key}
    - get
    - put
    - delete
  instance_attrs:         # Operations on /addressbook/{address_key}/field
    - get
    - put

# ============================================================================
# SECURITY - Authentication/authorization schemes
# ============================================================================

security:
  scheme:
    bearer_auth:
      scheme: bearer
      type: http
      bearerFormat: JWT
  resource:               # Which resource operations require auth
    - post
  instance:               # Which instance operations require auth
    - put
    - delete

# ============================================================================
# SCHEMA - The core JSON Schema definition
# ============================================================================

schema:
  type: array             # This resource is a collection

  # --------------------------------------------------------------------------
  # KEY - Unique identifier for instances
  # --------------------------------------------------------------------------

  key:
    name: address_key
    description: A unique identifier for an addressbook entry
    schema:
      type: string

  # --------------------------------------------------------------------------
  # QUERY PARAMETERS - Resource-specific filtering
  # --------------------------------------------------------------------------

  query_params:
    - name: city
      description: Filter by city name
      required: false
      schema:
        type: string
      methods:              # Only available on these methods
        - get

  # --------------------------------------------------------------------------
  # ITEMS - The actual resource schema
  # --------------------------------------------------------------------------

  items:
    type: object
    properties:
      address_key:
        expose: false       # Don't expose as URL attribute endpoint
        description: A unique identifier
        schema:
          type: string

      street:
        description: The street and civic number
        type: string

      city:
        description: The city
        type: string

      state:
        description: The state
        type: string

      country:
        description: The country
        type: string

      addrtype:
        description: The address type
        type: string
        enum:
          - work
          - home

      people:
        description: A list of people living there
        type: array
        items:
          type: string

      is_valid:
        description: Whether this address is valid
        type: boolean

    # Required fields for creation
    required:
      - street
      - city
      - state
      - country
```

## Section Breakdown

Let's explore each section in detail.

### Metadata Section

```yaml
kind: addressbook
apiVersion: v1
metadata:
  description: An addressbook resource
versionInPath: false
```

**kind** (required)
- The resource name
- Becomes the base URL path (e.g., `/addressbook`)
- Should be plural for collections (books, users, addresses)
- Must be a valid URL path segment

**apiVersion** (required)
- Semantic version of your resource definition
- Format: `v1`, `v1.2`, `v1.2.3`
- Used if `versionInPath` is true

**metadata.description** (optional but recommended)
- Human-readable description of the resource
- Appears in generated documentation
- Keep it concise (1-2 sentences)

**versionInPath** (optional, default: false)
- If `true`, includes version in URL: `/v1/addressbook`
- If `false`, URL is just `/addressbook`
- Useful for API versioning strategies

### Default Query Parameters

```yaml
default_query_params:
  - name: limit
    description: Maximum number to return
    in: query
    schema:
      type: integer
      default: 20
```

These parameters are added to **all** operations unless you specify specific methods.

**Fields:**
- `name` - Parameter name
- `description` - What the parameter does
- `in` - Always `query` for query params
- `schema` - JSON Schema for the parameter type
- `default` - Default value if not provided
- `methods` (optional) - Limit to specific HTTP methods

**Use cases:**
- Pagination (limit, offset)
- Sorting (sort, order)
- Common filters (active, status)
- Output formatting (format, fields)

### AsyncAPI Configuration

```yaml
asyncapi:
  servers:
    dev:
      url: ws://localhost
      protocol: ws
      description: Development server
  channels:
    resources: true
    instances: true
    instance_attrs: true
```

Controls AsyncAPI spec generation for WebSocket channels.

**servers** - WebSocket server definitions
- Each server has a name (`dev`, `prod`, etc.)
- `url` - WebSocket server URL
- `protocol` - Usually `ws` or `wss`
- `description` - Server purpose

**channels** - Which channels to generate
- `resources: true` - Channel for collection (e.g., `/addressbook`)
- `instances: true` - Channel for instances (e.g., `/addressbook/{id}`)
- `instance_attrs: true` - Channels for attributes (e.g., `/addressbook/{id}/city`)

Only include `asyncapi` if you're generating AsyncAPI specs.

### Descriptions

```yaml
descriptions:
  resource:
    get: List all addresses
    post: Create a new address
  instance:
    get: Get a specific address
    put: Update an address
    delete: Delete an address
```

Provides human-readable descriptions for each operation.

**Structure:**
- `resource` - Descriptions for collection operations
- `instance` - Descriptions for individual resource operations
- `instance_attrs` - Descriptions for attribute operations

**Best practices:**
- Start with a verb (List, Create, Update, Delete, Get)
- Be specific about what's happening
- Keep it short (one sentence)
- These appear in Swagger UI and generated docs

### Methods

```yaml
methods:
  resource:
    - get
    - post
  instance:
    - get
    - put
    - delete
  instance_attrs:
    - get
    - put
```

Defines which HTTP methods are available.

**resource** - Operations on the collection
- `get` - List resources (GET /addressbook)
- `post` - Create resource (POST /addressbook)
- `delete` - Delete all (DELETE /addressbook) - rarely used
- `patch` - Bulk update (PATCH /addressbook) - rarely used
- `head` - Metadata only (HEAD /addressbook)

**instance** - Operations on individual resources
- `get` - Retrieve (GET /addressbook/{id})
- `put` - Update/replace (PUT /addressbook/{id})
- `patch` - Partial update (PATCH /addressbook/{id})
- `delete` - Remove (DELETE /addressbook/{id})
- `head` - Metadata (HEAD /addressbook/{id})

**instance_attrs** - Operations on resource attributes
- `get` - Get field value (GET /addressbook/{id}/city)
- `put` - Update field (PUT /addressbook/{id}/city)
- `delete` - Clear field (DELETE /addressbook/{id}/city)
- `head` - Field metadata (HEAD /addressbook/{id}/city)

**Common patterns:**

*Read-only API:*
```yaml
methods:
  resource: [get]
  instance: [get]
```

*Full CRUD:*
```yaml
methods:
  resource: [get, post]
  instance: [get, put, delete]
```

*Create and list only:*
```yaml
methods:
  resource: [get, post]
  instance: []
```

### Security

```yaml
security:
  scheme:
    bearer_auth:
      scheme: bearer
      type: http
      bearerFormat: JWT
  resource:
    - post
  instance:
    - put
    - delete
```

Defines authentication/authorization requirements.

**scheme** - Security scheme definitions
- Key is the scheme name (e.g., `bearer_auth`)
- `type` - Usually `http`, `apiKey`, or `oauth2`
- `scheme` - For HTTP: `bearer`, `basic`, etc.
- `bearerFormat` - Token format (e.g., JWT)

**resource** - Which resource methods require auth
- List HTTP methods that need authentication
- Example: Require auth to create resources

**instance** - Which instance methods require auth
- List HTTP methods that need authentication
- Example: Require auth to update or delete

**instance_attrs** - Which attribute methods require auth
- List HTTP methods that need authentication

If omitted, no authentication is required (public API).

See [Security Reference](../../resource-schema/security/) for all security schemes.

### Schema Section

The `schema` section is the heart of your resource definition. It's pure JSON Schema with a few firestone-specific extensions.

```yaml
schema:
  type: array    # This resource is a collection
  key:           # Unique identifier
    name: address_key
    schema:
      type: string
  items:         # The resource structure
    type: object
    properties:
      # ... fields ...
```

**type** - Must be `array` for collections

**key** - Unique identifier (required for array types)
- `name` - The field name (e.g., `id`, `uuid`, `address_key`)
- `description` - What this key represents
- `schema` - JSON Schema for the key type

**query_params** - Resource-specific query parameters
- Same structure as `default_query_params`
- Only apply to this resource
- Can specify which methods they apply to

**items** - The actual resource schema
- `type` - Usually `object`
- `properties` - All fields in the resource
- `required` - List of required fields

#### Property Definition

Each property in `items.properties` can have:

```yaml
property_name:
  description: What this field represents
  type: string | integer | number | boolean | array | object
  enum: [value1, value2]        # Optional: allowed values
  default: some_value            # Optional: default value
  expose: true | false           # Optional: expose as URL attribute endpoint
  schema:                        # Optional: for nested resources
    $ref: "other.yaml#/schema"
```

**Standard JSON Schema fields:**
- `type` - Data type
- `description` - Field documentation
- `enum` - Allowed values
- `default` - Default value
- `minimum` / `maximum` - Numeric constraints
- `minLength` / `maxLength` - String constraints
- `pattern` - Regex validation
- `items` - For array types
- `properties` - For object types

**Firestone extensions:**
- `expose` - Whether to generate attribute endpoints (default: true)
- `schema.$ref` - Reference to nested resource definition

## How Sections Work Together

Here's how different sections interact:

```mermaid
graph TB
    A[kind + apiVersion] --> B[Base URL Path]
    B --> C[versionInPath?]
    C -->|Yes| D[/v1/addressbook]
    C -->|No| E[/addressbook]

    F[methods.resource] --> G[Collection Operations]
    H[methods.instance] --> I[Instance Operations]

    J[schema.key] --> K[Path Parameter]
    K --> I

    L[default_query_params] --> G
    L --> I
    M[schema.query_params] --> G
    M --> I

    N[security] --> O[Auth Requirements]
    O --> G
    O --> I

    P[descriptions] --> Q[API Documentation]
    Q --> G
    Q --> I
```

## Validation Rules

Firestone validates your resource file:

**Required sections:**
- `kind` must be present
- `apiVersion` must be present
- `schema` must be present
- `schema.type` must be `array`
- `schema.key` must be present for array types

**Consistency checks:**
- Methods in `descriptions` must exist in `methods`
- Methods in `security` must exist in `methods`
- Referenced fields in `query_params` should exist in `items.properties`

**JSON Schema validation:**
- `schema.items` must be valid JSON Schema
- Types must be valid JSON Schema types
- References must resolve

## Common Patterns

### Simple Resource

Minimal viable resource:

```yaml
kind: items
apiVersion: v1
metadata:
  description: A simple item collection
methods:
  resource: [get, post]
  instance: [get, put, delete]
schema:
  type: array
  key:
    name: item_id
    schema:
      type: string
  items:
    type: object
    properties:
      name:
        type: string
    required:
      - name
```

### Resource with Filtering

Add query parameters:

```yaml
schema:
  type: array
  query_params:
    - name: status
      description: Filter by status
      schema:
        type: string
        enum: [active, inactive]
      methods: [get]
  # ... rest of schema
```

### Nested Resource

Reference another resource:

```yaml
items:
  type: object
  properties:
    person:
      description: The person at this address
      schema:
        $ref: "person.yaml#/schema"
```

### Read-Only Resource

No modification operations:

```yaml
methods:
  resource: [get]
  instance: [get]
```

## Next Steps

Now that you understand resource file structure:

- **[Resource Types](./resource-types)** - Learn about different schema types
- **[Generation Outputs](../getting-started/outputs.md)** - See what firestone generates
- **[Resource Schema Reference](../../resource-schema/)** - Complete field documentation

