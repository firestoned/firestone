---
title: "Common Patterns Cheat Sheet"
linkTitle: "Cheat Sheet"
weight: 4
description: >
  Copy-paste patterns for common firestone scenarios. Quick reference for schemas, validation, and best practices.
---

## Overview

This cheat sheet provides ready-to-use YAML patterns for common scenarios. Copy, paste, and customize for your needs.

**How to use:**
1. Find the pattern you need
2. Copy the YAML snippet
3. Customize field names and values
4. Add to your resource definition

---

## Basic Resource Templates

### Minimal Resource

Simplest possible resource definition:

```yaml
kind: items
apiVersion: v1

methods:
  resource: [get, post]
  instance: [get, put, delete]

schema:
  type: array
  key:
    name: id
    schema: {type: string, format: uuid}
  items:
    type: object
    properties:
      name: {type: string}
    required: [name]
```

---

### Complete Resource

Full-featured resource with all common fields:

```yaml
kind: users
apiVersion: v1

metadata:
  description: User management API
  version: "1.0.0"
  version_in_path: false

methods:
  resource: [get, post]
  instance: [get, put, delete]

descriptions:
  resource:
    get: List all users
    post: Create new user
  instance:
    get: Get user details
    put: Update user
    delete: Delete user

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
      description: Filter by status
      required: false
      schema:
        type: string
        enum: [active, inactive]
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
        description: Email address

      created_at:
        type: string
        format: date-time
        description: Account creation time

    required: [name, email]

security:
  scheme:
    bearer_auth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  resource: [post]
  instance: [put, delete]
```

---

## Key Patterns

### UUID Key

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

### Slug Key

```yaml
key:
  name: slug
  description: URL-friendly identifier
  schema:
    type: string
    pattern: '^[a-z0-9]+(?:-[a-z0-9]+)*$'
    minLength: 3
    maxLength: 50
```

### Composite Key (Not Directly Supported)

*Workaround: Use single string key with delimiter*

```yaml
key:
  name: composite_id
  description: "Format: tenant_id:resource_id"
  schema:
    type: string
    pattern: '^[a-z0-9-]+:[a-z0-9-]+$'
```

---

## String Field Patterns

### Simple String

```yaml
name:
  type: string
  minLength: 1
  maxLength: 100
  description: Name
```

### Email

```yaml
email:
  type: string
  format: email
  maxLength: 254
  description: Email address
```

### URL

```yaml
website:
  type: string
  format: uri
  description: Website URL
```

### Phone Number (E.164)

```yaml
phone:
  type: string
  pattern: '^\+?[1-9]\d{1,14}$'
  description: Phone number in E.164 format
```

### Username

```yaml
username:
  type: string
  pattern: '^[a-z0-9_]{3,20}$'
  minLength: 3
  maxLength: 20
  description: Alphanumeric username with underscores
```

### Password

```yaml
password:
  type: string
  minLength: 12
  maxLength: 128
  pattern: '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$'
  description: |
    Password must be 12-128 characters and contain:
    - At least one lowercase letter
    - At least one uppercase letter
    - At least one digit
    - At least one special character (@$!%*?&)
```

### SKU / Product Code

```yaml
sku:
  type: string
  pattern: '^[A-Z0-9-]+$'
  minLength: 5
  maxLength: 20
  description: Stock Keeping Unit (uppercase alphanumeric)
```

### Hex Color

```yaml
color:
  type: string
  pattern: '^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
  description: Hex color code (e.g., #FF5733)
```

### IPv4 Address

```yaml
ip_address:
  type: string
  format: ipv4
  description: IPv4 address
```

### UUID v4

```yaml
uuid:
  type: string
  format: uuid
  description: UUID v4 identifier
```

---

## Number Field Patterns

### Integer (Non-Negative)

```yaml
count:
  type: integer
  minimum: 0
  description: Count value
```

### Integer (Positive)

```yaml
quantity:
  type: integer
  minimum: 1
  description: Quantity (must be at least 1)
```

### Integer (Range)

```yaml
age:
  type: integer
  minimum: 0
  maximum: 150
  description: Age in years
```

### Price (Cents)

```yaml
price:
  type: integer
  minimum: 0
  description: Price in cents (e.g., 1999 = $19.99)
```

### Percentage (0-100)

```yaml
discount_percentage:
  type: integer
  minimum: 0
  maximum: 100
  description: Discount percentage
```

### Float with Precision

