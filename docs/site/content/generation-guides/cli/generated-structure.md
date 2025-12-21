---
title: "Generated CLI Structure"
linkTitle: "Generated Structure"
weight: 4
description: >
  Understanding the structure and components of firestone-generated CLI code.
---

## Overview

Firestone generates complete, production-ready CLI applications using the Click framework. Understanding the generated structure helps you customize, extend, and troubleshoot your CLIs.

## File Structure

### Single File Mode (Default)

```python
#!/usr/bin/env python
"""
Main entry point for a click based CLI.
"""

# 1. Imports
# 2. Exception Handler
# 3. Main Command Group
# 4. Resource Command Groups
# 5. Operation Commands
# 6. Entry Point
```

### Module Mode (--as-modules)

```
cli/
├── __init__.py     # You create this
├── tasks.py        # Generated
├── projects.py     # Generated
└── users.py        # Generated
```

Each module:
```python
# 1. Imports
# 2. Exception Handler
# 3. init() Function
#    ├── Resource Command Group
#    ├── Operation Commands
#    └── Return Command Group
```

## Section Breakdown

### 1. Shebang and Docstring

```python
#!/usr/bin/env python
"""
Main entry point for a click based CLI.
"""
```

**Purpose:**
- Makes file executable on Unix systems
- Documents the script purpose

**Usage:**
```bash
chmod +x cli.py
./cli.py --help
```

---

### 2. Imports

```python
import functools
import json
import logging
import os
import sys

import click
from firestone_lib import cli
from firestone_lib import utils as firestone_utils

from {{ client_pkg }} import api_client
from {{ client_pkg }} import configuration
from {{ client_pkg }} import exceptions

# Resource-specific imports
from {{ client_pkg }}.api import tasks_api
from {{ client_pkg }}.models import task as task_model
from {{ client_pkg }}.models import create_task as create_task_model
from {{ client_pkg }}.models import update_task as update_task_model
```

**Import groups:**
1. **Standard library** - Python built-ins
2. **Third-party** - Click framework
3. **Firestone** - CLI utilities
4. **Client** - OpenAPI-generated client
5. **Resource models** - API data models

**Conditional imports:**
- `create_*` models only if resource has POST
- `update_*` models only if resource has PUT/PATCH

---

### 3. Logger

```python
_LOGGER = logging.getLogger(__name__)
```

**Usage in commands:**
```python
_LOGGER.debug(f"resp: {resp}")
_LOGGER.info("Calling API...")
```

**Control with --debug:**
```bash
python cli.py --debug tasks list
# Enables DEBUG level logging
```

---

### 4. Exception Handler

```python
def api_exc(func):
    """Handle ApiExceptions in all functions."""
    async def wrapper(*args, **kwargs):
        resp = None
        try:
            return await func(*args, **kwargs)
        except exceptions.ApiException as apie:
            if apie.body:
                click.echo(apie.body)
            else:
                click.echo(apie.reason)

            api_obj = args[0].get("api_obj")
            if api_obj:
                await api_obj.api_client.close()
        sys.exit(-1)

    return functools.update_wrapper(wrapper, func)
```

**Purpose:**
- Catches API exceptions from client library
- Displays error messages to user
- Properly closes API client
- Exits with error code

**Applied to all commands:**
```python
@api_exc
async def tasks_get(ctx_obj):
    # If API raises exception, api_exc catches it
```

---

### 5. Main Command Group

```python
@click.group()
@click.option("--debug", help="Turn on debugging", is_flag=True)
@click.option(
    "--api-key",
    help="The API key to authorize against API",
    envvar="API_KEY",
)
@click.option(
    "--api-url",
    help="The API url, e.g. https://localhost",
    envvar="API_URL",
)
@click.option(
    "--client-cert",
    help="Path to the client cert for mutual TLS",
    envvar="CLIENT_CERT",
)
@click.option(
    "--client-key",
    help="Path to the client key for mutual TLS",
    envvar="CLIENT_KEY",
)
@click.option("--trust-proxy", help="Trust the proxy env vars", is_flag=True, default=False)
@click.pass_context
def main(ctx, debug, api_key, api_url, client_cert, client_key, trust_proxy):
    """{{ title }}

    {{ description }}
    """
```

**Global options:**
- `--debug` - Enable debug logging
- `--api-key` - API authentication (or `API_KEY` env var)
- `--api-url` - Base API URL (or `API_URL` env var)
- `--client-cert` - mTLS certificate (or `CLIENT_CERT` env var)
- `--client-key` - mTLS key (or `CLIENT_KEY` env var)
- `--trust-proxy` - Respect HTTP proxy environment variables

**Main function body:**

