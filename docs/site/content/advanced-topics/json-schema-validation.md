+++
title = "JSON Schema Validation"
weight = 3
description = "How validation in your resource definition automatically enforces data integrity everywhere."
+++

## Add Validation Once, Enforce it Everywhere

Here's the beautiful part about firestone's validation: **you write it once, in your resource schema, and it works across all four outputs**.

No duplicate validation logic. No keeping multiple validation rules in sync. Just JSON Schema validation keywords ([reference](https://json-schema.org/understanding-json-schema/reference/)), and firestone handles the rest.

## How It Works

Add validation to your resource:

```yaml
properties:
  username:
    type: string
    minLength: 3
    maxLength: 20
    pattern: "^[a-z0-9_]+$"
    description: "Lowercase letters, numbers, and underscores only"
  email:
    type: string
    format: email
  age:
    type: integer
    minimum: 18
    maximum: 120
  role:
    type: string
    enum: [user, admin, moderator]
required: [username, email]
```

Now that validation automatically works in:

**1. OpenAPI Spec**
The generated spec includes all validation rules. API gateways and server frameworks use these to reject invalid requests:
```yaml
# In generated OpenAPI spec
username:
  type: string
  minLength: 3
  maxLength: 20
  pattern: "^[a-z0-9_]+$"
```

**2. CLI**
Generated Click commands validate before sending requests:
```bash
$ python cli.py users create --username "AB" --email "invalid" --age 15

Error: username must be at least 3 characters
Error: email is not a valid email address
Error: age must be at least 18
```

**3. Streamlit UI**
Form inputs enforce validation rules automatically:
- Text inputs show min/max length
- Number inputs enforce min/max values
- Dropdowns are populated from enums
- Forms won't submit with invalid data

**4. Generated Client SDKs**
When you generate client libraries from the OpenAPI spec, they include validation, catching errors before making network requests.

## Common Validation Keywords

**Strings**
```yaml
type: string
minLength: 3          # Minimum characters
maxLength: 100        # Maximum characters
pattern: "^[A-Z]"     # Regex match
format: email         # Built-in formats: email, uri, date, time, etc.
```

**Numbers**
```yaml
type: integer         # or "number" for floats
minimum: 0            # >= 0
maximum: 100          # <= 100
multipleOf: 5         # Must be multiple of 5
```

**Enums (Choices)**
```yaml
type: string
enum: [pending, approved, rejected]
```

**Arrays**
```yaml
type: array
minItems: 1          # At least one item
maxItems: 10         # At most 10 items
uniqueItems: true    # No duplicates
```

**Objects**
```yaml
type: object
required: [name, email]    # These fields are mandatory
additionalProperties: false # Only allow defined properties
```

## Real-World Example

Let's create a user resource with comprehensive validation:

```yaml
kind: user
schema:
  type: array
  key:
    name: user_id
  items:
    type: object
    properties:
      username:
        type: string
        minLength: 3
        maxLength: 20
        pattern: "^[a-z0-9_]+$"
        description: "Alphanumeric and underscore, lowercase only"
      email:
        type: string
        format: email
        description: "Valid email address required"
      age:
        type: integer
        minimum: 18
        maximum: 120
        description: "Must be 18 or older"
      bio:
        type: string
        maxLength: 500
        description: "Short biography, max 500 characters"
      role:
        type: string
        enum: [user, moderator, admin]
        default: user
        description: "User permission level"
      tags:
        type: array
        items:
          type: string
        maxItems: 10
        uniqueItems: true
        description: "Up to 10 unique tags"
    required: [username, email, age]
```

Generate everything:
```bash
# OpenAPI spec with all validation
firestone generate --resources user.yaml openapi > openapi.yaml

# CLI that validates inputs
firestone generate --resources user.yaml cli > cli.py

# Streamlit UI with validated forms
firestone generate --resources user.yaml streamlit > app.py
```

Now try to create an invalid user:
- **Via CLI**: Validation fails before request is sent
- **Via Streamlit**: Form shows errors, won't submit
- **Via API**: Server returns 400/422 with detailed error messages
- **Via Generated Client**: Client-side validation catches errors

**All from the same validation rules in your resource schema.**

## The Single Source of Truth

Need to change a validation rule? Update it once in your resource:

```yaml
# Change minimum age from 18 to 21
age:
  type: integer
  minimum: 21  # Changed from 18
  maximum: 120
```

Regenerate all four outputs:
```bash
firestone generate --resources user.yaml openapi > openapi.yaml
firestone generate --resources user.yaml cli > cli.py
firestone generate --resources user.yaml streamlit > app.py
# (and AsyncAPI if you use it)
```

Now the new minimum age of 21 is enforced in:
- OpenAPI spec (API validation)
- CLI (command validation)
- Streamlit (form validation)
- AsyncAPI (message validation)

**One change, four updates, zero inconsistencies.**

## Best Practices

**1. Validate at the Source**
Put validation in your resource schema, not scattered across application code.

**2. Use Descriptive Messages**
The `description` field helps users understand what's expected:
```yaml
username:
  type: string
  pattern: "^[a-z0-9_]+$"
  description: "Letters, numbers, and underscores only"
```

**3. Fail Fast**
Let firestone's validation catch errors early - before they reach your database or business logic.

**4. Test Your Validation**
Use the generated CLI to quickly test validation rules:
```bash
# Should fail
python cli.py users create --username "UPPERCASE" --email "bad" --age 10

# Should succeed
python cli.py users create --username "valid_user" --email "user@example.com" --age 25
```

## Next Steps

Want to learn more about JSON Schema validation?
- [JSON Schema Validation Reference](https://json-schema.org/understanding-json-schema/reference/) - Complete validation keyword reference

Ready to see validation in action?
- **Try it:** [Quickstart Tutorial](../../getting-started/quickstart/) - Build a resource with validation
- **Go deeper:** [Schema Design](./schema-design/) - Best practices for designing schemas