```yaml
rating:
  type: number
  minimum: 0
  maximum: 5
  multipleOf: 0.1
  description: Rating from 0 to 5 (one decimal place)
```

---

## Enum Patterns

### Simple Enum

```yaml
status:
  type: string
  enum: [draft, published, archived]
  description: Publication status
```

### Enum with Default

```yaml
priority:
  type: string
  enum: [low, medium, high, critical]
  default: medium
  description: Priority level
```

### Enum with Descriptions

```yaml
role:
  type: string
  enum: [user, moderator, admin]
  description: |
    User role:
    - user: Standard user with basic permissions
    - moderator: Can moderate content
    - admin: Full administrative access
```

---

## Date/Time Patterns

### Timestamp (Created/Updated)

```yaml
created_at:
  type: string
  format: date-time
  description: ISO 8601 timestamp of creation

updated_at:
  type: string
  format: date-time
  description: ISO 8601 timestamp of last update
```

### Date Only

```yaml
birth_date:
  type: string
  format: date
  description: Birth date (YYYY-MM-DD)
```

### Nullable Timestamp

```yaml
deleted_at:
  type: ['string', 'null']
  format: date-time
  description: Soft delete timestamp (null if not deleted)
```

---

## Boolean Patterns

### Simple Boolean

```yaml
is_active:
  type: boolean
  description: Whether the account is active
```

### Boolean with Default

```yaml
newsletter_opt_in:
  type: boolean
  default: false
  description: Opted in to newsletter
```

---

## Array Patterns

### Array of Strings

```yaml
tags:
  type: array
  items:
    type: string
    minLength: 1
    maxLength: 50
  maxItems: 20
  uniqueItems: true
  description: Tags
```

### Array of Numbers

```yaml
scores:
  type: array
  items:
    type: integer
    minimum: 0
    maximum: 100
  minItems: 1
  maxItems: 10
  description: Test scores
```

### Array of Objects

```yaml
line_items:
  type: array
  minItems: 1
  items:
    type: object
    properties:
      product_id: {type: string, format: uuid}
      quantity: {type: integer, minimum: 1}
      unit_price: {type: integer, minimum: 0}
    required: [product_id, quantity, unit_price]
  description: Order line items
```

### Array of Enums

```yaml
permissions:
  type: array
  items:
    type: string
    enum: [read, write, delete, admin]
  uniqueItems: true
  description: User permissions
```

---

## Nested Object Patterns

### Address

```yaml
address:
  type: object
  properties:
    street:
      type: string
      maxLength: 200
    city:
      type: string
      maxLength: 100
    state:
      type: string
      pattern: '^[A-Z]{2}$'
      description: Two-letter state code
    postal_code:
      type: string
      pattern: '^\d{5}(-\d{4})?$'
      description: ZIP code (5 or 9 digits)
    country:
      type: string
      pattern: '^[A-Z]{2}$'
      default: "US"
      description: Two-letter country code
  required: [street, city, postal_code, country]
  description: Mailing address
```

### Contact Information

```yaml
contact:
  type: object
  properties:
    name: {type: string, maxLength: 100}
    email: {type: string, format: email}
    phone: {type: string, pattern: '^\+?[1-9]\d{1,14}$'}
  required: [name, email]
  description: Contact details
```

### Metadata Object

```yaml
metadata:
  type: object
  additionalProperties: true
  description: Arbitrary key-value metadata
```

### Geolocation

```yaml
location:
  type: object
  properties:
    latitude:
      type: number
      minimum: -90
      maximum: 90
    longitude:
      type: number
      minimum: -180
      maximum: 180
  required: [latitude, longitude]
  description: GPS coordinates
```

---

## Query Parameter Patterns

### Pagination

```yaml
query_params:
  - name: limit
    description: Number of results to return
    required: false
    schema:
      type: integer
      minimum: 1
      maximum: 100
      default: 20
    methods: [get]

  - name: offset
    description: Number of results to skip
    required: false
    schema:
      type: integer
      minimum: 0
      default: 0
    methods: [get]
```

### Cursor Pagination

```yaml
query_params:
  - name: cursor
    description: Pagination cursor from previous response
    required: false
    schema:
      type: string
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
```

### Filtering

```yaml
query_params:
  - name: status
    description: Filter by status
    required: false
    schema:
      type: string
      enum: [active, inactive, pending]
    methods: [get]

  - name: created_after
    description: Filter by creation date
    required: false
    schema:
      type: string
      format: date-time
    methods: [get]
```

