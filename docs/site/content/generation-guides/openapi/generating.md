---
title: "Generating OpenAPI Specs"
linkTitle: "Generating Specs"
weight: 2
description: >
  Learn the simple commands to transform your firestone resource blueprints into industry-standard OpenAPI specifications.
---

## Your First API Contract

You've put a lot of thought into designing your API with `firestone` resource blueprints. Now, it's time to generate the universal contract that brings your API to life: the OpenAPI Specification.

The process is straightforward and powerful. `firestone` takes your declarative YAML or JSON resource definitions and automatically produces a comprehensive OpenAPI 3.x document.

## The `firestone generate openapi` Command

The magic happens with the `firestone generate openapi` command.

```bash
firestone generate openapi [OPTIONS]
```

This command takes your resource blueprint(s) and, using the `firestone` CLI's core `generate` options, produces a fully compliant OpenAPI specification.

### Core `generate` Options (Required for `openapi`)

Remember these options from the `firestone` CLI's `generate` command? They provide the high-level metadata for your OpenAPI spec.

-   **`--resources`, `-r`** `TEXT` (Required): One or more resource files in JSON Schema format (can be JSON or YAML). This is where you tell `firestone` *which* blueprints to use.
    ```bash
    firestone generate --resources my_resource.yaml openapi
    ```
-   **`--title`, `-t`** `TEXT` (Required): The overall title of your API, appearing in the OpenAPI `info` section.
    ```bash
    firestone generate --title "My Awesome API" ... openapi
    ```
-   **`--description`, `-d`** `TEXT` (Required): A high-level description of your API, also in the OpenAPI `info` section.
    ```bash
    firestone generate --description "This is my API for awesome stuff." ... openapi
    ```
-   **`--version`, `-v`** `TEXT` (Required): The overall API version, distinct from resource `apiVersion`. This represents the version of your *entire* OpenAPI document.
    ```bash
    firestone generate --version "1.0.0" ... openapi
    ```
-   **`--summary`, `-s`** `TEXT` (Optional): A short summary of your API. If omitted, `description` is used.

### `openapi` Specific Options

Once you've provided the core generation details, you can fine-tune the OpenAPI output with these `openapi`-specific options:

-   **`--output`, `-O`** `TEXT` (Default: `-` for stdout): Where to save the generated specification.
    -   Use `-` to print to your console.
    -   Provide a filename (e.g., `api-spec.yaml`) to save it to a file.
-   **`--ui-server`** (Flag): Launch a local web server to instantly view your generated OpenAPI spec rendered with Swagger UI. Perfect for quick previews!
-   **`--prefix`** `TEXT`: Add a base path prefix to all your API's URLs. This creates a `servers` section in your OpenAPI spec. Useful for deploying behind a gateway.
-   **`--version`** `TEXT` (Default: `3.0.0`): The OpenAPI specification version to use (e.g., `3.0.0`, `3.1.0`).

## Basic Usage: Generating to Console

Let's assume you have a `books.yaml` resource blueprint:
```yaml
# books.yaml
kind: books
apiVersion: v1
# ... rest of your resource definition
```

To generate the OpenAPI spec and print it directly to your terminal:
```bash
firestone generate \
  --resources books.yaml \
  --title "Library API" \
  --description "API for managing books" \
  --version "1.0.0" \
  openapi
```
This will output a large YAML document to your console.

## Saving to a File

To save the output to a file, simply provide a filename with the `--output` option:
```bash
firestone generate \
  --resources books.yaml \
  --title "Library API" \
  --description "API for managing books" \
  --version "1.0.0" \
  openapi --output library_api.yaml
```
You now have a `library_api.yaml` file containing your OpenAPI specification.

## Instant Preview with Swagger UI

The `--ui-server` flag is incredibly useful for quickly visualizing your API.

```bash
firestone generate \
  --resources books.yaml \
  --title "Library API" \
  --description "API for managing books" \
  --version "1.0.0" \
  openapi --ui-server
```
This command will:
1.  Generate the OpenAPI spec internally.
2.  Launch a local web server (usually on `http://localhost:5000` or similar).
3.  Open your default web browser to display the spec rendered in Swagger UI.

This allows you to immediately see how your API contract looks to consumers, test endpoints, and verify descriptions.

## Combining Multiple Resources

`firestone` can generate a single OpenAPI specification from multiple resource blueprints. This is how you build a comprehensive API for your entire application.

Let's say you have `books.yaml` and `authors.yaml`:
```bash
firestone generate \
  --resources books.yaml,authors.yaml \
  --title "Comprehensive Library API" \
  --description "API for managing all library entities" \
  --version "1.0.0" \
  openapi --output library_full_api.yaml
```
The resulting `library_full_api.yaml` will contain definitions for both your `books` and `authors` resources, all combined into a single, cohesive OpenAPI document.

## Setting a Path Prefix

If your API is deployed behind a gateway or needs a specific base path (e.g., all endpoints should start with `/api/v1`), use the `--prefix` option:

```bash
firestone generate \
  --resources books.yaml \
  --title "Library API" \
  --description "API for managing books" \
  --version "1.0.0" \
  openapi --prefix "/api/v1" --output library_api_prefixed.yaml
```
The OpenAPI spec will now include a `servers` section indicating that all paths should be prefixed with `/api/v1`. For example, `GET /books` becomes `GET /api/v1/books`.

---
## Next Steps

You've generated your first OpenAPI spec! Now, let's look inside that document and understand its structure.
- **Next:** Dive into the details of the generated OpenAPI specification in **[OpenAPI Spec Structure](./structure)**.
