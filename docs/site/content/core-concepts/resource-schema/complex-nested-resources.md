---
title: "Complex Nested Resources"
linkTitle: "Nested Resources"
weight: 50
description: >
  Master deeply nested data structures and hierarchical relationships in your resource schemas.
---

## When Simple Isn't Enough

You've defined simple resources with basic properties. But what happens when your data model includes addresses with multiple lines, products with variants, or orders with line items? Real-world APIs often require **nested objects** and **hierarchical structures**.

Firestone handles this elegantly through JSON Schema's `object` and `array` types. Let's explore how to model complex, real-world data.

## Nested Objects: The Address Example

Imagine a `users` resource where each user has an address. Instead of flattening everything into top-level fields, you can nest the address structure:

```yaml
kind: users
apiVersion: v1
schema:
  type: array
  key:
    name: user_id
    schema:
      type: string
      format: uuid

  items:
    type: object
    properties:
      name:
        type: string
        description: User's full name

      email:
        type: string
        format: email

      # Nested object for address
      address:
        type: object
        description: User's mailing address
        properties:
          street:
            type: string
            description: Street address
          city:
            type: string
            description: City name
          state:
            type: string
            description: State or province
            pattern: '^[A-Z]{2}$'
          postal_code:
            type: string
            description: ZIP or postal code
          country:
            type: string
            description: Country code
            pattern: '^[A-Z]{2}$'
            default: "US"
        required:
          - street
          - city
          - postal_code

    required:
      - name
      - email
```

**What this generates:**

When you create a user, the request body looks like:

```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "address": {
    "street": "123 Main St",
    "city": "Springfield",
    "state": "IL",
    "postal_code": "62701",
    "country": "US"
  }
}
```

The OpenAPI spec automatically includes schemas for both `User` and the nested address structure.

## Arrays of Objects: The Order Line Items Example

A common pattern is a resource that contains an array of complex objects. For example, an order with multiple line items:

```yaml
kind: orders
apiVersion: v1
schema:
  type: array
  key:
    name: order_id
    schema:
      type: string
      format: uuid

  items:
    type: object
    properties:
      customer_id:
        type: string
        format: uuid
        description: Reference to customer

      order_date:
        type: string
        format: date-time
        description: When the order was placed

      # Array of complex objects
      line_items:
        type: array
        description: Items in this order
        items:
          type: object
          properties:
            product_id:
              type: string
              format: uuid
              description: Reference to product
            quantity:
              type: integer
              minimum: 1
              description: Number of units
            unit_price:
              type: number
              minimum: 0
              description: Price per unit in cents
            discount_percent:
              type: number
              minimum: 0
              maximum: 100
              default: 0
          required:
            - product_id
            - quantity
            - unit_price
        minItems: 1

      total_amount:
        type: number
        minimum: 0
        description: Total order amount in cents

    required:
      - customer_id
      - order_date
      - line_items
      - total_amount
```

**What this generates:**

```json
{
  "customer_id": "550e8400-e29b-41d4-a716-446655440000",
  "order_date": "2025-01-15T10:30:00Z",
  "line_items": [
    {
      "product_id": "c73bcdcc-2669-4bf6-81d3-e4ae73fb11fd",
      "quantity": 2,
      "unit_price": 1999,
      "discount_percent": 10
    },
    {
      "product_id": "a9b8c7d6-e5f4-3210-9876-543210fedcba",
      "quantity": 1,
      "unit_price": 4999
    }
  ],
  "total_amount": 8597
}
```

The generated OpenAPI spec will include:
- `Order` schema
- `LineItem` schema (reusable component)
- Proper validation for all nested fields

## Multiple Levels of Nesting

You can nest as deeply as needed. Here's a company with departments, teams, and employees:

```yaml
kind: companies
apiVersion: v1
schema:
  type: array
  key:
    name: company_id
    schema:
      type: string

  items:
    type: object
    properties:
      name:
        type: string

      # Level 1: Departments
      departments:
        type: array
        items:
          type: object
          properties:
            department_name:
              type: string

            # Level 2: Teams within departments
            teams:
              type: array
              items:
                type: object
                properties:
                  team_name:
                    type: string

                  # Level 3: Employees in teams
                  employees:
                    type: array
                    items:
                      type: object
                      properties:
                        employee_id:
                          type: string
                        name:
                          type: string
                        role:
                          type: string
                          enum: [manager, developer, designer, qa]
                      required:
                        - employee_id
                        - name
                        - role
```

**Three levels deep**, all properly validated and documented in the generated OpenAPI spec.

## Validation in Nested Structures

All JSON Schema validation keywords work within nested objects:

