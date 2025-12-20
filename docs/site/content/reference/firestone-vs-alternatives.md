---
title: "Firestone vs Alternatives"
linkTitle: "Firestone vs Alternatives"
weight: 3
description: >
  When to use firestone vs code-first, OpenAPI-first, or other approaches to API development.
---

## Overview

API development has many approaches. This guide helps you choose the right tool for your situation by comparing firestone's resource-first approach to alternatives.

**TL;DR:**
- **Use firestone** when: You want to define data models once and generate multiple outputs (specs, CLIs, UIs)
- **Use code-first** when: You have existing code and want to document it
- **Use OpenAPI-first** when: You need maximum control over every API detail
- **Use GraphQL** when: Clients need flexible querying of complex data graphs

---

## The Three Approaches

### 1. Resource-First (Firestone)

**Philosophy:** Define your data model with JSON Schema. Generate everything else from it.

**Workflow:**
```
Resource YAML → OpenAPI + AsyncAPI + CLI + Streamlit
```

**Advantages:**
- ✅ **Single source of truth** - Data model drives everything
- ✅ **Multiple outputs** - One definition → many artifacts
- ✅ **JSON Schema validation** - Industry-standard validation
- ✅ **Less code to maintain** - Automate boilerplate
- ✅ **Consistency guaranteed** - All outputs match the schema

**Disadvantages:**
- ❌ **Opinionated structure** - REST conventions enforced
- ❌ **Less control** - Can't customize every OpenAPI detail
- ❌ **Learning curve** - Need to learn resource schema format

**When to use:**
- Building new APIs from scratch
- Data-centric applications
- CRUD-heavy applications
- Microservices with standard patterns
- Generating multiple outputs (spec + CLI + docs)

---

### 2. Code-First

**Philosophy:** Write code first. Generate API documentation from code.

**Examples:**
- FastAPI (Python)
- Axum with utoipa (Rust)
- Spring Boot (Java)
- NestJS (TypeScript)

**Workflow:**
```
Python/Rust/Java code → OpenAPI spec → Client SDKs
```

**Advantages:**
- ✅ **Code is truth** - Implementation and docs can't diverge
- ✅ **Type safety** - Compiler enforces correctness
- ✅ **Incremental adoption** - Add docs to existing code
- ✅ **IDE support** - Autocomplete, refactoring work
- ✅ **Framework features** - Dependency injection, middleware, etc.

**Disadvantages:**
- ❌ **More boilerplate** - Write routes, handlers, validation
- ❌ **Single output** - Just OpenAPI spec
- ❌ **Tied to language** - Can't switch easily
- ❌ **Implementation details leak** - Code structure affects API

**When to use:**
- Existing codebase you want to document
- Complex business logic in handlers
- Team already familiar with a web framework
- Need framework-specific features (auth, middleware, etc.)

---

### 3. OpenAPI-First

**Philosophy:** Write OpenAPI spec by hand. Generate code from it.

**Tools:**
- Swagger Editor
- Stoplight Studio
- OpenAPI Generator
- Redocly

**Workflow:**
```
Hand-written OpenAPI YAML → Server stubs + Client SDKs
```

**Advantages:**
- ✅ **Maximum control** - Every detail of the spec
- ✅ **Language agnostic** - Generate any language from spec
- ✅ **API design focus** - Think about API before implementation
- ✅ **Tooling ecosystem** - Mature OpenAPI tools
- ✅ **Contract-first** - Spec is the contract

**Disadvantages:**
- ❌ **Verbose** - OpenAPI specs are large and repetitive
- ❌ **Hard to maintain** - Manual changes to large YAML files
- ❌ **No abstraction** - Repeat yourself for similar endpoints
- ❌ **Validation gaps** - Easy to make spec mistakes
- ❌ **Schema drift** - Implementation can diverge from spec

**When to use:**
- APIs with unusual patterns OpenAPI handles well
- Need extreme control over API design
- Strong API governance requirements
- Team has OpenAPI expertise
- Generating clients in many languages

---

## Detailed Comparison

### Firestone vs FastAPI (Code-First)

#### FastAPI Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI(title="User API")

