---
title: "Schema Composition Patterns"
linkTitle: "Schema Composition"
weight: 51
description: >
  Combine and reuse schemas with allOf, anyOf, and oneOf for powerful, DRY resource definitions.
---

## Building Blocks: The Power of Composition

You've defined resource schemas with properties and validation. But what if you have common fields across multiple resources? Or multiple valid structures for the same field?

JSON Schema provides **composition keywords** that let you combine schemas like building blocks:

- **`allOf`** - Must match ALL of the schemas (intersection)
- **`anyOf`** - Must match AT LEAST ONE schema (union)
- **`oneOf`** - Must match EXACTLY ONE schema (exclusive union)

These patterns let you write **DRY** (Don't Repeat Yourself) schemas and model complex validation logic elegantly.

## `allOf`: Combining Schemas (Intersection)

`allOf` means "this must match ALL of these schemas." It's perfect for:
- Extending a base schema with additional fields
- Combining common properties
- Adding constraints to existing schemas

### Example: Base + Extensions

Imagine you have a base `Person` schema and want to extend it for different types:

```yaml
# Common base properties
definitions:
  BasePerson:
    type: object
    properties:
      id:
        type: string
        format: uuid
      name:
        type: string
        minLength: 1
      email:
        type: string
        format: email
    required: [id, name, email]

# Employee extends BasePerson
kind: employees
apiVersion: v1
schema:
  type: array
  key:
    name: employee_id
    schema:
      type: string

  items:
    allOf:
      - $ref: '#/definitions/BasePerson'  # Include all base fields
      - type: object                      # Add employee-specific fields
        properties:
          employee_number:
            type: string
          department:
            type: string
          hire_date:
            type: string
            format: date
        required:
          - employee_number
          - department
```

**What this means:**

An employee must have:
- `id`, `name`, `email` (from BasePerson)
- `employee_number`, `department` (employee-specific)

The resulting schema is the **intersection** of all schemas in the `allOf` array.

### Example: Adding Validation Constraints

You can use `allOf` to layer additional validation on top of a base type:

```yaml
properties:
  username:
    allOf:
      - type: string
      - minLength: 3
        maxLength: 20
      - pattern: '^[a-z0-9_]+$'  # Lowercase alphanumeric + underscore
      - not:
          enum: [admin, root, system]  # Forbidden values
```

Each schema in `allOf` adds a constraint. The username must satisfy ALL of them.

## `anyOf`: At Least One Match (Union)

`anyOf` means "this must match AT LEAST ONE of these schemas." Use it when:
- A field can have multiple valid formats
- You want flexible validation
- You're modeling unions of types

### Example: Multiple Contact Methods

A contact field can be either an email OR a phone number (or both):

```yaml
properties:
  contact:
    anyOf:
      - type: object
        properties:
          email:
            type: string
            format: email
        required: [email]

      - type: object
        properties:
          phone:
            type: string
            pattern: '^\+?[1-9]\d{1,14}$'
        required: [phone]

      - type: object
        properties:
          email:
            type: string
            format: email
          phone:
            type: string
            pattern: '^\+?[1-9]\d{1,14}$'
        required: [email, phone]
```

**Valid inputs:**
```json
{"contact": {"email": "user@example.com"}}
{"contact": {"phone": "+12345678901"}}
{"contact": {"email": "user@example.com", "phone": "+12345678901"}}
```

All three are valid because each matches at least one schema.

### Example: Flexible Value Types

Allow a field to be either a string or a number:

```yaml
properties:
  quantity:
    anyOf:
      - type: integer
        minimum: 0
      - type: string
        pattern: '^\d+$'
```

**Valid inputs:**
```json
{"quantity": 42}
{"quantity": "42"}
```

Both validate successfully.

## `oneOf`: Exactly One Match (Exclusive Union)

`oneOf` means "this must match EXACTLY ONE of these schemas." It's stricter than `anyOf`—if multiple schemas match, validation fails.

Use `oneOf` when:
- You have mutually exclusive options
- You want to enforce polymorphic types
- You need a discriminated union

### Example: Payment Methods

A payment can be EITHER credit card OR bank transfer, but not both:

```yaml
kind: payments
apiVersion: v1
schema:
  type: array
  key:
    name: payment_id
    schema:
      type: string

  items:
    type: object
    properties:
      amount:
        type: number
        minimum: 0

      method:
        type: string
        enum: [credit_card, bank_transfer]

      payment_details:
        oneOf:
          - type: object  # Credit card
            properties:
              card_number:
                type: string
                pattern: '^\d{16}$'
              expiry_month:
                type: integer
                minimum: 1
                maximum: 12
              expiry_year:
                type: integer
              cvv:
                type: string
                pattern: '^\d{3,4}$'
            required: [card_number, expiry_month, expiry_year, cvv]

          - type: object  # Bank transfer
            properties:
              account_number:
                type: string
              routing_number:
                type: string
              account_holder:
                type: string
            required: [account_number, routing_number, account_holder]

    required: [amount, method, payment_details]
```

**Valid:**
```json
{
  "amount": 100.00,
  "method": "credit_card",
  "payment_details": {
    "card_number": "1234567812345678",
    "expiry_month": 12,
    "expiry_year": 2025,
    "cvv": "123"
  }
}
```

**Invalid:**
```json
{
  "amount": 100.00,
  "method": "credit_card",
  "payment_details": {
    "card_number": "1234567812345678",
    "account_number": "9876543210"  // ❌ Matches BOTH schemas
  }
}
```

### Example: Discriminated Unions with `discriminator`

For better API documentation, combine `oneOf` with OpenAPI's `discriminator`:

```yaml
properties:
  shape:
    oneOf:
      - type: object
        properties:
          type:
            const: circle
          radius:
            type: number
        required: [type, radius]

      - type: object
        properties:
          type:
            const: rectangle
          width:
            type: number
          height:
            type: number
        required: [type, width, height]

    discriminator:
      propertyName: type
      mapping:
        circle: '#/definitions/Circle'
        rectangle: '#/definitions/Rectangle'
```

The `discriminator` tells API clients: "Look at the `type` field to determine which schema applies."

## Combining Composition Keywords

You can nest and combine these keywords for sophisticated validation:

```yaml
# A user must be either an admin OR (a regular user with an email)
allOf:
  - type: object
    properties:
      id: {type: string}
      name: {type: string}
    required: [id, name]

  - oneOf:
      - type: object
        properties:
          role:
            const: admin
        required: [role]

      - type: object
        properties:
          role:
            const: user
          email:
            type: string
            format: email
        required: [role, email]
```

**Valid:**
```json
{"id": "1", "name": "Alice", "role": "admin"}
{"id": "2", "name": "Bob", "role": "user", "email": "bob@example.com"}
```

**Invalid:**
```json
{"id": "3", "name": "Charlie", "role": "user"}  // ❌ Missing email
```

## Real-World Pattern: API Versioning

Use composition to support multiple API versions:

```yaml
kind: resources
apiVersion: v1
definitions:
  ResourceV1:
    type: object
    properties:
      name: {type: string}
      value: {type: string}

  ResourceV2:
    type: object
    properties:
      name: {type: string}
      value: {type: number}
      unit: {type: string}

schema:
  type: array
  key:
    name: resource_id
    schema:
      type: string

  items:
    oneOf:
      - allOf:
          - $ref: '#/definitions/ResourceV1'
          - type: object
            properties:
              api_version: {const: "v1"}
      - allOf:
          - $ref: '#/definitions/ResourceV2'
          - type: object
            properties:
              api_version: {const: "v2"}
```

Clients can send either v1 or v2 format, identified by `api_version`.

## Common Pitfalls and Solutions

### Pitfall 1: `oneOf` Ambiguity

**Problem**: Multiple schemas match, causing validation to fail.

```yaml
oneOf:
  - type: object
    properties:
      email: {type: string}
  - type: object
    properties:
      email: {type: string}
      phone: {type: string}
```

Sending `{"email": "test@example.com"}` matches BOTH schemas!

**Solution**: Make schemas mutually exclusive:

```yaml
oneOf:
  - type: object
    properties:
      email: {type: string}
    required: [email]
    additionalProperties: false  # No other properties allowed

  - type: object
    properties:
      email: {type: string}
      phone: {type: string}
    required: [email, phone]
    additionalProperties: false
```

### Pitfall 2: `allOf` Contradictions

**Problem**: Schemas in `allOf` contradict each other.

```yaml
allOf:
  - type: string
  - type: number
```

Nothing can be both a string AND a number. This schema is impossible to satisfy.

**Solution**: Ensure all schemas in `allOf` are compatible. Use `allOf` to **add** constraints, not to change types.

### Pitfall 3: Performance with Deep Nesting

**Problem**: Deeply nested composition can slow down validation.

```yaml
allOf:
  - allOf:
      - allOf:
          - type: object
```

**Solution**: Flatten when possible:

```yaml
allOf:
  - type: object
  - properties: {...}
  - required: [...]
```

## Best Practices

### 1. **Use `allOf` for Extension**
When you have a base schema and want to add fields:

```yaml
allOf:
  - $ref: '#/definitions/BaseResource'
  - type: object
    properties:
      extra_field: {type: string}
```

### 2. **Use `oneOf` for Polymorphism**
When you have mutually exclusive types:

```yaml
oneOf:
  - $ref: '#/definitions/TypeA'
  - $ref: '#/definitions/TypeB'
```

### 3. **Use `anyOf` Sparingly**
`anyOf` is flexible but can be confusing. Prefer `oneOf` when possible for clarity.

### 4. **Add Discriminators**
For `oneOf`, use `discriminator` to improve generated API docs:

```yaml
oneOf:
  - ...
discriminator:
  propertyName: type
```

### 5. **Document Your Intent**
Add descriptions explaining WHY you're using composition:

```yaml
payment_details:
  description: |
    Payment details. Must be either credit card OR bank transfer.
    Use the 'method' field to indicate which type.
  oneOf:
    - $ref: '#/definitions/CreditCardDetails'
    - $ref: '#/definitions/BankTransferDetails'
```

## Testing Composition Schemas

Always test edge cases:

```bash
# Test that ALL schemas in allOf are required
# Test that ONLY ONE schema in oneOf matches
# Test that AT LEAST ONE schema in anyOf matches
# Test invalid combinations
```

Use Firestone's Swagger UI server to interactively test:

```bash
firestone generate \
  --resources resource.yaml \
  openapi \
  --ui-server
```

Try submitting various payloads and see which ones validate.

## Next Steps

You've mastered schema composition. Explore:

- **[Schema References](../../advanced-topics/schema-references-and-reuse.md)** - Reuse schemas with `$ref`
- **[Validation Best Practices](../../advanced-topics/json-schema-validation.md)** - Write robust validation
- **[Complex Nested Resources](./complex-nested-resources/)** - Deep nesting patterns

---

**Remember**: Composition is powerful, but keep it simple. If your composition logic requires a PhD to understand, you've gone too far. Aim for clarity over cleverness.