```python
    # Remove proxy env vars unless --trust-proxy
    if not trust_proxy:
        for prefix in ["http", "https", "all_http", "all_https"]:
            env_var = f"{prefix}_proxy"
            if env_var in os.environ:
                del os.environ[env_var]
            if env_var.upper() in os.environ:
                del os.environ[env_var.upper()]

    # Setup logging
    try:
        cli.init_logging("{{ pkg }}.resources.logging", "cli.conf")
    except Exception:
        logging.basicConfig(
            level=logging.INFO,
            format="# %(asctime)s - [%(threadName)s] %(name)s:%(lineno)d %(levelname)s - %(message)s",
        )

    # Enable debug if requested
    logging.getLogger("asyncio").setLevel(logging.CRITICAL)
    if debug:
        _LOGGER.setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("{{ pkg }}").setLevel(logging.DEBUG)
        logging.getLogger("aiohttp").setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.DEBUG)
        logging.getLogger("httplib").setLevel(logging.DEBUG)

    # Configure API client
    config = configuration.Configuration(host=api_url)
    config.debug = debug
    if api_key:
        config.access_token = api_key
    if client_cert:
        config.cert_file = client_cert
    if client_key:
        config.key_file = client_key
    if "SSL_CA_CERT" in os.environ:
        config.ssl_ca_cert = os.environ["SSL_CA_CERT"]
    if "REQUESTS_CA_BUNDLE" in os.environ:
        config.ssl_ca_cert = os.environ["REQUESTS_CA_BUNDLE"]

    # Store config in context
    ctx.obj = {
        "api_client_config": config,
    }
```

---

### 6. Resource Command Groups

One group per resource:

```python
@main.group()
@firestone_utils.click_coro
@click.pass_obj
async def tasks(ctx_obj):
    """High level command for tasks."""
    _LOGGER.debug(f"ctx_obj: {ctx_obj}")
    config = ctx_obj["api_client_config"]
    aclient = api_client.ApiClient(configuration=config)
    ctx_obj["api_obj"] = tasks_api.TasksApi(api_client=aclient)
```

**Key components:**
- `@main.group()` - Nest under main
- `@firestone_utils.click_coro` - Enable async
- `@click.pass_obj` - Receive context from main
- Initialize resource-specific API client
- Store API client in context for commands

**Usage:**
```bash
python cli.py tasks --help
```

---

### 7. Resource Operations (Collection)

Operations on the resource collection (`/tasks`):

```python
@tasks.command("list")
@click.option("--limit", help="Limit the number of responses back", type=int, show_default=True, required=False)
@click.option("--offset", help="The offset to start returning resources", type=int, show_default=True, required=False)
@click.pass_obj
@firestone_utils.click_coro
@api_exc
async def tasks_get(ctx_obj, limit, offset):
    """List all tasks in this collection"""
    api_obj = ctx_obj["api_obj"]
    params = {
        "limit": limit,
        "offset": offset,
    }

    resp = await api_obj.tasks_get(**params)
    _LOGGER.debug(f"resp: {resp}")

    if isinstance(resp, list):
        click.echo(json.dumps([obj.to_dict() for obj in resp]))
        return

    if resp:
        click.echo(json.dumps(resp.to_dict()))
        return

    click.echo("No data returned")
```

**Command name mapping:**
- `GET /tasks` → `list`
- `POST /tasks` → `create`

**Response handling:**
- List of objects → JSON array
- Single object → JSON object
- No data → "No data returned"

---

### 8. Resource Operations (Instance)

Operations on individual resources (`/tasks/{task_id}`):

```python
@tasks.command("get")
@click.argument("task_id", type=str)
@click.pass_obj
@firestone_utils.click_coro
@api_exc
async def tasks_task_id_get(ctx_obj, task_id):
    """Get a specific task from this collection"""
    api_obj = ctx_obj["api_obj"]
    params = {}

    resp = await api_obj.tasks_task_id_get(task_id, **params)
    _LOGGER.debug(f"resp: {resp}")

    if isinstance(resp, list):
        print(json.dumps([obj.to_dict() for obj in resp]))
        return

    print(json.dumps(resp.to_dict()) if resp else "None")
```

**Command name mapping:**
- `GET /tasks/{id}` → `get`
- `PUT /tasks/{id}` → `update`
- `DELETE /tasks/{id}` → `delete`

**Key differences:**
- Uses `@click.argument` for ID (positional)
- Uses `@click.option` for other parameters
- ID is passed as first argument to API method

---

### 9. Create Operation

