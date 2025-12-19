---
title: "Generating CLI Tools"
linkTitle: "Generating CLI"
weight: 2
description: >
  Learn the simple `firestone` commands to transform your resource blueprints into powerful, Python Click-based CLI tools.
---

## Your API, From the Command Line

You've defined your API's blueprint. `firestone` can generate its OpenAPI contract and even event-driven AsyncAPI specs. But for many developers and administrators, the most direct way to interact with an API is through a command-line interface (CLI).

`firestone` makes it incredibly easy to create a functional, Python [Click](https://click.palletsprojects.com/)-based CLI tool that mirrors your API's operations. This generated CLI allows you to:

-   List, create, retrieve, update, and delete resources directly from your terminal.
-   Integrate API interactions into shell scripts and automation workflows.
-   Provide a developer-friendly interface that reflects your API's design.

## The `firestone generate cli` Command

The core command for building your CLI is `firestone generate cli`.

```bash
firestone generate cli [OPTIONS]
```

This command takes your resource blueprint(s) and, combining them with your defined methods and schemas, produces a robust Python CLI.

### Core `generate` Options (Required for `cli`)

These options provide the high-level metadata for your CLI, appearing in help texts and package metadata.

-   **`--resources`, `-r`** `TEXT` (Required): One or more resource files in JSON Schema format (can be JSON or YAML). This tells `firestone` *which* blueprints to use for your CLI.
-   **`--title`, `-t`** `TEXT` (Required): The overall title of your CLI application.
-   **`--description`, `-d`** `TEXT` (Required): A high-level description for your CLI.
-   **`--version`, `-v`** `TEXT` (Required): The version of your CLI application.
-   **`--summary`, `-s`** `TEXT` (Optional): A short summary for your CLI.

### `cli` Specific Options

These options allow you to control the output format and dependencies of your generated CLI.

-   **`--language`, `-l`** `TEXT` (Default: `python`): The target language for the CLI. Supported values: `python`, `rust`.
-   **`--output`, `-O`** `TEXT` (Default: `-` for stdout): Where to save the main generated CLI file.
    -   Use `-` to print the CLI code directly to your console.
    -   Provide a filename (e.g., `my_cli.py` or `main.rs`) to save it to a file.
-   **`--output-dir`, `-o`** `PATH`: Required when `--as-modules` is used. Specifies the directory where generated module files will be placed.
-   **`--as-modules`** (Flag): Generate a modular CLI structure.
-   **`--pkg`** `TEXT` (Required): The package/crate name for your CLI.
-   **`--client-pkg`** `TEXT` (Required): The package/crate name of the client library your CLI will use.
-   **`--template`, `-T`** `TEXT`: Path to a custom Jinja2 template.

## Generating a Python CLI (Click)

For simpler APIs or quick demonstrations, you can generate a single Python file containing your entire CLI.

```bash
firestone generate \
  --resources books.yaml \
  --title "Library CLI" \
  --description "Command-line tool for managing library books." \
  --version "0.1.0" \
  --pkg "my_library_cli" \
  --client-pkg "library_client" \
  cli --output my_library_cli.py
```

## Generating a Rust CLI (Clap)

Firestone can generate a high-performance Rust CLI using the `clap` crate.

```bash
firestone generate \
  --resources books.yaml \
  --title "Library CLI" \
  --description "Fast Rust CLI" \
  --version "0.1.0" \
  --pkg "library_cli" \
  --client-pkg "library_client" \
  cli --language rust --output src/main.rs
```

**Prerequisites for Rust:**
1.  You must have a Rust client crate generated (e.g., via `openapi-generator -g rust`).
2.  Your `Cargo.toml` must depend on `clap`, `tokio`, `serde_json`, `log`, `env_logger`, and your generated client crate.

## Modular CLI (`--as-modules`)

For larger APIs, use `--as-modules` to split the code:

```bash
# Python
firestone generate ... cli --as-modules --output-dir library_cli_modules

# Rust
firestone generate ... cli --language rust --as-modules --output-dir src/bin
```


---
## Next Steps

You've successfully generated your first CLI tool. Now, let's look inside that generated code and understand how it's structured.
- **Next:** Dive into the organization of your generated CLI in **[Understanding the Generated CLI Structure](./generated-cli-structure)**.
