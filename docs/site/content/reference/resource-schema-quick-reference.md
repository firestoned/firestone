---
title: "Resource Schema Quick Reference"
linkTitle: "Schema Reference"
weight: 2
description: >
  Field-by-field quick reference for resource YAML structure.
---

## Resource Schema Structure

```yaml
kind: <string>                    # Required
apiVersion: <string>              # Required
metadata:                         # Optional
  description: <string>
  version: <string>
  version_in_path: <boolean>
methods:                          # Required
  resource: [<http-methods>]
  instance: [<http-methods>]
descriptions:                     # Optional
  resource: {<method>: <string>}
  instance: {<method>: <string>}
schema:                           # Required
  type: array                     # Must be "array"
  key:                            # Required for instance methods
    name: <string>
    description: <string>
    schema: <json-schema>
  query_params: [...]             # Optional
  items:                          # Required
    type: object                  # Usually "object"
    properties: {...}
    required: [...]
default_query_params: [...]       # Optional
security:                         # Optional
  scheme: {...}
  resource: [<methods>]
  instance: [<methods>]
asyncapi:                         # Optional
  publish: <boolean>
  subscribe: <boolean>
```

---

## Top-Level Fields

### kind (Required)

**Type:** String
**Description:** Resource name used in API paths
**URL Format:** `/{kind}` and `/{kind}/{id}`

**Rules:**
- ✅ Lowercase
- ✅ Plural nouns recommended
- ✅ Alphanumeric + hyphens/underscores
- ❌ No spaces or special characters

**Examples:**
```yaml
kind: users              # → /users, /users/{user_id}
kind: blog-posts         # → /blog-posts, /blog-posts/{post_id}
kind: product_categories # → /product_categories, /product_categories/{category_id}
```

---

### apiVersion (Required)

**Type:** String
**Description:** Resource definition version
**Current:** Always `"v1"`

```yaml
apiVersion: v1  # Required, always "v1" currently
```

---

### metadata (Optional)

**Type:** Object
**Description:** Resource-level metadata

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | string | No | Human-readable description |
| `version` | string | No | Semantic version (e.g., "1.0.0") |
| `version_in_path` | boolean | No | Include version in URL path |

**Example:**
```yaml
metadata:
  description: User account management
  version: "2.1.0"
  version_in_path: false  # → /users (not /v2.1.0/users)
```

---

### methods (Required)

**Type:** Object
**Description:** HTTP methods to expose

**Structure:**
```yaml
methods:
  resource: [<methods>]   # Collection endpoint: /{kind}
  instance: [<methods>]   # Instance endpoint: /{kind}/{id}
```

**Valid HTTP Methods:**
- `get` - Retrieve resources
- `post` - Create resource
- `put` - Replace resource
- `patch` - Update resource
- `delete` - Delete resource

**Examples:**

```yaml
# Full CRUD
methods:
  resource: [get, post]
  instance: [get, put, delete]

# Read-only
methods:
  resource: [get]
  instance: [get]

# Create-only
methods:
  resource: [post]
  instance: []

# Custom operations
methods:
  resource: [get, post]
  instance: [get, patch]  # PATCH instead of PUT
```

---

### descriptions (Optional)

**Type:** Object
**Description:** Human-readable operation descriptions

**Structure:**
```yaml
descriptions:
  resource:
    get: "Description for GET /{kind}"
    post: "Description for POST /{kind}"
  instance:
    get: "Description for GET /{kind}/{id}"
    put: "Description for PUT /{kind}/{id}"
    delete: "Description for DELETE /{kind}/{id}"
```

**Example:**
```yaml
descriptions:
  resource:
    get: List all users with optional filtering
    post: Create a new user account
  instance:
    get: Retrieve detailed user information
    put: Update user account
    delete: Permanently delete user account
```

---

### schema (Required)

**Type:** Object
**Description:** JSON Schema definition for the resource

#### schema.type (Required)

**Must be:** `"array"`

```yaml
schema:
  type: array  # Always "array"
```

#### schema.key (Required for instance methods)

**Type:** Object
**Description:** Identifier field for instance endpoints

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ Yes | Key field name |
| `description` | string | No | Key description |
| `schema` | object | ✅ Yes | JSON Schema for key |

**Examples:**

```yaml
# UUID key
key:
  name: user_id
  description: Unique user identifier
  schema:
    type: string
    format: uuid

# Integer key
key:
  name: id
  schema:
    type: integer
    minimum: 1

# String slug
key:
  name: slug
  schema:
    type: string
    pattern: '^[a-z0-9-]+$'
    minLength: 3
    maxLength: 50
```

