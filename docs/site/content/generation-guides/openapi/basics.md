+++
title = "OpenAPI Basics"
linkTitle = "OpenAPI Basics"
weight = 1
description = "How firestone generates complete OpenAPI 3.x specs from your resource definitions."
+++

## From Resource to REST API Spec - Automatically

OpenAPI 3.x is the industry standard for describing REST APIs ([learn more](https://swagger.io/specification/)). Here's what makes firestone's approach special: **you never write OpenAPI YAML directly**.

Instead, you define your resource once, and firestone generates a complete, valid OpenAPI spec automatically. Let's see what firestone handles for you:

**Automatic Path Generation**
Your `methods` configuration becomes REST endpoints:
- `methods.resource: [get, post]` → `GET /books` and `POST /books`
- `methods.instance: [get, put, delete]` → `GET /books/{id}`, `PUT /books/{id}`, `DELETE /books/{id}`

**Smart Schema Translation**
Your JSON Schema becomes reusable OpenAPI components:
- Nested objects become `$ref` references
- Arrays get proper item definitions
- Validation rules (min, max, pattern) transfer directly

**Response Structures**
Firestone generates proper response schemas:
- Collection endpoints return arrays
- Instance endpoints return single objects
- Error responses follow OpenAPI conventions

**Security Definitions**
Add security to your resource, get it in OpenAPI:
```yaml
security:
  - type: bearer
```
Becomes a complete security scheme definition.

> 💡 **One Definition, Four Outputs**
> This same resource definition also generates [AsyncAPI](../asyncapi/) (WebSocket specs), [CLI](../cli/) (command-line tools), and [Streamlit UI](../streamlit/) (web dashboards).

**What You Can Do With the Generated OpenAPI Spec**

Once firestone generates your spec, you can:
- **View it in Swagger UI** - interactive documentation that updates as your resource evolves
- **Generate client SDKs** - Python, TypeScript, Java, Go, and 50+ languages via [OpenAPI Generator](https://openapi-generator.tech/)
- **Generate server stubs** - FastAPI, Spring Boot, Express.js starting points
- **Import into Postman** - instant test collections
- **Validate requests** - ensure API compliance in tests

The best part? Change your resource definition, regenerate, and all of these stay in sync. No manually updating OpenAPI paths when you add a field.

---
## Next Steps

You've learned how firestone generates OpenAPI specs. Now let's actually create one!
- **Next:** Learn the commands to produce a valid OpenAPI specification in **[Generating OpenAPI Specs](./generating)**.
