---
title: "Generating a Server"
linkTitle: "Generating"
weight: 1
description: >
  Turn a set of resource files into an axum crate that compiles, runs and answers.
---

## The Command

```bash
firestone generate \
  --title 'Example person and addressbook API' \
  --description 'Example person and addressbook API' \
  --resources examples/addressbook/addressbook.yaml,examples/addressbook/person.yaml \
  --version 1.0 \
  server \
  --pkg addressbook_server \
  --output-dir addressbook/server-rs
```

| Option | Required | Description |
|--------|----------|-------------|
| `--output-dir`, `-o` | yes | The directory to write the crate to; created if missing |
| `--pkg` | no | The crate name, `api_server` by default |
| `--no-validations` | no | Do not wire the resources' rules into the handlers |
| `--language`, `-l` | no | `rust`, the default and currently the only choice |

Then:

```bash
cd addressbook/server-rs
cargo fmt        # the generator does not format; see below
cargo run
```

## Formatting

The generator does not run rustfmt: how a line wraps depends on how long your resource names are, so a template cannot be written that is stable under it. `make gen-server-rust` therefore runs `cargo fmt` straight after generating, and `make verify-rust` checks with `cargo fmt --check` that the committed crate was formatted, so a regeneration that skipped it fails rather than landing.

## What Gets Written

```
addressbook/server-rs/
├── Cargo.toml
├── src/
│   ├── main.rs        # config, graceful shutdown
│   ├── lib.rs         # AppState, and the router() everything hangs off
│   ├── routes.rs      # GENERATED from methods and security
│   ├── handlers.rs    # GENERATED: extract, validate, hand off to the backend
│   ├── models.rs      # GENERATED from the resource schemas
│   ├── backend.rs     # the Backend trait, and an in-memory implementation
│   ├── middleware.rs  # bearer auth, rate limiting
│   ├── error.rs       # RFC 9457 problem responses
│   ├── resolver.rs    # the rules' lookups, answered by the backend
│   └── validation/    # the generated validation package
└── tests/
    └── routes.rs      # GENERATED smoke tests for every route
```

`routes.rs`, `handlers.rs`, `models.rs` and `tests/routes.rs` are regenerated whenever the schemas change - do not edit them. Everything else is generated once and then yours, though a fresh generation will overwrite it, so put your own code in its own module.

## What It Does With the Schema

| In the resource file | In the generated server |
|----------------------|--------------------------|
| `kind`, `plural`, `versionInPath` | the path the routes are mounted on |
| `methods.resource` / `methods.instance` | which routes exist at all |
| `security` | which routes the bearer check wraps |
| `schema.items.properties` | the request and response models |
| `schema.key` | the path parameter |
| `query_params`, `default_query_params` | a typed query struct per resource |
| `references`, `validations` | rules enforced in the handler before the backend is called |

A property firestone cannot name exactly - an embedded resource, or a free form object - is carried as `serde_json::Value` rather than guessed at.

## Running It

```console
$ RATE_LIMIT=5 API_TOKENS=s3cret cargo run
INFO Example person and addressbook API v1.0 listening on http://127.0.0.1:8080
```

| Variable | Default | Meaning |
|----------|---------|---------|
| `BIND` | `127.0.0.1:8080` | The address to listen on |
| `API_TOKENS` | none | Comma separated bearer tokens the secured routes accept |
| `RATE_LIMIT` | `120` | Requests allowed per caller per window |
| `RATE_LIMIT_WINDOW_SECS` | `60` | The window |
| `RUST_LOG` | `info` | The tracing filter |

With no `API_TOKENS`, a secured route refuses everything, which is the safe way round for a service that asked for authentication.

## Generated Tests

`tests/routes.rs` comes from the same resource files as the router, so a route that stops being reachable, or one that should have been secured and is not, fails there:

```console
$ cargo test
test addressbook_collection_is_reachable ... ok
test addressbook_attribute_is_routed ... ok
test addressbook_head_is_answered_on_an_attribute ... ok
test persons_delete_instance_needs_a_token ... ok
test addressbook_instance_is_not_found_when_absent ... ok
```

The app is driven directly rather than over a socket, so nothing binds a port.

## Route Coverage

Everything the OpenAPI document describes is routed:

| In the schema | Route |
|---------------|-------|
| `methods.resource` | `/addressbook` |
| `methods.instance` | `/addressbook/{address_key}` |
| `methods.instance_attrs` | `/addressbook/{address_key}/{attr}` |

Attribute endpoints are one parameterised route per resource rather than one per property, with the exposed attribute names generated into an allowlist, so an attribute the schema hides with `expose: false` - or one a caller invented - is a 404.

`HEAD` needs no route of its own: axum answers it wherever `GET` is routed.

An attribute `PUT` or `DELETE` changes one field of a resource, but the rules are written against the whole resource, so the handler works out the resource as it will be and hands that to `validate` as its `subject`. A rule about the whole address is therefore enforced when you change one field of it:

```console
$ curl -X PUT localhost:8080/addressbook/addressbook-0/person \
    -H 'content-type: application/json' -d '{"first_name":"Nobody"}'
{"title":"Validation failed","status":422,
 "detail":"No persons found with first_name 'Nobody'.", ...}
```

## Limitations

- The generated query structs are parsed but not applied; filtering is a storage concern and belongs in your `Backend`.
- `POST` mints a key through the backend and returns it in a `Location` header. The in-memory one counts; yours will want something better.
- An attribute `DELETE` is validated as an update, since removing a field changes the resource.

## Next Steps

- **[Implementing a Backend](./backend)** - the one trait you write