### Sorting

```yaml
query_params:
  - name: sort_by
    description: Field to sort by
    required: false
    schema:
      type: string
      enum: [created_at, name, price]
      default: created_at
    methods: [get]

  - name: sort_order
    description: Sort direction
    required: false
    schema:
      type: string
      enum: [asc, desc]
      default: desc
    methods: [get]
```

### Search

```yaml
query_params:
  - name: q
    description: Search query
    required: false
    schema:
      type: string
      minLength: 1
      maxLength: 100
    methods: [get]
```

### Range Filter

```yaml
query_params:
  - name: min_price
    description: Minimum price in cents
    required: false
    schema:
      type: integer
      minimum: 0
    methods: [get]

  - name: max_price
    description: Maximum price in cents
    required: false
    schema:
      type: integer
      minimum: 0
    methods: [get]
```

---

## Security Patterns

### Bearer Token (JWT)

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

### API Key in Header

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

### OAuth2

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
            read: Read access to resources
            write: Write access to resources
  resource: [get, post]
  instance: [get, put, delete]
```

### Multiple Security Schemes

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

## Validation Patterns

### Required vs Optional

```yaml
properties:
  required_field:
    type: string
    minLength: 1
  optional_field:
    type: string
required: [required_field]  # optional_field is optional
```

### Field with Default

```yaml
status:
  type: string
  enum: [draft, published]
  default: draft
```

### Conditional Required (allOf)

```yaml
# If type is "business", tax_id is required
allOf:
  - type: object
    properties:
      type: {type: string, enum: [individual, business]}
      tax_id: {type: string}
  - if:
      properties:
        type: {const: business}
    then:
      required: [tax_id]
```

---

## Real-World Examples

### User Resource

```yaml
kind: users
apiVersion: v1
schema:
  type: array
  key:
    name: user_id
    schema: {type: string, format: uuid}
  items:
    type: object
    properties:
      email: {type: string, format: email}
      name: {type: string, maxLength: 100}
      avatar_url: {type: string, format: uri}
      is_active: {type: boolean, default: true}
      created_at: {type: string, format: date-time}
    required: [email, name]
methods:
  resource: [get, post]
  instance: [get, put, delete]
```

### Product Resource

```yaml
kind: products
apiVersion: v1
schema:
  type: array
  key:
    name: product_id
    schema: {type: string, format: uuid}
  items:
    type: object
    properties:
      name: {type: string, maxLength: 200}
      sku: {type: string, pattern: '^[A-Z0-9-]+$'}
      price: {type: integer, minimum: 0, description: "Price in cents"}
      category: {type: string, enum: [electronics, clothing, books]}
      in_stock: {type: boolean}
      tags: {type: array, items: {type: string}, uniqueItems: true}
    required: [name, sku, price, category]
methods:
  resource: [get, post]
  instance: [get, put, delete]
```

### Order Resource

```yaml
kind: orders
apiVersion: v1
schema:
  type: array
  key:
    name: order_id
    schema: {type: string, format: uuid}
  items:
    type: object
    properties:
      customer_id: {type: string, format: uuid}
      status: {type: string, enum: [pending, confirmed, shipped, delivered]}
      line_items:
        type: array
        items:
          type: object
          properties:
            product_id: {type: string, format: uuid}
            quantity: {type: integer, minimum: 1}
            unit_price: {type: integer, minimum: 0}
          required: [product_id, quantity, unit_price]
      total: {type: integer, minimum: 0}
      created_at: {type: string, format: date-time}
    required: [customer_id, status, line_items, total]
methods:
  resource: [get, post]
  instance: [get, put]
```

---

## Copy-Paste Checklist

When using these patterns:

- [ ] Replace `kind` with your resource name (plural, lowercase)
- [ ] Update `key.name` to match your identifier field
- [ ] Customize property names and descriptions
- [ ] Adjust min/max values for your use case
- [ ] Add/remove `required` fields as needed
- [ ] Update enums to match your domain
- [ ] Add appropriate security if needed
- [ ] Test with `firestone generate` command

---

## See Also

- **[Resource Schema Reference](./resource-schema-quick-reference)** - Complete field reference
- **[CLI Command Reference](./cli-command-reference)** - Command syntax
- **[Examples](../examples/)** - Full working examples
- **[Best Practices](common-patterns-cheat-sheet.md)** - Recommended patterns
