---
title: "Generating Streamlit UIs"
linkTitle: "Generating UI"
weight: 2
description: >
  Learn the simple `firestone` commands to transform your resource blueprints into interactive, data-driven Streamlit UIs.
---

## Your API, Visually Managed

You've built robust APIs and CLIs. Now, imagine instantly having an interactive web application that allows you to:

-   Browse your API's resources in a tabular format.
-   Create new resource instances through dynamic forms.
-   Edit existing resources with auto-generated input widgets.
-   Delete resources with a click of a button.
-   Filter and search your data visually.

`firestone` makes this a reality by automatically generating **Streamlit UIs** directly from your resource blueprints. This powerful feature allows for rapid prototyping, instant admin dashboards, and quick data management tools without writing any HTML, CSS, or JavaScript.

## The `firestone generate streamlit` Command

The core command for building your Streamlit UI is `firestone generate streamlit`.

```bash
firestone generate streamlit [OPTIONS]
```

This command takes your resource blueprint(s) and, combining them with your defined methods and schemas, produces a functional Python Streamlit application.

### Core `generate` Options (Required for `streamlit`)

These options provide the high-level metadata for your Streamlit application, appearing in the UI's title and description.

-   **`--resources`, `-r`** `TEXT` (Required): One or more resource files in JSON Schema format (can be JSON or YAML). This tells `firestone` *which* blueprints to use for your UI.
-   **`--title`, `-t`** `TEXT` (Required): The overall title of your Streamlit application.
-   **`--description`, `-d`** `TEXT` (Required): A high-level description for your Streamlit application.
-   **`--version`, `-v`** `TEXT` (Required): The version of your Streamlit application.
-   **`--summary`, `-s`** `TEXT` (Optional): A short summary for your Streamlit application.

### `streamlit` Specific Options

These options allow you to control the output format, API connection, and layout of your generated Streamlit UI.

-   **`--output`, `-O`** `TEXT` (Default: `-` for stdout): Where to save the main generated Streamlit file.
    -   Use `-` to print the Streamlit Python code directly to your console.
    -   Provide a filename (e.g., `my_app.py`) to save it to a single Python file.
-   **`--output-dir`, `-o`** `PATH`: Required when `--as-modules` is used. Specifies the directory where generated Python module files for each resource UI will be placed.
-   **`--as-modules`** (Flag): Generate a modular UI where each resource's management interface is a separate Python module, organized within a specified `--output-dir`. This is ideal for UIs managing multiple resources.
-   **`--backend-url`** `TEXT` (Default: `http://localhost:8000`): The base URL of the API that your Streamlit UI will connect to.
-   **`--col-mappings`, `-C`** `TEXT`: Custom column mapping orders, for example, `{'books': ['title', 'author']}`. This allows you to control which columns appear in the data tables and in what order.
-   **`--template`, `-T`** `TEXT`: Path to a custom Jinja2 template for generating the Streamlit UI. This allows for deep customization.

## Basic Usage: Single-File Streamlit UI

For simpler APIs or quick prototypes, you can generate a single Python file containing your entire Streamlit UI.

Let's assume you have a `books.yaml` resource blueprint and your API is running at `http://localhost:8000`.

```bash
firestone generate \
  --resources books.yaml \
  --title "Library Dashboard" \
  --description "Interactive UI for managing library books." \
  --version "0.1.0" \
  streamlit --output library_dashboard.py --backend-url "http://localhost:8000"
```
This will create a `library_dashboard.py` file.

### Running Your Streamlit App

To run the generated Streamlit app, simply use the `streamlit run` command:
```bash
streamlit run library_dashboard.py
```
This will open your default web browser to display the interactive UI. You can then use it to list, create, edit, and delete books in your API!

## Advanced Usage: Modular UI (`--as-modules`)

For UIs managing multiple resources, generating a single, monolithic Streamlit file can become complex. The `--as-modules` option, combined with `--output-dir`, allows `firestone` to generate a modular UI where each resource management interface gets its own Python module.

```bash
firestone generate \
  --resources books.yaml,authors.yaml \
  --title "Comprehensive Library Dashboard" \
  --description "Modular UI for managing library entities."
  --version "0.1.0" \
  streamlit --as-modules --output-dir library_ui_modules --backend-url "http://localhost:8000"
```

This command will create a directory structure like:
```
library_ui_modules/
├── __init__.py          # Python package initializer
├── main.py              # Main Streamlit app entry point (sidebar navigation)
├── books.py             # Streamlit code for managing 'books'
├── authors.py           # Streamlit code for managing 'authors'
└── api_client.py        # Generated API client setup
```
Each `.py` file corresponds to a resource's UI page, making the generated app organized and easier to extend. You would run `streamlit run library_ui_modules/main.py` to start this modular app.

## Connecting to Your API (`--backend-url`)

The generated Streamlit UI needs to know where your API is running to fetch and update data. You provide this base URL using the `--backend-url` option. This URL should point to your `firestone`-backed API server (which itself might be serving an `openapi-generator`-generated server stub).

## Customizing Your UI (Advanced)

Similar to CLI generation, `firestone` uses Jinja2 templates for Streamlit UI generation. You can provide your own custom template using the `--template` option. This is an advanced feature that allows for deep customization of the generated UI's layout, widgets, and interaction logic.

---
## Next Steps

You've generated your first Streamlit UI! Now, let's explore the powerful features available in these automatically created applications.
- **Next:** Discover the interactive capabilities in **[Exploring Generated UI Features](./ui-features)**.