class User(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

users_db = {}

@app.get("/users")
def list_users():
    return list(users_db.values())

@app.post("/users", status_code=201)
def create_user(user: User):
    user_id = str(len(users_db) + 1)
    users_db[user_id] = user
    return {"id": user_id, **user.dict()}

@app.get("/users/{user_id}")
def get_user(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]
```

#### Firestone Equivalent

```yaml
kind: users
apiVersion: v1
metadata:
  description: User management API

methods:
  resource: [get, post]
  instance: [get]

schema:
  type: array
  key:
    name: user_id
    schema: {type: string}
  items:
    type: object
    properties:
      name: {type: string, minLength: 1}
      email: {type: string, format: email}
      age: {type: integer, minimum: 0}
    required: [name, email]
```

Then generate:
```bash
# OpenAPI spec
firestone generate -r user.yaml -t "User API" openapi > spec.yaml

# CLI
firestone generate -r user.yaml -t "User API" cli --pkg user_cli --client-pkg user_client > cli.py

# Streamlit UI
firestone generate -r user.yaml -t "User API" streamlit --backend-url http://localhost:8000 > ui.py
```

**Comparison:**

| Aspect | FastAPI | Firestone |
|--------|---------|-----------|
| Lines of code | ~30 | ~15 YAML |
| Outputs | OpenAPI spec | OpenAPI + CLI + UI |
| Type safety | Python types | JSON Schema |
| Learning curve | Medium (FastAPI + Pydantic) | Medium (YAML + JSON Schema) |
| Flexibility | High (write any Python code) | Medium (REST conventions) |
| Boilerplate | More (routes + handlers) | Less (generated) |

**Choose FastAPI if:**
- You need custom business logic in handlers
- You want to use Python's type system
- You have an existing Python codebase
- You need FastAPI-specific features (dependency injection, background tasks)

**Choose Firestone if:**
- You want to generate multiple outputs (spec + CLI + UI)
- Your API follows standard CRUD patterns
- You want less boilerplate
- You prefer data-model-driven development

---

### Firestone vs OpenAPI-First

#### OpenAPI-First Example

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
  /users/{user_id}:
    get:
      summary: Get user
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: Not found
components:
  schemas:
    User:
      type: object
      properties:
        user_id: {type: string}
        name: {type: string}
        email: {type: string, format: email}
        age: {type: integer}
      required: [user_id, name, email]
    UserCreate:
      type: object
      properties:
        name: {type: string}
        email: {type: string, format: email}
        age: {type: integer}
      required: [name, email]
```

**Comparison:**

| Aspect | OpenAPI-First | Firestone |
|--------|---------------|-----------|
| Lines of YAML | ~60 | ~15 |
| Control over spec | Maximum | Medium |
| Repetition | High (DRY violations) | Low (abstracted) |
| Custom responses | Easy | Limited |
| Schema reuse | Manual $ref | Automatic |
| Maintainability | Hard (large files) | Easy (small files) |

**Choose OpenAPI-First if:**
- You need custom response codes (e.g., 202 Accepted, 409 Conflict)
- You want to define non-CRUD operations
- You need specific OpenAPI extensions
- You're documenting a legacy API with unusual patterns

**Choose Firestone if:**
- Your API follows standard CRUD patterns
- You want to avoid repetitive YAML
- You want automated schema reuse
- You prefer a higher-level abstraction

---

### Firestone vs GraphQL

#### GraphQL Example

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  age: Int
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}

type Query {
  user(id: ID!): User
  users: [User!]!
  post(id: ID!): Post
}

