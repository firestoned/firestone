---
title: "Error Messages Guide"
linkTitle: "Error Messages"
weight: 5
description: >
  Common firestone error messages and how to fix them.
---

## Overview

This guide explains common error messages you'll encounter when using firestone and how to resolve them.

**How to use:**
1. Find your error message (search with Ctrl+F)
2. Read the explanation
3. Apply the suggested fix
4. Re-run your command

---

## Resource File Errors

### Error: Resource file not found

```
Error: Resource file not found: resources/user.yaml
```

**Cause:** The file path doesn't exist or is incorrect.

**Fix:**
```bash
# Check file exists
ls resources/user.yaml

# Use correct path
firestone generate --resources resources/user.yaml openapi

# Or use current directory
firestone generate --resources ./user.yaml openapi
```

---

### Error: Invalid YAML syntax

```
Error: Invalid YAML syntax in user.yaml:
  line 12: mapping values are not allowed here
```

**Cause:** YAML formatting error (indentation, colons, etc.)

**Common mistakes:**
```yaml
# ❌ BAD - Missing colon
properties
  name:
    type: string

# ✅ GOOD
properties:
  name:
    type: string
```

```yaml
# ❌ BAD - Inconsistent indentation
properties:
  name:
    type: string
   email:  # Wrong indentation
    type: string

# ✅ GOOD
properties:
  name:
    type: string
  email:
    type: string
```

**Fix:**
- Use a YAML validator: https://www.yamllint.com/
- Use consistent 2-space indentation
- Ensure colons have space after them: `key: value` not `key:value`

---

### Error: Missing required field

```
Error: Missing required field: 'kind'
```

**Cause:** Resource YAML is missing a required top-level field.

**Required fields:**
- `kind`
- `apiVersion`
- `methods`
- `schema`

**Fix:**
```yaml
kind: users           # ✅ Required
apiVersion: v1        # ✅ Required
methods:              # ✅ Required
  resource: [get]
  instance: [get]
schema:               # ✅ Required
  type: array
  items:
    type: object
```

---

## Schema Validation Errors

### Error: Invalid schema type

```
Error: Invalid schema type: 'object'
  schema.type must be 'array'
```

**Cause:** Top-level `schema.type` must be `array`, not `object`.

**Fix:**
```yaml
# ❌ BAD
schema:
  type: object  # Wrong!

# ✅ GOOD
schema:
  type: array
  items:
    type: object  # Object goes in items
```

---

### Error: Missing required schema field

```
Error: schema.items is required when schema.type is 'array'
```

**Cause:** Array schema must have `items` field.

**Fix:**
```yaml
schema:
  type: array
  items:        # ✅ Required for arrays
    type: object
    properties:
      name: {type: string}
```

---

### Error: Invalid JSON Schema

```
Error: Invalid JSON Schema in schema.items
  'invalid_type' is not a valid type
```

**Cause:** Using an invalid JSON Schema type.

**Valid types:**
- `string`
- `number`
- `integer`
- `boolean`
- `array`
- `object`
- `null`

**Fix:**
```yaml
# ❌ BAD
properties:
  age:
    type: int  # Should be "integer"

# ✅ GOOD
properties:
  age:
    type: integer
```

---

### Error: Key is required for instance methods

```
Error: schema.key is required when instance methods are defined
```

**Cause:** If you have instance methods (`get`, `put`, `delete`), you need a key.

**Fix:**
```yaml
methods:
  instance: [get, put, delete]

schema:
  type: array
  key:  # ✅ Required for instance methods
    name: user_id
    schema:
      type: string
      format: uuid
```

---

## Method Errors

### Error: Invalid HTTP method

```
Error: Invalid HTTP method: 'update'
  Valid methods: get, post, put, patch, delete
```

**Cause:** Using an invalid HTTP method name.

**Valid methods:**
- `get`
- `post`
- `put`
- `patch`
- `delete`

**Fix:**
```yaml
# ❌ BAD
methods:
  resource: [list, create]  # Invalid

# ✅ GOOD
methods:
  resource: [get, post]
```

---

### Error: Instance method without key

```
Error: Instance methods require a key definition
  Found instance methods: [get, put, delete]
  But schema.key is not defined
```

**Cause:** Instance methods need a key to identify resources.

**Fix:**
```yaml
methods:
  resource: [get, post]
  instance: [get, put, delete]

schema:
  key:  # ✅ Add key definition
    name: id
    schema:
      type: string
```

