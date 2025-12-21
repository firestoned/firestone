---
title: "firestone vs firestone-lib"
linkTitle: "firestone vs firestone-lib"
weight: 4
description: >
  Understanding when to use the CLI tool versus the programmatic library.
---

## Overview

The firestone ecosystem includes two separate but related packages:

- **`firestoned`** - The command-line tool (CLI)
- **`firestone-lib`** - The programmatic library

This guide explains the differences, when to use each, and how they relate.

## Package Names vs Module Names

First, let's clarify the naming:

### The 'd' Suffix Situation

**Installation names:**
```bash
pip install firestoned      # CLI tool
pip install firestone-lib   # Library
```

**Why "firestoned"?**
The name `firestone` was already taken on PyPI (though essentially unused). The firestone project publishes the CLI as `firestoned` with a 'd' suffix.

**Import names:**
```python
# After installing 'firestoned', import as:
import firestone

# After installing 'firestone-lib', import as:
import firestone_lib
```

**Command-line usage:**
```bash
# Both packages installed, command is:
firestone generate --resources book.yaml openapi
# No 'd' in the command
```

## firestone (CLI Tool)

### What It Is

A command-line application for generating specs and code from the terminal.

### Installation

```bash
# With Poetry (recommended)
poetry add firestoned

# With pip
pip install firestoned
```

### Usage

```bash
# Run commands from terminal
firestone generate --resources book.yaml openapi > spec.yaml
firestone generate --resources book.yaml cli > cli.py
firestone --version
firestone --help
```

### Key Features

**1. Terminal-First Interface**
- Designed for shell usage
- Pipes output to stdout or files
- Integrates with Unix tools

**2. Built-in UI Server**
- Launches Swagger UI for testing
- Quick visualization of specs

```bash
firestone generate --resources book.yaml openapi --ui-server
# Opens browser at http://127.0.0.1:5000/apidocs
```

**3. Simple Workflow**
- No programming required
- Direct file-to-file transformation
- Perfect for scripts and automation

**4. Multiple Output Formats**
- OpenAPI, AsyncAPI, CLI, Streamlit
- Output to stdout or files

### Use Cases

**Use the CLI when:**

- **Generating specs during development**
  ```bash
  firestone generate --resources *.yaml openapi > openapi.yaml
  ```

- **Building CI/CD pipelines**
  ```yaml
  # .github/workflows/generate.yml
  - name: Generate OpenAPI spec
    run: |
      poetry run firestone generate \
        --resources resources/*.yaml \
        openapi > openapi.yaml
  ```

- **One-off code generation**
  ```bash
  firestone generate --resources user.yaml cli > user_cli.py
  ```

- **Quick prototyping**
  ```bash
  firestone generate --resources proto.yaml openapi --ui-server
  ```

- **Shell scripting**
  ```bash
  #!/bin/bash
  for resource in resources/*.yaml; do
    name=$(basename "$resource" .yaml)
    firestone generate --resources "$resource" \
      openapi > "specs/${name}.yaml"
  done
  ```

### Advantages

- **Zero code** - Just run commands
- **Fast** - Quick iterations
- **Scriptable** - Easy automation
- **Self-contained** - Everything in one tool

### Limitations

- **Less flexible** - Command-line options only
- **No programmatic control** - Can't customize mid-generation
- **Limited integration** - Harder to embed in applications

## firestone-lib (Library)

### What It Is

A Python library providing programmatic access to firestone's generation capabilities.

### Installation

```bash
# With Poetry (recommended)
poetry add firestone-lib

# With pip
pip install firestone-lib
```

### Usage

```python
import yaml
from firestone_lib.spec import openapi, asyncapi, cli

# Load resource data
with open('book.yaml') as f:
    resource_data = [yaml.safe_load(f)]

# Generate OpenAPI spec programmatically
openapi_spec = openapi.generate(
    rsrc_data=resource_data,
    title='Library API',
    desc='API for managing books',
    summary='Book management',
    version='1.0.0'
)

print(openapi_spec)  # YAML string

# Generate AsyncAPI spec
asyncapi_spec = asyncapi.generate(
    rsrc_data=resource_data,
    title='Library Events',
    desc='WebSocket events',
    summary='Real-time book updates',
    version='1.0.0'
)

# Generate CLI code
cli_code = cli.generate(
    pkg='library',
    client_pkg='library.client',
    rsrc_data=resource_data,
    title='Library CLI',
    desc='Command-line interface',
    summary='CLI tool',
    version='1.0.0'
)
```