type Mutation {
  createUser(name: String!, email: String!, age: Int): User!
  createPost(title: String!, content: String!, authorId: ID!): Post!
}
```

**Comparison:**

| Aspect | GraphQL | Firestone (REST) |
|--------|---------|------------------|
| Query flexibility | High (client chooses fields) | Low (fixed endpoints) |
| Over/under-fetching | Eliminated | Common |
| Caching | Complex (needs Apollo) | Simple (HTTP caching) |
| Learning curve | Steep | Gentle |
| Tooling | Specialized | Standard HTTP |
| Type system | GraphQL types | JSON Schema |

**Choose GraphQL if:**
- Clients need to query complex, nested data
- You want to avoid over-fetching
- You have many different client types (web, mobile, etc.)
- Your data model is a graph (with relationships)

**Choose Firestone if:**
- Your API is primarily CRUD operations
- You want simple HTTP semantics
- You need OpenAPI compatibility
- You prefer REST conventions

---

## Decision Matrix

### Choose Firestone When

✅ Building a new API from scratch
✅ API follows CRUD patterns
✅ Need multiple outputs (spec + CLI + UI)
✅ Want to minimize boilerplate
✅ Data model is the core complexity
✅ Team comfortable with YAML and JSON Schema
✅ Want generated, consistent specs
✅ Need AsyncAPI support

### Choose Code-First (FastAPI/Axum) When

✅ Have existing code to document
✅ Complex business logic in handlers
✅ Team is strong in a specific language
✅ Need framework-specific features
✅ Want type-safe compilation
✅ Prefer code over configuration
✅ Need fine-grained control over implementation

### Choose OpenAPI-First When

✅ Need maximum control over API spec
✅ API has unusual patterns
✅ Strong API governance requirements
✅ Generating clients in many languages
✅ Team has OpenAPI expertise
✅ Want spec as the contract
✅ Non-CRUD operations dominate

### Choose GraphQL When

✅ Complex, interconnected data model
✅ Many different client types
✅ Clients need flexible querying
✅ Want to eliminate over/under-fetching
✅ Real-time subscriptions needed
✅ Team has GraphQL expertise

---

## Hybrid Approaches

### Firestone + FastAPI

1. Use firestone to generate OpenAPI spec
2. Generate FastAPI server stub from spec
3. Implement business logic in FastAPI handlers
4. Use generated firestone CLI for testing

**Advantages:**
- Firestone for boilerplate reduction
- FastAPI for custom logic
- Best of both worlds

---

### Firestone + OpenAPI Customization

1. Generate base OpenAPI spec with firestone
2. Post-process with custom scripts to add:
   - Custom response codes
   - OpenAPI extensions
   - Additional operations
3. Validate with Spectral

**Advantages:**
- 80% automation from firestone
- 20% customization for edge cases

---

## Migration Paths

### From Code-First to Firestone

1. Extract resource schemas from existing code
2. Create firestone resource YAML files
3. Generate OpenAPI spec
4. Compare with code-generated spec
5. Gradually replace endpoints

### From OpenAPI-First to Firestone

1. Analyze existing OpenAPI spec
2. Identify CRUD patterns
3. Extract schemas into firestone resources
4. Generate new spec and compare
5. Migrate standard operations first

### From REST to GraphQL

(Firestone doesn't help here - different paradigms)

---

## When NOT to Use Firestone

❌ **Complex, non-CRUD operations** - E.g., `/search`, `/report`, `/export`
❌ **Highly customized responses** - Different schemas per status code
❌ **Legacy API with quirks** - Unusual patterns that don't fit REST
❌ **GraphQL/gRPC APIs** - Firestone generates REST/AsyncAPI only
❌ **Minimal schema complexity** - Overhead not worth it for simple APIs

---

## Complementary Tools

Firestone works well with:

- **openapi-generator** - Generate client SDKs from firestone's OpenAPI output
- **Spectral** - Validate generated OpenAPI specs
- **FastAPI** - Implement server logic based on firestone specs
- **Docker** - Containerize firestone workflows
- **GitHub Actions** - Automate spec generation in CI/CD

---

## Example Scenarios

### Scenario 1: Startup Building MVP

**Situation:** Need to build user management API quickly
**Recommendation:** **Firestone**
**Why:** Minimize boilerplate, generate spec + CLI + UI from one definition

---

### Scenario 2: Enterprise with Existing Java Codebase

**Situation:** Documenting 50 existing REST endpoints
**Recommendation:** **Code-first (Spring Boot + Swagger)**
**Why:** Already have implementation, just need docs

---

### Scenario 3: Complex E-Commerce with Recommendations

**Situation:** Product catalog + recommendations + real-time inventory
**Recommendation:** **Hybrid: Firestone for CRUD + Custom OpenAPI for algorithms**
**Why:** Standard operations (products, orders) fit firestone; custom endpoints handwritten

---

### Scenario 4: Mobile App with Flexible Data Fetching

**Situation:** iOS + Android + Web apps need different data subsets
**Recommendation:** **GraphQL**
**Why:** Clients need query flexibility, avoid over-fetching

---

### Scenario 5: API-as-a-Product

**Situation:** Public API with strict design standards
**Recommendation:** **OpenAPI-first**
**Why:** Need maximum control, API design is critical

---

## Conclusion

**Firestone is best when:**
- You have well-defined data models
- Your API follows REST conventions
- You want to generate multiple outputs
- You prefer declarative configuration over imperative code

**The resource-first philosophy shines when data is the API.** If your API is primarily about CRUD operations on resources, firestone will save you time and ensure consistency across specs, CLIs, and documentation.

For complex business logic, unusual patterns, or existing codebases, code-first or OpenAPI-first approaches may be better fits.

**The right choice depends on your project's unique constraints.** There's no one-size-fits-all answer—but understanding the trade-offs helps you make an informed decision.

---

## See Also

- **[Why Resource-First?](../getting-started/why-resource-first.md)** - Firestone's philosophy
- **[Quickstart Tutorial](../getting-started/quickstart)** - Try firestone
- **[Examples](../examples/)** - See firestone in action
- **[Best Practices](common-patterns-cheat-sheet.md)** - Recommended patterns
