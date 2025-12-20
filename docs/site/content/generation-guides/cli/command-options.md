---
title: "CLI Command Options"
linkTitle: "Command Options"
weight: 3
description: >
  Comprehensive reference for all firestone generate cli command options.
---

## Option Reference

### Common Generate Options

These options are shared across all `firestone generate` subcommands (openapi, asyncapi, cli, streamlit).

#### --title / -t

**Type:** String
**Required:** Yes
**Description:** The title of your API/application

```bash
--title "Task Management API"
```

**Used in:**
- Main CLI help text
- Docstrings and comments
- Log messages

**Example:**
```bash
firestone generate --title "Inventory System" ...
```

---

#### --description / -d

**Type:** String
**Required:** Yes
**Description:** Detailed description of your API/application

```bash
--description "A comprehensive task management system with projects, tags, and collaboration"
```

**Used in:**
- CLI docstring (`"""Description"""`)
- Help pages
- Generated documentation

**Example:**
```bash
firestone generate \
  --description "Manage customer orders, inventory, and shipping" \
  ...
```

---

#### --version / -v

**Type:** String
**Required:** Yes
**Description:** Version number for your API

```bash
--version 1.0
--version 2.3.1
--version 0.1.0-beta
```

**Used in:**
- API versioning
- Package metadata
- Version display in CLI

**Example:**
```bash
firestone generate --version 2.1.0 ...
```

---

#### --summary / -s

**Type:** String
**Required:** No
**Default:** Same as `--description`
**Description:** Short summary (defaults to description if not provided)

```bash
--summary "Task management"
```

**When to use:**
- When description is long and you want a shorter version
- For API docs that need both summary and detailed description

**Example:**
```bash
firestone generate \
  --summary "CRM system" \
  --description "Complete customer relationship management with sales, marketing, and support modules" \
  ...
```

---

#### --resources / -r

**Type:** PathList (comma-separated or multiple flags)
**Required:** Yes
**Description:** One or more resource YAML files

**Single resource:**
```bash
--resources tasks.yaml
```

**Multiple resources (comma-separated):**
```bash
--resources tasks.yaml,projects.yaml,users.yaml
```

**Multiple resources (multiple flags):**
```bash
--resources tasks.yaml \
--resources projects.yaml \
--resources users.yaml
```

**Relative or absolute paths:**
```bash
# Relative
--resources ./schemas/tasks.yaml

# Absolute
--resources /home/user/project/schemas/tasks.yaml
```

**Example:**
```bash
firestone generate \
  --resources \
    resources/users.yaml \
    resources/products.yaml \
    resources/orders.yaml \
  ...
```

---

#### --debug

**Type:** Flag
**Required:** No
**Description:** Enable debug logging

```bash
--debug
```

**What it does:**
- Sets log level to DEBUG
- Shows detailed processing information
- Displays resource validation details
- Shows template rendering debug info

**Example:**
```bash
firestone --debug generate \
  --title "My API" \
  --resources resource.yaml \
  cli ...
```

---

### CLI-Specific Options

These options are specific to the `cli` subcommand.

#### --pkg

**Type:** String
**Required:** Yes
**Description:** The Python package name for your application

```bash
--pkg myapi
```

**Used in imports:**
```python
from myapi import ...
from myapi.resources.logging import ...
```

**Naming conventions:**
- Use lowercase
- Use underscores for multi-word names (`task_api`, not `task-api`)
- Match your package structure

**Example:**
```bash
firestone generate ... cli \
  --pkg ecommerce_api \
  ...
```

---

#### --client-pkg

**Type:** String
**Required:** Yes
**Description:** The package where OpenAPI-generated client code is located

```bash
--client-pkg myapi.client
```

**Used in imports:**
```python
from myapi.client import api_client
from myapi.client import configuration
from myapi.client import exceptions
from myapi.client.api import tasks_api
from myapi.client.models import task
```

**Package structure assumption:**
```
myapi/
└── client/              # --client-pkg myapi.client
    ├── api_client.py
    ├── configuration.py
    ├── exceptions.py
    ├── api/
    │   └── tasks_api.py
    └── models/
        ├── task.py
        ├── create_task.py
        └── update_task.py
```

**Example:**
```bash
firestone generate ... cli \
  --pkg myapp \
  --client-pkg myapp.openapi_client \
  ...
```

---

#### --output / -O

**Type:** File path or `-` for stdout
**Required:** No
**Default:** `-` (stdout)
**Description:** Output file path

**Write to stdout (default):**
```bash
--output -
# or omit entirely
```

**Write to file:**
```bash
--output cli.py
--output myapi/cli/main.py
```

**Redirect stdout to file:**
```bash
firestone generate ... cli > output.py
```

**When to use:**
- **stdout** (`-`): Quick testing, piping to other tools
- **File**: Production code, version control

**Example:**
```bash
# Quick test - view in terminal
firestone generate ... cli --output -

# Save to file
firestone generate ... cli --output production_cli.py

# Advanced: process with another tool
firestone generate ... cli | black - > formatted_cli.py
```

---

#### --output-dir / -o

**Type:** Directory path
**Required:** Only when using `--as-modules`
**Description:** Directory for generated module files

```bash
--output-dir myapi/cli/
```

**Creates:**
```
myapi/cli/
├── tasks.py       # One file per resource
├── projects.py
└── users.py
```

**Directory creation:**
- Firestone creates the directory if it doesn't exist
- Parent directories must exist

**Example:**
```bash
firestone generate ... cli \
  --as-modules \
  --output-dir src/myapi/cli/ \
  ...
```