### Key Features

**1. Programmatic API**
- Full Python access to generation
- Customize behavior with code
- Integrate into applications

**2. Embeddable**
- Use in web apps, tools, frameworks
- Build custom workflows
- Extend functionality

**3. Flexible**
- Modify resources before generation
- Transform outputs after generation
- Build complex pipelines

**4. Reusable**
- Create libraries on top of firestone
- Share generation logic
- Build frameworks

### Use Cases

**Use the library when:**

- **Embedding in applications**
  ```python
  # Flask app that generates specs on-demand
  from flask import Flask, request, jsonify
  from firestone_lib.spec import openapi
  import yaml

  app = Flask(__name__)

  @app.route('/generate', methods=['POST'])
  def generate_spec():
      resource_yaml = request.data.decode('utf-8')
      resource = yaml.safe_load(resource_yaml)
      spec = openapi.generate(
          rsrc_data=[resource],
          title=request.args.get('title'),
          version='1.0.0'
      )
      return spec, 200, {'Content-Type': 'application/yaml'}
  ```

- **Building custom tools**
  ```python
  # Tool that validates and generates in one step
  class ResourceValidator:
      def __init__(self, schema_path):
          self.schema = load_json_schema(schema_path)

      def validate_and_generate(self, resource_file):
          with open(resource_file) as f:
              resource = yaml.safe_load(f)

          # Custom validation
          self.validate(resource)

          # Generate if valid
          return openapi.generate(
              rsrc_data=[resource],
              title=resource['kind'],
              version=resource['apiVersion']
          )
  ```

- **Dynamic resource generation**
  ```python
  # Generate resources from database schema
  def generate_from_db_schema(table_name):
      # Query database schema
      columns = get_table_columns(table_name)

      # Build resource definition
      resource = {
          'kind': table_name,
          'apiVersion': 'v1',
          'schema': {
              'type': 'array',
              'key': {'name': 'id', 'schema': {'type': 'integer'}},
              'items': {
                  'type': 'object',
                  'properties': {
                      col.name: {'type': map_db_type(col.type)}
                      for col in columns
                  }
              }
          }
      }

      # Generate OpenAPI spec
      return openapi.generate(
          rsrc_data=[resource],
          title=f"{table_name.title()} API",
          version='1.0.0'
      )
  ```

- **Custom templates**
  ```python
  # Use custom Jinja2 template
  from jinja2 import Environment, FileSystemLoader

  def generate_with_custom_template(resource, template_path):
      # Load resource
      with open(resource) as f:
          resource_data = [yaml.safe_load(f)]

      # Custom template environment
      env = Environment(loader=FileSystemLoader('.'))
      template = env.get_template(template_path)

      # Generate with custom context
      return template.render(
          resources=resource_data,
          custom_field='custom_value'
      )
  ```

- **Complex workflows**
  ```python
  # Multi-stage generation pipeline
  def build_api_package(resource_files, output_dir):
      # Stage 1: Load all resources
      resources = []
      for rf in resource_files:
          with open(rf) as f:
              resources.append(yaml.safe_load(f))

      # Stage 2: Generate OpenAPI
      openapi_spec = openapi.generate(
          rsrc_data=resources,
          title='Multi-Resource API',
          version='1.0.0'
      )

      # Stage 3: Write to file
      with open(f'{output_dir}/openapi.yaml', 'w') as f:
          f.write(openapi_spec)

      # Stage 4: Generate client SDK
      subprocess.run([
          'openapi-generator', 'generate',
          '-i', f'{output_dir}/openapi.yaml',
          '-g', 'python',
          '-o', f'{output_dir}/client'
      ])

      # Stage 5: Generate CLI
      cli_code = cli.generate(
          pkg='api',
          client_pkg='api.client',
          rsrc_data=resources,
          title='API CLI',
          version='1.0.0'
      )

      with open(f'{output_dir}/cli.py', 'w') as f:
          f.write(cli_code)

      return output_dir
  ```

### Advantages

