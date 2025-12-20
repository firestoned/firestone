---
title: "Customizing Your CLI"
linkTitle: "CLI Customization"
weight: 4
description: >
  Learn how to extend and tailor your firestone-generated CLI tools with custom commands, templates, and integration logic.
---

## Tailoring Your CLI to Perfection

`firestone` generates a robust and functional CLI directly from your resource blueprints. This covers the vast majority of common API interactions. However, real-world applications often have unique requirements, bespoke commands, or specific integration patterns that go beyond standard CRUD.

This section explores how you can customize and extend your `firestone`-generated CLI tools to perfectly match your needs, leveraging the power of the underlying [Click framework](https://click.palletsprojects.com/).

## 1. The Power of Jinja2 Templates

`firestone` uses **Jinja2 templates** to generate the Python code for your CLI. This is the ultimate customization mechanism. By providing your own custom template, you can completely redefine how your CLI looks and behaves.

### Providing a Custom Template (`--template`)
You can specify a path to your custom Jinja2 template file using the `--template` option when generating your CLI:

```bash
firestone generate \
  --resources books.yaml \
  --title "My Custom Library CLI" \
  --description "A highly customized CLI for my library." \
  --version "0.1.0" \
  --pkg "my_library_cli" \
  --client-pkg "library_client" \
  cli --output my_library_cli.py --template ./my_custom_cli_template.py.jinja
```

### What You Can Customize:
-   **Command Structure:** Change how commands and groups are defined.
-   **Default Options:** Add global options to your CLI.
-   **Command Logic:** Inject custom Python code into generated commands (e.g., pre-processing inputs, adding validation, custom output formatting).
-   **Custom Subcommands:** Add entirely new subcommands to resource groups.

> **When to use:** This is for advanced users who need to fundamentally alter the generated CLI's logic or structure. It requires understanding Jinja2 templating and the `firestone` internal data structures passed to the template.

## 2. Adding Custom Commands and Groups

While `firestone` generates commands for your API resources, you might need additional utility commands that aren't directly tied to a REST endpoint (e.g., `my_cli config set`, `my_cli deploy`).

If you use the modular generation (`--as-modules`), you can easily add custom commands by:

1.  **Creating a new Python file** in your `--output-dir` (or modifying the main `main.py`).
2.  **Using standard Click decorators** to define your new commands and groups.
3.  **Ensuring your main `cli` group imports and registers these new commands.**

### Example: Adding a `config` command

Assuming a modular CLI generated into `my_cli_package/`:

**`my_cli_package/config.py`:**
```python
import click

@click.group()
def config():
    """Manage CLI configuration."""
    pass

@config.command()
@click.argument('key')
@click.argument('value')
def set(key, value):
    """Set a configuration key-value pair."""
    click.echo(f"Setting {key} to {value}")

@config.command()
@click.argument('key')
def get(key):
    """Get a configuration value."""
    click.echo(f"Getting value for {key}")
```

**`my_cli_package/main.py` (modified to import and register):**
```python
# ... existing imports ...
from my_cli_package.config import config # Import your new command group

@click.group()
@click.option("--debug", is_flag=True, help="Turn on debugging")
def cli(debug):
    """Main entry point for your CLI."""
    # ... existing logic ...

cli.add_command(config) # <--- Add this line to register the new group
# ... existing resource commands (books, authors, etc.) ...
```
Now, your CLI will have a new `config` group:
```bash
python my_cli_package/main.py config set token abc123
```

## 3. Injecting Custom Logic into Generated Commands

You might want to add custom validation, logging, or pre/post-processing to a command that `firestone` generates. This can be done by:

-   **Modifying the generated files (temporarily):** For quick tests, but be aware changes will be overwritten on regeneration.
-   **Using Click decorators/callbacks:** If `firestone`'s template exposes hooks, you can use Click's extensibility.
-   **Custom Templates:** The most robust solution for permanent changes.

## 4. Integrating with External Python Libraries

Since your generated CLI is standard Python, you can import and use any other Python library within your custom commands or modifications. For instance, you might use a specific logging library, a database ORM, or a data processing tool.

## Best Practices for Customization

### 1. Version Control Your Customizations
If you're using custom templates, make sure they are stored in your version control system.

### 2. Isolate Custom Logic
When adding custom commands or modifying generated ones, try to keep your custom logic in separate modules or well-defined functions. This makes your CLI easier to maintain and upgrade.

### 3. Test Your Customizations
Always write tests for your custom commands and any modifications you make to the generated CLI.

### 4. Provide Good Help Text
Ensure your custom commands, options, and arguments have clear and informative help text, following Click's conventions.

---
## Next Steps

You've learned how to tailor your CLI. Now, let's see some common commands in action.
- **Next:** Explore practical interactions in **[CLI Usage Examples](./cli-usage-examples)**.