---

## Query Parameter Errors

### Error: Invalid query parameter structure

```
Error: query_params must be an array of objects
```

**Cause:** Incorrect structure for query parameters.

**Fix:**
```yaml
# ❌ BAD
query_params:
  status:
    type: string

# ✅ GOOD
query_params:
  - name: status
    schema:
      type: string
```

---

### Error: Query parameter missing required field

```
Error: query_param is missing required field 'name'
```

**Cause:** Each query parameter must have `name` and `schema`.

**Fix:**
```yaml
query_params:
  - name: status      # ✅ Required
    schema:           # ✅ Required
      type: string
    methods: [get]    # ❌ Optional
```

---

## Security Errors

### Error: Invalid security scheme type

```
Error: Invalid security scheme type: 'jwt'
  Valid types: http, apiKey, oauth2, openIdConnect
```

**Cause:** Using an invalid security scheme type.

**Valid types:**
- `http` (for bearer, basic auth)
- `apiKey`
- `oauth2`
- `openIdConnect`

**Fix:**
```yaml
# ❌ BAD
security:
  scheme:
    jwt_auth:
      type: jwt  # Invalid type

# ✅ GOOD
security:
  scheme:
    bearer_auth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

---

### Error: Security scheme requires 'scheme' field

```
Error: HTTP security type requires 'scheme' field
  Valid schemes: basic, bearer
```

**Cause:** HTTP security type needs `scheme` field.

**Fix:**
```yaml
# ❌ BAD
security:
  scheme:
    auth:
      type: http  # Missing 'scheme'

# ✅ GOOD
security:
  scheme:
    bearer_auth:
      type: http
      scheme: bearer  # ✅ Required for http type
```

---

## Generation Errors

### Error: No resources provided

```
Error: No resources provided
  Use --resources <path> to specify resource files
```

**Cause:** Forgot `--resources` flag.

**Fix:**
```bash
# ❌ BAD
firestone generate openapi

# ✅ GOOD
firestone generate --resources user.yaml openapi
```

---

### Error: Title is required for OpenAPI generation

```
Error: --title is required for openapi generator
```

**Cause:** OpenAPI generation requires `--title` flag.

**Fix:**
```bash
# ❌ BAD
firestone generate --resources user.yaml openapi

# ✅ GOOD
firestone generate --resources user.yaml --title "User API" openapi
```

---

### Error: Missing required CLI options

```
Error: CLI generator requires --pkg and --client-pkg options
```

**Cause:** CLI generation requires package names.

**Fix:**
```bash
# ❌ BAD
firestone generate --resources user.yaml --title "CLI" cli

# ✅ GOOD
firestone generate \
  --resources user.yaml \
  --title "User CLI" \
  cli \
  --pkg user_cli \
  --client-pkg user_client
```

---

### Error: Streamlit requires backend URL

```
Error: Streamlit generator requires --backend-url option
```

**Cause:** Streamlit generation needs API backend URL.

**Fix:**
```bash
# ❌ BAD
firestone generate --resources user.yaml --title "UI" streamlit

# ✅ GOOD
firestone generate \
  --resources user.yaml \
  --title "User UI" \
  streamlit \
  --backend-url http://localhost:8000
```

---

## Validation Errors

### Error: Pattern validation failed

```
Error: Field 'username' failed pattern validation
  Value: 'Invalid User!'
  Pattern: ^[a-z0-9_]+$
```

**Cause:** Value doesn't match the regex pattern.

**Fix:**
```yaml
# Pattern only allows lowercase, digits, underscores
username:
  type: string
  pattern: '^[a-z0-9_]+$'

# ✅ Valid values: "john_doe", "user123"
# ❌ Invalid: "Invalid User!", "UPPERCASE"
```

---

### Error: Length validation failed

```
Error: Field 'name' failed length validation
  Value length: 0
  minLength: 1
```

**Cause:** String is shorter than `minLength`.

**Fix:**
```yaml
name:
  type: string
  minLength: 1  # Empty strings not allowed
  maxLength: 100
```

---

### Error: Enum validation failed

```
Error: Field 'status' value not in enum
  Value: 'unknown'
  Allowed: [active, inactive, pending]
```

**Cause:** Value not in the enum list.

**Fix:**
```yaml
status:
  type: string
  enum: [active, inactive, pending]