```python
@tasks.command("create")
@click.option("--title", help="Task title", type=str, show_default=True, required=True)
@click.option("--completed/--no-completed", help="Task completion status", is_flag=True, show_default=True, required=False)
@click.pass_obj
@firestone_utils.click_coro
@api_exc
async def tasks_post(ctx_obj, title, completed):
    """Create a new task in this collection"""
    api_obj = ctx_obj["api_obj"]
    params = {
        "title": title,
        "completed": completed,
    }

    req_body = create_task_model.CreateTask(**params)
    resp = await api_obj.tasks_post(req_body)
    _LOGGER.debug(f"resp: {resp}")

    if isinstance(resp, list):
        click.echo(json.dumps([obj.to_dict() for obj in resp]))
        return

    if resp:
        click.echo(json.dumps(resp.to_dict()))
        return

    click.echo("No data returned")
```

**Special handling:**
- Creates model instance from parameters
- Passes model as request body
- Uses `CreateTask` model (from OpenAPI spec)

---

### 10. Update Operation

```python
@tasks.command("update")
@click.option("--title", help="Task title", type=str, required=False)
@click.option("--completed/--no-completed", help="Task completion status", is_flag=True, required=False)
@click.argument("task_id", type=str)
@click.pass_obj
@firestone_utils.click_coro
@api_exc
async def tasks_task_id_put(ctx_obj, title, completed, task_id):
    """Update an existing task in this collection"""
    api_obj = ctx_obj["api_obj"]
    params = {
        "title": title,
        "completed": completed,
    }

    req_body = update_task_model.UpdateTask(**params)
    resp = await api_obj.tasks_task_id_put(task_id, req_body)
    _LOGGER.debug(f"resp: {resp}")

    if isinstance(resp, list):
        print(json.dumps([obj.to_dict() for obj in resp]))
        return

    print(json.dumps(resp.to_dict()) if resp else "None")
```

**Special handling:**
- Combines ID argument with optional update fields
- Creates `UpdateTask` model
- Fields typically not required (partial update)

---

### 11. Entry Point

```python
if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
```

**Allows direct execution:**
```bash
python cli.py --help
```

---

## Module Structure (--as-modules)

Each module exports an `init()` function:

```python
def init():
    """Initialize tasks resource CLI."""

    @click.group()
    @firestone_utils.click_coro
    @click.pass_obj
    async def tasks(ctx_obj):
        """High level command for tasks."""
        # ... setup ...

    @tasks.command("list")
    @click.pass_obj
    @firestone_utils.click_coro
    @api_exc
    async def tasks_get(ctx_obj):
        # ... operation ...

    # ... more operations ...

    return tasks
```

**Integration example:**

```python
# main.py
import click
from myapi.cli import tasks
from myapi.cli import projects

@click.group()
@click.option("--api-url", envvar="API_URL")
@click.pass_context
def main(ctx, api_url):
    """My API CLI"""
    # ... setup config ...

# Register resource command groups
tasks_cli = tasks.init()
projects_cli = projects.init()
main.add_command(tasks_cli)
main.add_command(projects_cli)

if __name__ == "__main__":
    main()
```

---

## Code Patterns

### Consistent Decorator Order

All commands follow this pattern:

```python
@<group>.command("<name>")
@click.option(...) / @click.argument(...)  # Options/args first
@click.pass_obj                            # Pass context
@firestone_utils.click_coro                # Enable async
@api_exc                                   # Exception handling
async def command_name(ctx_obj, ...):
    # Implementation
```

### Consistent Response Handling

```python
if isinstance(resp, list):
    click.echo(json.dumps([obj.to_dict() for obj in resp]))
    return

if resp:
    click.echo(json.dumps(resp.to_dict()))
    return

click.echo("No data returned")
```

### Context Usage

```python
# Main stores config
ctx.obj = {"api_client_config": config}

# Resource group adds API client
ctx_obj["api_obj"] = tasks_api.TasksApi(...)

# Commands use API client
api_obj = ctx_obj["api_obj"]
resp = await api_obj.tasks_get()
```

---

## Customization Points

### 1. Add Custom Commands

```python
@tasks.command("export")
@click.option("--format", type=click.Choice(["csv", "json"]))
@click.pass_obj
@firestone_utils.click_coro
@api_exc
async def export_tasks(ctx_obj, format):
    """Export tasks to file"""
    # Custom implementation
```

### 2. Modify Response Formatting

```python
# Instead of JSON
click.echo(json.dumps(resp.to_dict()))

# Use table format
from tabulate import tabulate
table = [[t.id, t.title, t.completed] for t in resp]
click.echo(tabulate(table, headers=["ID", "Title", "Done"]))
```

### 3. Add Global Options

```python
@main.option("--timeout", type=int, default=30)
def main(ctx, api_url, timeout, ...):
    config = configuration.Configuration(host=api_url)
    config.timeout = timeout
```

---

## Next Steps

- **[CRUD Operations](./crud-operations)** - Use the generated commands
- **[Integration](../../advanced-topics/docker-integration.md)** - Connect with OpenAPI clients
- **[Customization](./customization)** - Modify templates
- **[Usage Examples](cli-usage-examples.md)** - Real-world scenarios