```yaml
properties:
  contact_info:
    type: object
    properties:
      primary_phone:
        type: string
        pattern: '^\+?[1-9]\d{1,14}$'  # E.164 format
        description: Primary phone number

      secondary_phone:
        type: string
        pattern: '^\+?[1-9]\d{1,14}$'

      emergency_contact:
        type: object
        properties:
          name:
            type: string
            minLength: 1
          relationship:
            type: string
            enum: [spouse, parent, sibling, friend, other]
          phone:
            type: string
            pattern: '^\+?[1-9]\d{1,14}$'
        required:
          - name
          - phone
    required:
      - primary_phone
```

The validation rules apply recursively through all levels.

## Best Practices for Nested Resources

### 1. **Don't Nest Too Deeply**
Three levels is usually the maximum for maintainability. Beyond that, consider splitting into separate resources with references.

**Bad:**
```yaml
company → divisions → departments → teams → projects → tasks → subtasks
```

**Better:**
```yaml
# Separate resources
companies:
  - divisions (with company_id reference)
departments:
  - teams (with department_id reference)
projects:
  - tasks (with project_id reference)
```

### 2. **Make Nested Objects Optional When Appropriate**
If a nested object is optional, don't include it in `required`:

```yaml
properties:
  shipping_address:
    type: object
    # Not in required - optional nested object

  billing_address:
    type: object
    # This one IS required

required:
  - billing_address
```

### 3. **Use Descriptions Liberally**
Nested structures can be complex. Help users understand:

```yaml
properties:
  metadata:
    type: object
    description: |
      Additional metadata for the resource. This is a flexible
      key-value structure for storing custom attributes that
      don't fit into the standard schema.
    additionalProperties:
      type: string
```

### 4. **Validate Array Lengths**
For arrays of objects, use `minItems` and `maxItems`:

```yaml
line_items:
  type: array
  minItems: 1     # At least one item
  maxItems: 100   # No more than 100 items
  items:
    type: object
    # ...
```

### 5. **Consider Default Values**
Nested objects can have defaults:

```yaml
properties:
  preferences:
    type: object
    default:
      theme: "light"
      notifications: true
    properties:
      theme:
        type: string
        enum: [light, dark]
        default: "light"
      notifications:
        type: boolean
        default: true
```

## Common Patterns

### Pattern 1: Polymorphic Objects with Discriminators
Different types of nested objects based on a type field:

```yaml
properties:
  payment_method:
    type: object
    properties:
      type:
        type: string
        enum: [credit_card, bank_account, paypal]

      # Type-specific fields
      credit_card_details:
        type: object
        # Only present when type=credit_card

      bank_account_details:
        type: object
        # Only present when type=bank_account
    required:
      - type
```

### Pattern 2: Extensible Metadata
A catch-all object for custom data:

```yaml
properties:
  metadata:
    type: object
    description: Custom key-value pairs
    additionalProperties:
      type: string
    example:
      source: "mobile_app"
      campaign_id: "summer_2025"
```

### Pattern 3: Versioned Nested Objects
Include version information within nested structures:

```yaml
properties:
  api_config:
    type: object
    properties:
      version:
        type: string
        enum: ["v1", "v2"]
      settings:
        type: object
        # Settings structure varies by version
```

## Troubleshooting Nested Resources

### Issue: "Required property missing" errors
**Cause**: You marked a nested property as required, but it's not being sent.

**Solution**: Check the `required` array at EACH level:

```yaml
items:
  type: object
  properties:
    address:
      type: object
      properties:
        street: {type: string}
        city: {type: string}
      required: [street, city]  # Required WITHIN address
  required: [address]  # address itself is required at top level
```

### Issue: Array validation failing
**Cause**: `minItems` or `maxItems` constraint violated.

**Solution**: Ensure your array has the right number of elements:

```yaml
line_items:
  type: array
  minItems: 1  # Must have at least one item!
  items:
    type: object
```

### Issue: Nested object showing as empty `{}`
**Cause**: All properties of the nested object are optional, and none were provided.

**Solution**: Either require at least one property, or allow empty objects:

```yaml
# Option 1: Require properties
properties:
  contact_info:
    type: object
    properties:
      email: {type: string}
      phone: {type: string}
    required: [email]  # At least email must be present
    minProperties: 1   # At least one property required

# Option 2: Allow empty, but mark the whole object as optional
# (Don't include contact_info in the parent's required array)
```

## Next Steps

You've mastered nested resources. Now explore:

- **[Schema Composition](./schema-composition/)** - Combine schemas with allOf, anyOf, oneOf
- **[Schema References](../../advanced-topics/schema-references-and-reuse.md)** - Reuse schemas with $ref
- **[Validation Best Practices](../../advanced-topics/json-schema-validation.md)** - Write robust validation rules

---

**Remember**: Nesting is powerful, but don't overdo it. Three levels deep is usually the sweet spot. Beyond that, consider breaking out into separate resources with ID references.
