---
title: "CLI Command Reference"
linkTitle: "CLI Commands"
weight: 1
description: >
  Complete reference for all firestone CLI commands, options, and arguments.
---

## Overview

The `firestone` CLI provides commands to generate various outputs from resource definitions. This reference covers all commands, global options, and generator-specific options.

## Command Structure

```bash
firestone [GLOBAL_OPTIONS] generate [GENERATE_OPTIONS] <generator> [GENERATOR_OPTIONS]
```

## Global Options

These options apply to all firestone commands:

| Option | Description | Example |
|--------|-------------|---------|
| `--help` | Show help message | `firestone --help` |
| `--version` | Show version | `firestone --version` |
| `--debug` | Enable debug logging | `firestone --debug generate ...` |
| `--verbose`, `-v` | Verbose output | `firestone -v generate ...` |

## Generate Command

The main command for generating outputs from resource definitions.

### Syntax

```bash
firestone generate [OPTIONS] <generator>
```

### Common Options

| Option | Short | Required | Description | Example |
|--------|-------|----------|-------------|---------|
| `--resources <path>` | `-r` | ✅ Yes | Path to resource YAML file(s) or directory | `--resources user.yaml` |
| `--title <string>` | `-t` | ⚠️ Varies | Title for generated output | `--title "My API"` |
| `--description <string>` | `-d` | ❌ No | Description for generated output | `--description "User management API"` |
| `--version <string>` |  | ❌ No | API version | `--version "1.0.0"` |
| `--output <file>` | `-o` | ❌ No | Output file (default: stdout) | `--output spec.yaml` |

### Generators

Firestone supports four generators: `openapi`, `asyncapi`, `cli`, and `streamlit`.

---

## OpenAPI Generator

Generate OpenAPI 3.0.0 specifications from resources.

### Syntax

```bash
firestone generate --resources <path> [OPTIONS] openapi [OPENAPI_OPTIONS]
```

### Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--title` | ✅ Yes | - | API title |
| `--description` | ❌ No | "" | API description |
| `--version` | ❌ No | "1.0" | API version |
| `--server <url>` | ❌ No | - | Server URL (can be specified multiple times) |
| `--ui-server` | ❌ No | False | Start Swagger UI server after generation |
| `--ui-port <port>` | ❌ No | 5000 | Port for Swagger UI server |
| `--output` | ❌ No | stdout | Output file path |

### Examples

**Basic generation:**
```bash
firestone generate \
  --resources resources/ \
  --title "My API" \
  openapi > openapi.yaml
```

**With servers and version:**
```bash
firestone generate \
  --resources user.yaml \
  --title "User API" \
  --description "User management system" \
  --version "2.1.0" \
  openapi \
  --server https://api.example.com \
  --server https://api-staging.example.com \
  > openapi.yaml
```

**With Swagger UI:**
```bash
firestone generate \
  --resources resources/ \
  --title "My API" \
  openapi \
  --ui-server \
  --ui-port 8080
```

This opens Swagger UI at `http://localhost:8080/apidocs`.

### Output

Generates OpenAPI 3.0.0 YAML with:
- Complete path definitions (resource and instance endpoints)
- Request/response schemas
- Query parameters
- Security schemes
- Server configurations

---

## AsyncAPI Generator

Generate AsyncAPI 2.5.0 specifications for event-driven APIs.

### Syntax

```bash
firestone generate --resources <path> [OPTIONS] asyncapi [ASYNCAPI_OPTIONS]
```

### Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--title` | ✅ Yes | - | AsyncAPI title |
| `--description` | ❌ No | "" | AsyncAPI description |
| `--version` | ❌ No | "1.0" | AsyncAPI version |
| `--server <url>` | ❌ No | - | Server URL |
| `--protocol <proto>` | ❌ No | "ws" | Protocol (ws, wss, http, https) |
| `--output` | ❌ No | stdout | Output file path |

### Examples

**WebSocket API:**
```bash
firestone generate \
  --resources message.yaml \
  --title "Chat API" \
  asyncapi \
  --protocol wss \
  --server wss://chat.example.com > asyncapi.yaml
```

**HTTP streaming:**
```bash
firestone generate \
  --resources events.yaml \
  --title "Event Stream" \
  asyncapi \
  --protocol https \
  --server https://events.example.com > asyncapi.yaml
```

### Output

Generates AsyncAPI 2.5.0 YAML with:
- Channel definitions
- Message schemas
- Subscribe/publish operations
- Server and protocol bindings

---

## CLI Generator

Generate Python Click-based command-line interfaces.

### Syntax

```bash
firestone generate --resources <path> [OPTIONS] cli [CLI_OPTIONS]
```

### Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--title` | ✅ Yes | - | CLI application name |
| `--pkg <name>` | ✅ Yes | - | Package name for CLI module |
| `--client-pkg <name>` | ✅ Yes | - | Client package name (for API calls) |
| `--output` | ❌ No | stdout | Output file path |