**Error if not provided with --as-modules:**
```bash
firestone generate ... cli --as-modules
# Error: You must supply an --output-dir when using --as-modules
```

---

#### --as-modules

**Type:** Flag
**Required:** No
**Description:** Generate separate module files instead of one monolithic file

```bash
--as-modules
```

**Without --as-modules (default):**
```python
# Single file: cli.py
@click.group()
def main():
    pass

@main.group()
def tasks():
    pass

@main.group()
def projects():
    pass
```

**With --as-modules:**
```python
# tasks.py
def init():
    @click.group()
    def tasks():
        pass
    return tasks

# projects.py
def init():
    @click.group()
    def projects():
        pass
    return projects
```

**When to use:**
- **Without**: 1-3 resources, simple APIs
- **With**: 4+ resources, better code organization, team development

**Must use with --output-dir:**
```bash
firestone generate ... cli \
  --as-modules \
  --output-dir cli/
```

**Example:**
```bash
# Modular structure for large API
firestone generate \
  --title "Large API" \
  --resources *.yaml \
  cli \
  --pkg largeapi \
  --client-pkg largeapi.client \
  --as-modules \
  --output-dir largeapi/cli/
```

---

#### --template / -T

**Type:** File path
**Required:** No
**Description:** Path to custom Jinja2 template file

```bash
--template templates/custom_cli.jinja2
```

**When to use:**
- Custom CLI structure
- Additional imports or functions
- Modified command names or behavior
- Company-specific formatting

**Template types:**
- **Without --as-modules**: Use `main.py.jinja2` as base
- **With --as-modules**: Use `cli_module.py.jinja2` as base

**Available in template:**
```jinja2
{{ title }}           {# API title #}
{{ description }}     {# API description #}
{{ summary }}         {# API summary #}
{{ version }}         {# API version #}
{{ pkg }}             {# Package name #}
{{ client_pkg }}      {# Client package name #}
{{ rsrcs }}           {# List of resources #}
{{ rsrc }}            {# Current resource (in modules) #}
```

**Example:**
```bash
firestone generate ... cli \
  --template custom_templates/cli.jinja2 \
  --output custom_cli.py
```

**See:** [Customization](./customization) for template details

---

## Option Combinations

### Minimal Command

```bash
firestone generate \
  --title "API" \
  --description "Description" \
  --version 1.0 \
  --resources resource.yaml \
  cli \
  --pkg api \
  --client-pkg api.client
```

Outputs to stdout.

---

### Production Single File

```bash
firestone generate \
  --title "Production API" \
  --description "Production-ready task management" \
  --version 2.0.0 \
  --resources tasks.yaml projects.yaml \
  cli \
  --pkg taskapi \
  --client-pkg taskapi.client \
  --output taskapi/cli.py
```

Creates `taskapi/cli.py` with all resources.

---

### Modular Structure

```bash
firestone generate \
  --title "E-commerce Platform" \
  --summary "E-commerce API" \
  --description "Complete e-commerce with products, orders, payments" \
  --version 3.1.0 \
  --resources \
    schemas/products.yaml \
    schemas/orders.yaml \
    schemas/payments.yaml \
    schemas/customers.yaml \
  cli \
  --pkg ecommerce \
  --client-pkg ecommerce.openapi \
  --as-modules \
  --output-dir ecommerce/cli/
```

Creates:
```
ecommerce/cli/
├── products.py
├── orders.py
├── payments.py
└── customers.py
```

---

### Custom Template

```bash
firestone generate \
  --title "Custom API" \
  --description "API with custom CLI" \
  --version 1.0 \
  --resources resource.yaml \
  cli \
  --pkg myapi \
  --client-pkg myapi.client \
  --template templates/custom.jinja2 \
  --output custom_cli.py
```

Uses custom Jinja2 template for generation.

---

### Debug Mode

```bash
firestone --debug generate \
  --title "Debug API" \
  --description "Testing with debug output" \
  --version 1.0 \
  --resources tasks.yaml \
  cli \
  --pkg debugapi \
  --client-pkg debugapi.client \
  --output - | less
```

Shows debug logs and pipes output to `less` for review.

---

## Environment Variables

While not command options, generated CLIs support these environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `API_URL` | Base API URL | `https://api.example.com` |
| `API_KEY` | API authentication key | `abc123...` |
| `CLIENT_CERT` | mTLS client certificate | `/path/to/cert.pem` |
| `CLIENT_KEY` | mTLS client key | `/path/to/key.pem` |
| `SSL_CA_CERT` | Custom CA bundle | `/path/to/ca-bundle.crt` |
| `REQUESTS_CA_BUNDLE` | Alternative CA bundle | `/path/to/ca-bundle.crt` |

Usage:

```bash
export API_URL=https://api.example.com
export API_KEY=my-secret-key
python cli.py tasks list  # Uses environment variables
```

---

## Validation

Firestone validates your options before generation:

### Resource Files

- Must exist and be readable
- Must be valid YAML or JSON
- Must pass JSON Schema validation

### Package Names

- Must be valid Python identifiers
- Should follow PEP 8 naming conventions

### Output Paths

- Parent directory must exist (for `--output`)
- Must be writable

### Template Files

- Must exist if specified
- Must be valid Jinja2 syntax

---

## Next Steps

- **[Generated Structure](./generated-structure)** - Understand the generated code
- **[CRUD Operations](./crud-operations)** - Use the generated CLI
- **[Customization](./customization)** - Customize templates
- **[Troubleshooting](../../advanced-topics/troubleshooting-generation-failures.md)** - Solve common issues