#### schema.items (Required)

**Type:** Object
**Description:** JSON Schema for resource objects

**Common Structure:**
```yaml
items:
  type: object
  properties:
    field_name:
      type: <type>
      description: <description>
      # ... validation rules
  required: [list, of, required, fields]
```

**Example:**
```yaml
items:
  type: object
  properties:
    name:
      type: string
      minLength: 1
      maxLength: 100
      description: User's full name

    email:
      type: string
      format: email
      maxLength: 254
      description: Email address

    age:
      type: integer
      minimum: 0
      maximum: 150
      description: User's age

    is_active:
      type: boolean
      default: true
      description: Account status

  required: [name, email]
```

#### schema.query_params (Optional)

**Type:** Array of objects
**Description:** Query parameters for filtering/pagination

**Structure:**
```yaml
query_params:
  - name: <param_name>
    description: <description>
    required: <boolean>
    schema: <json-schema>
    methods: [<http-methods>]
```

**Example:**
```yaml
query_params:
  - name: status
    description: Filter by status
    required: false
    schema:
      type: string
      enum: [active, inactive, pending]
    methods: [get]

  - name: limit
    description: Number of results
    required: false
    schema:
      type: integer
      minimum: 1
      maximum: 100
      default: 20
    methods: [get]

  - name: offset
    description: Pagination offset
    required: false
    schema:
      type: integer
      minimum: 0
      default: 0
    methods: [get]
```

---

### default_query_params (Optional)

**Type:** Array of objects
**Description:** Query parameters added to all GET requests

**Example:**
```yaml
default_query_params:
  - name: limit
    schema:
      type: integer
      default: 20

  - name: offset
    schema:
      type: integer
      default: 0
```

---

### security (Optional)

**Type:** Object
**Description:** Security scheme definitions and requirements

**Structure:**
```yaml
security:
  scheme:
    <scheme_name>:
      type: <type>
      # ... scheme-specific fields
  resource: [<methods>]   # Methods requiring auth on /{kind}
  instance: [<methods>]   # Methods requiring auth on /{kind}/{id}
```

**Security Scheme Types:**

#### HTTP Bearer (JWT)
```yaml
security:
  scheme:
    bearer_auth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  resource: [post]
  instance: [put, delete]
```

#### API Key
```yaml
security:
  scheme:
    api_key:
      type: apiKey
      in: header
      name: X-API-Key
  resource: [get, post]
  instance: [get, put, delete]
```

#### OAuth2
```yaml
security:
  scheme:
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/oauth/authorize
          tokenUrl: https://auth.example.com/oauth/token
          scopes:
            read: Read access
            write: Write access
  resource: [get, post]
  instance: [get, put, delete]
```

#### Multiple Schemes
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
  resource: [post]  # Either bearer OR api_key required
  instance: [put, delete]
```

---

### asyncapi (Optional)

**Type:** Object
**Description:** AsyncAPI-specific configuration

**Fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `publish` | boolean | false | Enable publish operations |
| `subscribe` | boolean | false | Enable subscribe operations |

**Example:**
```yaml
asyncapi:
  publish: true    # Clients can publish to this resource
  subscribe: true  # Clients can subscribe to updates
```

---

## JSON Schema Types

Common JSON Schema types used in `schema.items.properties`:

### String

```yaml
field_name:
  type: string
  minLength: 1           # Optional
  maxLength: 100         # Optional
  pattern: '^[a-z]+$'    # Optional regex
  format: email          # Optional format
  enum: [val1, val2]     # Optional enumeration
  default: "value"       # Optional default
```

**Common Formats:**
- `email` - Email address
- `uri` - URI/URL
- `uuid` - UUID
- `date` - ISO 8601 date (YYYY-MM-DD)
- `date-time` - ISO 8601 datetime
- `ipv4` - IPv4 address
- `ipv6` - IPv6 address

### Number / Integer

```yaml
field_name:
  type: integer       # or "number" for floats
  minimum: 0          # Optional
  maximum: 100        # Optional
  multipleOf: 5       # Optional
  exclusiveMinimum: 0 # Optional
  default: 10         # Optional
```

### Boolean

```yaml
field_name:
  type: boolean
  default: false  # Optional
```

### Array

```yaml
field_name:
  type: array
  items:
    type: string       # or object, number, etc.
  minItems: 0          # Optional
  maxItems: 10         # Optional
  uniqueItems: true    # Optional