### Examples

**Generate CLI:**
```bash
firestone generate \
  --resources user.yaml \
  --title "User CLI" \
  cli \
  --pkg myapp_cli \
  --client-pkg myapp_client > cli.py
```

**Multi-resource CLI:**
```bash
firestone generate \
  --resources resources/ \
  --title "Management CLI" \
  cli \
  --pkg management \
  --client-pkg api_client > management_cli.py
```

### Output

Generates Python file with:
- Click CLI application
- CRUD commands (list, get, create, update, delete)
- JSON output formatting
- Error handling
- Integration with API client

### Generated Commands

For a resource named `users`:

```bash
python cli.py users list              # List all users
python cli.py users get <user_id>     # Get specific user
python cli.py users create <json>     # Create user
python cli.py users update <id> <json> # Update user
python cli.py users delete <user_id>  # Delete user
```

---

## Streamlit Generator

Generate Streamlit data applications for CRUD operations.

### Syntax

```bash
firestone generate --resources <path> [OPTIONS] streamlit [STREAMLIT_OPTIONS]
```

### Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--title` | ✅ Yes | - | Streamlit app title |
| `--backend-url <url>` | ✅ Yes | - | Backend API URL |
| `--output` | ❌ No | stdout | Output file path |

### Examples

**Generate Streamlit app:**
```bash
firestone generate \
  --resources product.yaml \
  --title "Product Manager" \
  streamlit \
  --backend-url http://localhost:8000 > app.py
```

**Multi-resource dashboard:**
```bash
firestone generate \
  --resources resources/ \
  --title "Admin Dashboard" \
  streamlit \
  --backend-url https://api.example.com > dashboard.py
```

### Output

Generates Python Streamlit application with:
- Sidebar navigation
- List/table view
- Create form
- Edit form
- Delete confirmation
- API integration

### Running Generated App

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`.

---

## Multiple Resources

All generators support multiple resources via:

**Directory of resource files:**
```bash
firestone generate --resources resources/ openapi
```

**Multiple file arguments:**
```bash
firestone generate \
  --resources user.yaml \
  --resources product.yaml \
  --resources order.yaml \
  openapi
```

**Glob patterns** (shell expansion):
```bash
firestone generate --resources resources/*.yaml openapi
```

---

## Output Redirection

All generators output to stdout by default. Redirect to files:

```bash
# Redirect stdout
firestone generate --resources user.yaml openapi > spec.yaml

# Use --output flag
firestone generate --resources user.yaml --output spec.yaml openapi

# Pipe to other commands
firestone generate --resources user.yaml openapi | spectral lint -
```

---

## Environment Variables

Firestone respects these environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `FIRESTONE_DEBUG` | Enable debug mode | `export FIRESTONE_DEBUG=1` |
| `FIRESTONE_LOG_LEVEL` | Set log level | `export FIRESTONE_LOG_LEVEL=DEBUG` |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Resource file not found |
| 4 | Resource validation failed |
| 5 | Generation failed |

---

## Common Patterns

### Generate All Outputs

```bash
# Generate OpenAPI spec
firestone generate -r resources/ -t "My API" openapi > openapi.yaml

# Generate AsyncAPI spec
firestone generate -r resources/ -t "My API" asyncapi > asyncapi.yaml

# Generate CLI
firestone generate -r resources/ -t "My API" cli --pkg myapi --client-pkg myapi_client > cli.py

# Generate Streamlit UI
firestone generate -r resources/ -t "My API" streamlit --backend-url http://localhost:8000 > app.py
```

### CI/CD Integration

```bash
#!/bin/bash
set -e

# Generate spec
firestone generate \
  --resources resources/ \
  --title "${API_TITLE}" \
  --version "${GIT_SHA}" \
  openapi > openapi.yaml

# Validate
spectral lint openapi.yaml

# Generate clients
openapi-generator generate -i openapi.yaml -g python -o client/
```

### Development Workflow

```bash
# Watch for changes and regenerate
while inotifywait -e modify resources/*.yaml; do
  firestone generate -r resources/ -t "Dev API" openapi --ui-server
done
```

---

## Getting Help

**Command help:**
```bash
firestone --help
firestone generate --help
firestone generate openapi --help
```

**Version information:**
```bash
firestone --version
```

**Debug output:**
```bash
firestone --debug generate --resources user.yaml openapi
```

---

## See Also

- **[Quickstart Tutorial](../getting-started/quickstart)** - First steps with firestone
- **[Resource Schema Reference](./resource-schema-quick-reference)** - YAML structure reference
- **[Examples](../examples/)** - Complete working examples
- **[Best Practices](common-patterns-cheat-sheet.md)** - Recommended patterns
