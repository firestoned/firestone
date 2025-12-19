---
title: "Generating the Python API Reference (pdoc)"
weight: 2
---

# Generating the Python API Reference (pdoc)

The API reference documentation for Python projects in the Firestone ecosystem (like `firestone` and `firestone-lib`) is generated using **[pdoc](https://pdoc.dev/)**. `pdoc` automatically creates clean, modern, and readable documentation from your Python docstrings and type hints.

## Generation Workflow

The `website` project contains a `Makefile` command to automate this process. The command runs `pdoc` on the `firestone` source code and places the output directly into the correct location for the Hugo build system.

### How to Run the Generator

1.  **Navigate to the `website` directory**:
    ```bash
    cd website/
    ```

2.  **Run the `make` command**:
    ```bash
    make prepare-firestone-api
    ```

### What This Command Does

This command executes a script that performs the following steps:
1.  Invokes `pdoc` targeting the `firestone` Python package.
2.  Specifies an output directory: `docs/site/content/api-reference/`.
3.  Tells `pdoc` to output in Markdown format, which is suitable for Hugo.
4.  The generated markdown will likely be a file named `reference.md`, which contains the documentation for all modules in the `firestone` package.

As `CLAUDE.md` notes, this process is optional if `pdoc` is not installed, but it is the standard way to keep the API reference up-to-date.

## Prerequisites

For the generation to work, you must have the necessary tools installed.

-   **Poetry**: The Python projects are managed with Poetry. `pdoc` will be run within the project's Poetry environment to ensure it has access to the source code and all its dependencies.
-   **`pdoc`**: The `pdoc` package must be installed in the relevant Python environment. It is listed as a development dependency in the `firestone` project's `pyproject.toml`. Running `poetry install` in the `firestone/` directory should install it for you.

## Previewing the API Reference

After you run `make prepare-firestone-api`, you can preview the generated documentation by running the Hugo server:

```bash
# Still in the website/ directory
make serve
```

Navigate to `http://localhost:1313` and find the "API Reference" section in the documentation to see the rendered output. This allows you to verify that your docstrings and type hints have been rendered correctly before you commit your changes.
