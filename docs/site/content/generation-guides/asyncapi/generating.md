---
title: "Generating AsyncAPI Specs"
linkTitle: "Generating Specs"
weight: 2
description: >
  Learn the simple commands to transform your firestone resource blueprints into industry-standard AsyncAPI specifications.
---

## Crafting Your Event-Driven Contract

Just as `firestone` empowers you to generate OpenAPI specifications for your request-response APIs, it also provides a straightforward way to produce AsyncAPI specifications for your event-driven APIs. This allows you to define a clear, machine-readable contract for your asynchronous communication.

The process is similar to OpenAPI generation, leveraging your declarative resource blueprints to automatically produce a comprehensive AsyncAPI 2.x document.

## The `firestone generate asyncapi` Command

The core command for this task is `firestone generate asyncapi`.

```bash
firestone generate asyncapi [OPTIONS]
```

This command takes your resource blueprint(s) and, using the `firestone` CLI's core `generate` options, produces a fully compliant AsyncAPI specification.

### Core `generate` Options (Required for `asyncapi`)

These options provide the high-level metadata for your AsyncAPI spec, similar to how they function for OpenAPI.

-   **`--resources`, `-r`** `TEXT` (Required): One or more resource files in JSON Schema format (can be JSON or YAML). This tells `firestone` *which* blueprints to use for generating the AsyncAPI spec.
    ```bash
    firestone generate --resources my_event_resource.yaml asyncapi
    ```
-   **`--title`, `-t`** `TEXT` (Required): The overall title of your event-driven API, appearing in the AsyncAPI `info` section.
    ```bash
    firestone generate --title "My Event Stream" ... asyncapi
    ```
-   **`--description`, `-d`** `TEXT` (Required): A high-level description of your event-driven API, also in the AsyncAPI `info` section.
    ```bash
    firestone generate --description "This API emits events for user activity." ... asyncapi
    ```
-   **`--version`, `-v`** `TEXT` (Required): The overall API version, representing the version of your *entire* AsyncAPI document.
    ```bash
    firestone generate --version "1.0.0" ... asyncapi
    ```
-   **`--summary`, `-s`** `TEXT` (Optional): A short summary of your event-driven API. If omitted, `description` is used.

### `asyncapi` Specific Options

Currently, the `firestone generate asyncapi` command has one specific option:

-   **`--output`, `-O`** `TEXT` (Default: `-` for stdout): Where to save the generated specification.
    -   Use `-` to print the AsyncAPI YAML directly to your console.
    -   Provide a filename (e.g., `event-spec.yaml`) to save it to a file.

## Basic Usage: Generating to Console or File

Let's assume you have an `events.yaml` resource blueprint with an `asyncapi` block defined:

```yaml
# events.yaml
kind: user_events
apiVersion: v1
asyncapi:
  servers:
    dev:
      url: ws://localhost:8080
      protocol: ws
  channels:
    resources: true
    instances: true
# ... rest of your resource definition
```

To generate the AsyncAPI spec and print it directly to your terminal:
```bash
firestone generate \
  --resources events.yaml \
  --title "User Event Stream" \
  --description "Real-time stream of user activity events." \
  --version "1.0.0" \
  asyncapi
```
This will output a large YAML document to your console.

To save the output to a file, simply provide a filename with the `--output` option:
```bash
firestone generate \
  --resources events.yaml \
  --title "User Event Stream" \
  --description "Real-time stream of user activity events." \
  --version "1.0.0" \
  asyncapi --output user_events_asyncapi.yaml
```
You now have a `user_events_asyncapi.yaml` file containing your AsyncAPI specification.

## Combining Multiple Resources

Just like with OpenAPI, `firestone` can generate a single AsyncAPI specification from multiple resource blueprints. This is useful if different services or components contribute to a larger event architecture.

Let's say you have `user_events.yaml` and `product_updates.yaml`:
```bash
firestone generate \
  --resources user_events.yaml,product_updates.yaml \
  --title "Platform Event Bus" \
  --description "Consolidated event stream for user and product activities." \
  --version "1.0.0" \
  asyncapi --output platform_events.yaml
```
The resulting `platform_events.yaml` will contain definitions for both your `user_events` and `product_updates` channels and servers, combined into a single, cohesive AsyncAPI document.

---
## Next Steps

You've successfully generated your first AsyncAPI spec! Now, let's explore some of the powerful ways you can use these event definitions in real-world scenarios.
- **Next:** Discover common applications and patterns in **[AsyncAPI Use Cases](./use-cases)**.
