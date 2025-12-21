+++
title = "Introduction"
weight = 10
description = "Discover firestone's resource-first approach and how it turns one definition into complete APIs, CLIs, and UIs."
+++

# Introduction

## Welcome to Firestone!

**Stop maintaining four versions of the same thing.**

Right now, you're probably defining your data model in multiple places:
- OpenAPI spec (for REST APIs)
- AsyncAPI spec (for WebSockets)
- CLI argument parsers
- UI form validation

When you add a field, you update all four. Miss one? Things break. Add validation? Four places to update. It's tedious, error-prone, and frustrating.

**Firestone fixes this.**

Define your resource once - as a simple JSON Schema. Firestone automatically generates:
- ✨ **OpenAPI 3.x specs** - Complete REST API documentation
- 🔄 **AsyncAPI specs** - WebSocket and event-driven APIs
- 🖥️ **Python CLIs** - Full CRUD command-line tools
- 📊 **Streamlit UIs** - Interactive web dashboards

One definition. Four outputs. Always in sync.

## Why You'll Love This

**Speed**
Generate a complete API ecosystem in minutes, not weeks. Define your resource, run `firestone generate`, done.

**Consistency**
Add a field in one place, it appears everywhere. Add validation once, it enforces everywhere. No more hunting for that one place you forgot to update.

**Focus on What Matters**
Think about your data model - what is a Book? What are its properties? Let firestone handle the boring parts: paths, parameters, argument parsing, form generation.

## What You'll Learn Here

This section explains firestone's philosophy and how it fits into your development workflow.

### 1. [What is Firestone?](../getting-started/what-is-firestone.md)
The problem firestone solves and its core value proposition.

### 2. [Architecture Overview](../getting-started/architecture.md)
How resource definitions flow through firestone to become multiple outputs.

### 3. [Why Resource-First Design?](../getting-started/why-resource-first.md)
The philosophy behind starting with data models instead of API paths.

## Next Steps

Ready to see what firestone can do?
- **Next:** Discover **[What is Firestone?](../getting-started/what-is-firestone.md)** and see real examples.
