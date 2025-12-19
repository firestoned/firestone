+++
title = "firestone"
weight = 10
description = "Resource-based API specification generator: Define your data once, generate OpenAPI, AsyncAPI, CLIs, and UIs automatically"
+++

# firestone: A Resource-First Approach to Building APIs

**Stop writing API boilerplate. Start defining resources.**

`firestone` lets you build OpenAPI, AsyncAPI, and CLI specifications from JSON Schema resource definitions. Focus on what matters—your data model—and let firestone handle the rest.

[Project Repository](https://github.com/firestoned/firestone)

## The Problem

Building modern APIs means writing the same things over and over:
- OpenAPI paths for each endpoint
- Request/response schemas for every operation
- Validation logic scattered everywhere
- CLI tools for testing
- Documentation that's out of sync with code

**What if you could define your resource once and generate everything automatically?**

## The Solution: Resource-First Design

firestone uses JSON Schema as a DSL to define resources. From one resource definition, it generates:

- ✨ **OpenAPI 3.x specifications** - Complete REST API definitions
- 🔄 **AsyncAPI specifications** - WebSocket and event-driven APIs
- 🖥️ **Python Click CLIs** - Full CRUD command-line tools
- 📊 **Streamlit UIs** - Data management dashboards

## Why This Approach Works

**Resources are your single source of truth.** Everything else is generated from them.

```yaml
# Define your resource once
kind: book
schema:
  type: array
  key:
    name: book_id
    schema:
      type: string
  items:
    type: object
    properties:
      title:
        type: string
      author:
        type: string
      isbn:
        type: string
```

From this single definition, you get:
- REST API endpoints (`GET /books`, `POST /books`, `GET /books/{id}`, etc.)
- Request/response validation
- OpenAPI documentation with Swagger UI
- Python client SDK (via openapi-generator)
- Click-based CLI tool
- Streamlit data UI

## Key Features

- 🎯 **Resource-Based Design** - Define data models, not API endpoints
- 📐 **JSON Schema Native** - No new languages to learn
- 🔧 **Code Generation Ready** - Integrates with openapi-generator for multi-language clients
- 🚀 **Four Output Types** - OpenAPI, AsyncAPI, CLI, Streamlit from one input
- 🔌 **Ecosystem Integration** - Works with FastAPI, Rust clients, TypeScript SDKs
- 📝 **Self-Documenting** - Swagger UI built-in
- 🎨 **Template Customization** - Jinja2 templates for full control
- 🔒 **Security Built-In** - OAuth2, JWT, API keys supported

## Quick Example

**1. Define a resource**

```yaml
kind: addressbook
methods:
  resource: [get, post]
  instance: [get, put, delete]
schema:
  type: array
  key:
    name: address_key
    schema:
      type: string
  items:
    type: object
    properties:
      street: {type: string}
      city: {type: string}
      state: {type: string}
    required: [street, city, state]
```

**2. Generate OpenAPI**

```bash
firestone generate \
  --title 'Addressbook API' \
  --resources addressbook.yaml \
  openapi > openapi.yaml
```

**3. View in Swagger UI**

```bash
firestone generate \
  --title 'Addressbook API' \
  --resources addressbook.yaml \
  openapi --ui-server
```

Navigate to `http://127.0.0.1:5000/apidocs` to interact with your API.

**4. Generate client code**

```bash
# Python client
openapi-generator generate \
  -i openapi.yaml \
  -g python \
  -o client/

# Rust client
openapi-generator generate \
  -i openapi.yaml \
  -g rust \
  -o rust-client/
```

**5. Generate CLI tool**

```bash
firestone generate \
  --resources addressbook.yaml \
  cli \
  --pkg addressbook \
  --client-pkg addressbook.client > cli.py
```

## Who Should Use firestone?

- 👨‍💻 **API Developers** - Skip the OpenAPI boilerplate, focus on data models
- 🏗️ **Platform Engineers** - Generate consistent APIs across services
- 📱 **Full-Stack Developers** - Get client SDKs and CLIs automatically
- 🧪 **QA Engineers** - CLI tools for testing without writing code
- 📚 **Tech Writers** - Auto-generated Swagger documentation

## The Bigger Picture

firestone is part of the [firestoned ecosystem](https://github.com/firestoned):

- **firestone** - API specification generation (you are here)
- **firestone-lib** - Shared library for resource handling
- **forevd** - Authentication proxy (mTLS, OIDC, LDAP)
- **bindy** - Kubernetes DNS controller
- **bindcar** - BIND9 REST API sidecar

Together, they provide API-driven infrastructure management.

## Installation Note

> **Important:** The package name is `firestoned` (with a 'd'), not `firestone`.
> This is because `firestone` was already taken on PyPI.

```bash
# Install with pip
pip install firestoned

# Or with Poetry (recommended)
poetry add firestoned
```

## Next Steps

**New to firestone?** Start here:
- [Installation Guide](getting-started/installation/) - Get firestone running
- [Quick Start Tutorial](getting-started/quickstart/) - 5-minute walkthrough
- [Core Concepts](core-concepts) - Understand resource-first design

**Ready to build?**
- [Resource Schema Reference](core-concepts/resource-schema) - Complete schema documentation
- [OpenAPI Generation](generation-guides/openapi) - Generate REST APIs
- [CLI Generation](generation-guides/cli) - Build command-line tools
- **[Python API Reference](api-reference)** - Complete Python API documentation for the `firestone` package

**Looking for examples?**
- [Addressbook Tutorial](examples/addressbook/) - Complete working example
- [Blog API Example](examples/blog-api/) - Multi-resource relationships
- [Simple CRUD Example](examples/simple-crud/) - Contact management with full CRUD operations