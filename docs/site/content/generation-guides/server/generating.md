+++
title = "Generating a Server"
linkTitle = "Generating"
weight = 1
description = "Turn a set of resource files into an axum workspace that compiles, runs and answers."
+++

## The Two Commands

First the server, from the OpenAPI document:

```bash
firestone generate -t 'Addressbook API' -d 'Addressbook API' -v 1.0 \
  -r examples/addressbook/addressbook.yaml,examples/addressbook/person.yaml \
  openapi > openapi.yaml

openapi-generator generate \
  -i openapi.yaml -g rust-axum -o server-rs/api --skip-validate-spec \
  -p packageName=addressbook_api,packageVersion=1.0.0
```

Then the implementation of the traits it declares:

```bash
firestone generate -t 'Addressbook API' -d 'Addressbook API' -v 1.0 \
  -r examples/addressbook/addressbook.yaml,examples/addressbook/person.yaml \
  server --pkg addressbook_server --api-pkg addressbook_api -o server-rs/app
```

| Option | Required | Description |
|--------|----------|-------------|
| `--output-dir`, `-o` | yes | The directory to write the crate to |
| `--pkg` | no | The crate name, `api_server` by default |
| `--api-pkg` | no | The crate name openapi-generator was given, `openapi` by default |
| `--no-validations` | no | Do not enforce the resources' rules in the handlers |
| `--force` | no | Overwrite the scaffolded files too, losing any edits to them |
| `--language`, `-l` | no | `rust`, the default and currently the only choice |

`make gen-server-rust` does both for the addressbook example, and runs `cargo fmt` after, since neither generator formats its output.

## The Workspace

```
server-rs/
├── Cargo.toml          # a workspace over the two halves
├── api/                # openapi-generator: router, models, auth, request validation
└── app/
    ├── Cargo.toml
    └── src/
        ├── main.rs     # config, graceful shutdown
        ├── lib.rs      # the Api struct, the ErrorHandler, router()
        ├── handlers.rs # GENERATED: one method per operation
        ├── backend.rs  # the Backend trait, and an in-memory implementation
        ├── auth.rs     # what counts as an acceptable token
        ├── error.rs    # RFC 9457 problem responses
        ├── resolver.rs # the rules' lookups, answered by the backend
        └── validation/ # the generated validation package
```

## What Firestone Owns

Some files follow the OpenAPI document exactly and are **rewritten every time**:

| Rewritten | Why |
|-----------|-----|
| `src/handlers.rs` | one method per operation |
| `src/lib.rs` | declares the modules, which depend on whether the schema secures anything or carries rules |
| `src/resolver.rs`, `src/validation/` | the rules, and the adapter to your backend |
| `tests/api.rs` | derived from the same operations |

Everything else is **scaffolded once and then yours** - `backend.rs`, `auth.rs`, `main.rs`, `error.rs` and `Cargo.toml` are left alone if they already exist, so the `Backend` you implement and the tokens you accept survive a regeneration. Put your own code in its own module rather than in a rewritten one.

```console
$ firestone generate ... server -o server-rs/app
Wrote 1 file(s) to server-rs/app.
Kept 5 file(s) you own: Cargo.toml, src/backend.rs, src/error.rs, src/lib.rs, src/main.rs.
Pass --force to overwrite them.
```

Regenerate `api/` whenever the spec changes, and `app/` whenever either changes - it is safe to do so.

## What Comes From Where

| In the resource file | Who acts on it |
|----------------------|----------------|
| `methods.*` | openapi-generator: the routes |
| `security` | openapi-generator: a 401 on those operations, from your `ApiAuthBasic` |
| `schema.items.properties` | openapi-generator: the models, and request validation |
| `references`, `validations` | firestone: rules enforced in the handler before the backend is called |

The auth split is worth knowing: **which** operations need a token is in the schema, and the generated server enforces it. **What counts as a valid token** is a deployment question, and lives in the `auth.rs` firestone writes, reading `API_TOKENS`.

## Running It

```console
$ cd server-rs && API_TOKENS=s3cret cargo run -p addressbook_server
INFO Addressbook API v1.0 listening on http://127.0.0.1:8080
```

| Variable | Default | Meaning |
|----------|---------|---------|
| `BIND` | `127.0.0.1:8080` | The address to listen on |
| `API_TOKENS` | none | Comma separated bearer tokens the secured operations accept |
| `RUST_LOG` | `info` | The tracing filter |

With no `API_TOKENS`, a secured operation refuses everything, which is the safe way round for a service that asked for authentication.

## Adding Your Own Routes and Middleware

`router(api)` hands back an ordinary [`axum::Router`](https://docs.rs/axum/latest/axum/struct.Router.html), so everything axum offers is available in `main.rs`:

```rust
let app = router(api)
    .merge(Router::new().route("/healthz", get(healthz)))
    .layer(TraceLayer::new_for_http())
    .layer(your_middleware);
```

Firestone deliberately generates no middleware of its own. Rate limiting, CORS, compression and request ids are all `tower-http` layers, and which you want is a deployment decision rather than something a schema can say.

## Known Gaps

- Firestone writes a handler body only where the mapping is unambiguous. An operation with no request body, a collection `DELETE` or `PATCH`, and a `POST` or `PATCH` on an attribute all answer **501** until you implement them: a POST to an embedded collection appends and a PATCH merges, and neither is a replace.
- Query parameters are parsed and validated by the generated server but not applied; filtering is a storage concern and belongs in your `Backend`.
- `POST` mints a key through the backend. The in-memory one counts; yours will want something better.

## Next Steps

- **[Implementing a Backend](./backend)** - the one trait you write