```

### Object

```yaml
field_name:
  type: object
  properties:
    nested_field:
      type: string
  required: [nested_field]
  additionalProperties: false  # Optional
```

### Null / Optional

```yaml
# Nullable field
field_name:
  type: [string, "null"]

# Optional field (not in required array)
properties:
  optional_field:
    type: string
required: []  # optional_field not listed
```

---

## Validation Keywords

Common JSON Schema validation keywords:

| Keyword | Types | Description | Example |
|---------|-------|-------------|---------|
| `minLength` | string | Minimum length | `minLength: 1` |
| `maxLength` | string | Maximum length | `maxLength: 100` |
| `pattern` | string | Regex pattern | `pattern: '^[A-Z]'` |
| `format` | string | String format | `format: email` |
| `enum` | any | Fixed values | `enum: [a, b, c]` |
| `minimum` | number | Minimum value | `minimum: 0` |
| `maximum` | number | Maximum value | `maximum: 100` |
| `exclusiveMinimum` | number | Exclusive min | `exclusiveMinimum: 0` |
| `exclusiveMaximum` | number | Exclusive max | `exclusiveMaximum: 100` |
| `multipleOf` | number | Multiple of | `multipleOf: 10` |
| `minItems` | array | Min array length | `minItems: 1` |
| `maxItems` | array | Max array length | `maxItems: 10` |
| `uniqueItems` | array | Unique items | `uniqueItems: true` |
| `required` | object | Required fields | `required: [name]` |
| `additionalProperties` | object | Allow extra props | `additionalProperties: false` |

---

## Complete Example

```yaml
kind: users
apiVersion: v1

metadata:
  description: User account management API
  version: "1.0.0"
  version_in_path: false

methods:
  resource: [get, post]
  instance: [get, put, delete]

descriptions:
  resource:
    get: List all users with optional filtering
    post: Create a new user account
  instance:
    get: Get user details
    put: Update user account
    delete: Delete user account

schema:
  type: array

  key:
    name: user_id
    description: Unique user identifier
    schema:
      type: string
      format: uuid

  query_params:
    - name: status
      description: Filter by account status
      required: false
      schema:
        type: string
        enum: [active, inactive, pending]
      methods: [get]

    - name: limit
      description: Number of results to return
      required: false
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20
      methods: [get]

  items:
    type: object
    properties:
      name:
        type: string
        minLength: 1
        maxLength: 100
        description: User's full name

      email:
        type: string
        format: email
        maxLength: 254
        description: Email address

      status:
        type: string
        enum: [active, inactive, pending]
        default: pending
        description: Account status

      age:
        type: integer
        minimum: 0
        maximum: 150
        description: User's age in years

      tags:
        type: array
        items:
          type: string
          minLength: 1
          maxLength: 50
        maxItems: 10
        uniqueItems: true
        description: User tags

    required: [name, email, status]

security:
  scheme:
    bearer_auth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  resource: [post]
  instance: [put, delete]

asyncapi:
  publish: false
  subscribe: true
```

---

## Common Patterns

### UUID Primary Key
```yaml
key:
  name: id
  schema:
    type: string
    format: uuid
```

### Integer Auto-Increment Key
```yaml
key:
  name: id
  schema:
    type: integer
    minimum: 1
```

### Slug/Handle Key
```yaml
key:
  name: slug
  schema:
    type: string
    pattern: '^[a-z0-9-]+$'
    minLength: 3
    maxLength: 50
```

### Timestamps
```yaml
created_at:
  type: string
  format: date-time
  description: Creation timestamp

updated_at:
  type: string
  format: date-time
  description: Last update timestamp
```

### Nested Address
```yaml
address:
  type: object
  properties:
    street: {type: string}
    city: {type: string}
    state: {type: string, pattern: '^[A-Z]{2}$'}
    postal_code: {type: string, pattern: '^\d{5}(-\d{4})?$'}
  required: [street, city, postal_code]
```

### Enum with Description
```yaml
status:
  type: string
  enum: [draft, published, archived]
  description: |
    Publication status:
    - draft: Not yet published
    - published: Publicly visible
    - archived: No longer active
```

---

## See Also

- **[Resource Schema Section](../core-concepts/resource-schema)** - Detailed field documentation
- **[CLI Command Reference](./cli-command-reference)** - Command syntax
- **[Examples](../examples/)** - Complete working examples
- **[Common Patterns Cheat Sheet](./common-patterns-cheat-sheet)** - Copy-paste patterns