- **Programmable** - Full Python control
- **Flexible** - Customize everything
- **Embeddable** - Use in any Python app
- **Extensible** - Build on top of it

### Limitations

- **Requires programming** - Not for non-coders
- **More complex** - Need to write code
- **Dependencies** - Manage as a library

## Side-by-Side Comparison

| Feature | firestone (CLI) | firestone-lib (Library) |
|---------|-----------------|-------------------------|
| **Installation** | `pip install firestoned` | `pip install firestone-lib` |
| **Usage** | Command line | Python code |
| **Skill Required** | Basic shell | Python programming |
| **Primary Use** | Generation tasks | Embedded generation |
| **Flexibility** | Command options | Full programmatic control |
| **Integration** | Shell scripts, CI/CD | Applications, tools, frameworks |
| **Customization** | Limited to flags | Unlimited with code |
| **Learning Curve** | Low | Medium |
| **Output** | Stdout or files | Python strings |
| **Templates** | File-based | File or programmatic |
| **Best For** | Quick generation | Complex workflows |

## When to Use Both

Many projects use both packages for different purposes:

### Example Workflow

**Development (CLI):**
```bash
# Quick iteration during development
poetry run firestone generate --resources book.yaml openapi --ui-server
```

**CI/CD (CLI):**
```yaml
# .github/workflows/specs.yml
- name: Generate specs
  run: |
    poetry run firestone generate \
      --resources resources/*.yaml \
      openapi > openapi.yaml
```

**Production Application (Library):**
```python
# app.py - Generate specs dynamically
from firestone_lib.spec import openapi

@app.route('/api/schema/<resource>')
def get_resource_schema(resource):
    resource_def = load_resource(resource)
    spec = openapi.generate(
        rsrc_data=[resource_def],
        title=f"{resource} API",
        version='1.0.0'
    )
    return spec
```

## Choosing Between Them

### Use firestone (CLI) if you:

- ✅ Want to generate specs from the command line
- ✅ Are building CI/CD pipelines
- ✅ Prefer declarative, file-based workflows
- ✅ Don't need programmatic customization
- ✅ Want quick, one-off generation

### Use firestone-lib if you:

- ✅ Need to embed generation in Python applications
- ✅ Want programmatic control over generation
- ✅ Are building tools or frameworks
- ✅ Need dynamic or conditional generation
- ✅ Want to extend firestone's capabilities

### Use both if you:

- ✅ Develop locally with CLI, deploy with library
- ✅ Use CLI in CI/CD, library in production
- ✅ Want flexibility across different contexts

## Installation Together

Both can be installed side-by-side:

```bash
# Install both
poetry add firestoned firestone-lib

# Use CLI
poetry run firestone generate --resources book.yaml openapi

# Use library in Python scripts
python my_generator.py
```

They don't conflict and can be used together in the same project.

## Migration Between Them

### From CLI to Library

If you outgrow the CLI:

**Before (CLI):**
```bash
firestone generate --resources book.yaml openapi > openapi.yaml
```

**After (Library):**
```python
from firestone_lib.spec import openapi
import yaml

with open('book.yaml') as f:
    resource = yaml.safe_load(f)

spec = openapi.generate(
    rsrc_data=[resource],
    title='Book API',
    version='1.0.0'
)

with open('openapi.yaml', 'w') as f:
    f.write(spec)
```

### From Library to CLI

If you want simpler workflows:

**Before (Library):**
```python
spec = openapi.generate(...)
with open('openapi.yaml', 'w') as f:
    f.write(spec)
```

**After (CLI):**
```bash
firestone generate --resources book.yaml openapi > openapi.yaml
```

## Documentation and Support

**CLI Documentation:**
- Command-line help: `firestone --help`
- This documentation site
- Examples in the repo

**Library Documentation:**
- API docs (autodoc)
- Source code
- This documentation site

## Next Steps

Now that you understand the difference:

- **Using the CLI:** See [OpenAPI Generation](../../openapi-generation/), [AsyncAPI Generation](../../asyncapi-generation/), [CLI Generation](../../cli-generation/)
- **Using the Library:** See [Developer Guide](../../developer/), [API Reference](../../reference/)
- **Examples:** [Addressbook Tutorial](../../examples/addressbook-tutorial)

