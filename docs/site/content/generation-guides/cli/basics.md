+++
title = "CLI Basics"
linkTitle = "CLI Basics"
weight = 1
description = "How firestone generates command-line interfaces with full CRUD operations."
+++

## From Resource to Command-Line Tool - Automatically

Firestone generates Python CLIs using the Click framework ([docs](https://click.palletsprojects.com/)). But here's what matters: **you don't write any Click code**.

Define your resource, and firestone creates a fully functional command-line tool with CRUD operations, argument parsing, help text, and validation - all automatically.

## What Gets Generated

From this simple resource:

```yaml
kind: book
schema:
  type: array
  key:
    name: book_id
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

Firestone generates these commands:

```bash
# List all books
python cli.py books list

# Create a new book
python cli.py books create --title "The Great Gatsby" --author "F. Scott Fitzgerald" --isbn "978-0743273565"

# Get a specific book
python cli.py books get book-123

# Update a book
python cli.py books update book-123 --title "Updated Title"

# Delete a book
python cli.py books delete book-123
```

**Each command includes:**
- Proper argument parsing (strings, numbers, booleans, enums)
- Validation from your JSON Schema
- Help text from your descriptions
- Error handling and formatting

## How It Works

Firestone analyzes your resource and generates:

**CRUD Operations**
- `list` - GET all resources (with pagination options)
- `create` - POST a new resource
- `get` - GET a specific resource by ID
- `update` - PUT/PATCH to modify a resource
- `delete` - DELETE a resource

**Smart Arguments**
- Required fields become required options: `--title` (required)
- Optional fields become optional: `--isbn` (optional)
- Enums become choices: `--status [active|inactive|archived]`
- Nested objects accept JSON: `--address '{"city": "NYC"}'`

**Built-in Features**
- `--host` to point to different API servers
- `--format [json|yaml|table]` for output formatting
- `--limit` and `--offset` for pagination
- Help text: `python cli.py books --help`

> 💡 **One Definition, Four Outputs**
> This same resource definition also generates [OpenAPI](../openapi/) (REST specs), [AsyncAPI](../asyncapi/) (WebSocket specs), and [Streamlit UI](../streamlit/) (web dashboards).

## Why This Matters

**Instant Testing**
Generate your OpenAPI spec and CLI together. Test your API design without writing a server:
```bash
firestone generate --resources book.yaml openapi > spec.yaml
firestone generate --resources book.yaml cli > cli.py
# Now test with: python cli.py books create --title "Test"
```

**Scripting & Automation**
CLIs are perfect for:
- CI/CD pipelines
- Cron jobs
- Admin tasks
- Bulk operations

**Consistency Guaranteed**
The CLI uses your OpenAPI spec. If the spec validates correctly, the CLI works correctly. Change your resource, regenerate both - they stay in sync.

## Multi-Resource CLIs

Define multiple resources, get one CLI with all of them:

```bash
firestone generate \
    --resources book.yaml,author.yaml,publisher.yaml \
    cli > cli.py

# Now you have:
python cli.py books list
python cli.py authors list
python cli.py publishers list
```

All following the same command structure, all with proper validation, all from your resource definitions.

---
## Next Steps

Ready to generate your first CLI?
- **Next:** Learn the commands in **[Generating CLIs](./generating)**.