# ✅ Valid: "active", "inactive", "pending"
# ❌ Invalid: "unknown", "deleted", anything else
```

---

### Error: Required field missing

```
Error: Required field 'email' is missing
```

**Cause:** Required field not provided.

**Fix:**
```yaml
properties:
  name: {type: string}
  email: {type: string}
required: [name, email]  # Both must be present
```

---

## Type Errors

### Error: Type mismatch

```
Error: Field 'age' type mismatch
  Expected: integer
  Got: string
```

**Cause:** Provided value doesn't match schema type.

**Fix:**
```yaml
age:
  type: integer  # Expects numbers like 25, not "25"
```

**Correct values:**
```json
{"age": 25}      // ✅ Integer
{"age": "25"}    // ❌ String
{"age": 25.5}    // ❌ Number (not integer)
```

---

### Error: Format validation failed

```
Error: Field 'email' failed format validation
  Value: 'invalid-email'
  Format: email
```

**Cause:** Value doesn't match the specified format.

**Common formats:**
- `email` - Must be valid email
- `uri` - Must be valid URI
- `uuid` - Must be valid UUID
- `date` - Must be YYYY-MM-DD
- `date-time` - Must be ISO 8601 datetime

**Fix:**
```yaml
email:
  type: string
  format: email

# ✅ Valid: "user@example.com"
# ❌ Invalid: "invalid-email", "user@", "@example.com"
```

---

## File Output Errors

### Error: Permission denied writing output

```
Error: Permission denied: /etc/openapi.yaml
```

**Cause:** No write permission to output location.

**Fix:**
```bash
# Write to writable location
firestone generate --resources user.yaml openapi > ./openapi.yaml

# Or use sudo (not recommended)
sudo firestone generate --resources user.yaml openapi > /etc/openapi.yaml
```

---

### Error: Output directory does not exist

```
Error: No such file or directory: output/openapi.yaml
```

**Cause:** Parent directory doesn't exist.

**Fix:**
```bash
# Create directory first
mkdir -p output
firestone generate --resources user.yaml openapi > output/openapi.yaml
```

---

## Debug Mode

Enable debug output to see more details:

```bash
firestone --debug generate --resources user.yaml openapi
```

This shows:
- Resource parsing steps
- Validation checks
- Template rendering
- Full error stack traces

---

## Common Troubleshooting Steps

### Step 1: Validate YAML Syntax

```bash
# Use yamllint
yamllint user.yaml

# Or Python
python -c "import yaml; yaml.safe_load(open('user.yaml'))"
```

### Step 2: Validate JSON Schema

```bash
# Use check-jsonschema
pip install check-jsonschema
check-jsonschema --schemafile schema.json user.yaml
```

### Step 3: Test with Minimal Resource

```bash
# Create minimal test resource
cat > test.yaml <<EOF
kind: test
apiVersion: v1
methods:
  resource: [get]
  instance: []
schema:
  type: array
  items:
    type: object
    properties:
      name: {type: string}
EOF

# Test generation
firestone generate --resources test.yaml --title "Test" openapi
```

### Step 4: Enable Debug Mode

```bash
firestone --debug generate --resources user.yaml openapi
```

### Step 5: Check Firestone Version

```bash
firestone --version

# Update if old
pip install --upgrade firestoned
```

---

## Error Patterns

### Pattern: "Cannot read property X of undefined"

**Usually means:** Missing required nested field

**Fix:** Check for missing required sub-fields in objects

---

### Pattern: "Expected X but got Y"

**Usually means:** Type mismatch in schema

**Fix:** Ensure values match schema types (string, integer, etc.)

---

### Pattern: "Path /X already exists"

**Usually means:** Duplicate resource kind or overlapping paths

**Fix:** Ensure each resource has unique `kind` value

---

## Getting Help

If you can't resolve an error:

1. **Search documentation** - Use site search
2. **Check examples** - Compare to working examples
3. **Enable debug mode** - Get detailed error info
4. **Simplify** - Create minimal failing example
5. **Report issue** - GitHub issues with:
   - Error message
   - Resource YAML (redacted if needed)
   - Firestone version
   - Command used

---

## See Also

- **[Resource Schema Reference](./resource-schema-quick-reference)** - Schema field reference
- **[CLI Command Reference](./cli-command-reference)** - Command syntax
- **[Operations Guide](error-messages-guide.md)** - Troubleshooting workflows
- **[Examples](../examples/)** - Working examples to compare against
