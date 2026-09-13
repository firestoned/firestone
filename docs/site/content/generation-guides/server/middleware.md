---
title: "Middleware"
linkTitle: "Middleware"
weight: 3
description: >
  The bearer check and rate limiter the generated server comes with, and how to add your own.
---

## What Comes With It

`routes.rs` layers these on, outermost last:

| Layer | What it does |
|-------|--------------|
| `require_bearer` | Only on the routes the schema marked secured |
| `rate_limit` | Every route, so a caller cannot dodge it by picking an open one |
| `TraceLayer` | A span and a log line per request |
| `TimeoutLayer` | 504 after 30s |
| `RequestBodyLimitLayer` | 1MB |

## Bearer Auth Follows the Schema

This is the part worth understanding: **which** routes need a token is not a deployment decision, it is in the resource file already.

```yaml
security:
  scheme:
    bearer_auth:
      scheme: bearer
      type: http
  resource:
    - post
  instance:
    - delete
    - put
```

The generated router puts exactly those operations behind the check and leaves the rest open:

```console
$ curl -s -o /dev/null -w '%{http_code}\n' localhost:8080/persons
200
$ curl -s -o /dev/null -w '%{http_code}\n' -X POST localhost:8080/persons -d '{}'
401
$ curl -s -o /dev/null -w '%{http_code}\n' -X POST localhost:8080/persons \
    -H 'authorization: Bearer s3cret' -H 'content-type: application/json' \
    -d '{"first_name":"Ann"}'
201
```

What counts as a valid token *is* a deployment decision, so it comes from `API_TOKENS`. Tokens are compared in full rather than short-circuiting, so a wrong one cannot be narrowed down by timing the response.

## Rate Limiting

A fixed window per caller, `RATE_LIMIT` requests per `RATE_LIMIT_WINDOW_SECS`, answering 429 with a `Retry-After`:

```console
$ curl -i localhost:8080/addressbook
HTTP/1.1 429 Too Many Requests
retry-after: 50
content-type: application/problem+json

{"detail":"Try again in 50s.","status":429,"title":"Too many requests", ...}
```

Callers that have gone quiet are dropped as the window rolls, so the map cannot grow without bound. It is deliberately small, and per-instance: anything running on more than one replica wants a shared counter, and this is the shape to write it in.

## Adding Your Own

`router(state)` hands back an ordinary [`axum::Router`](https://docs.rs/axum/latest/axum/struct.Router.html), so a middleware of your own is an async function and a `.layer(...)`:

```rust
async fn served_by(request: Request, next: Next) -> Response {
    let mut response = next.run(request).await;
    response
        .headers_mut()
        .insert("x-served-by", HeaderValue::from_static("addressbook"));

    response
}

let app = Router::new()
    .route("/healthz", get(healthz))     // a route the schemas know nothing about
    .merge(router(state))                // everything firestone generated
    .layer(axum::middleware::from_fn(served_by));
```

Put that in your own module rather than in `main.rs`, which regeneration overwrites. `examples/addressbook/server-rs/examples/extend.rs` in the repository is exactly this, runnable:

```console
$ cargo run --example extend
$ curl localhost:8080/healthz
{"status":"ok"}
$ curl -i localhost:8080/addressbook | grep x-served-by
x-served-by: addressbook
```

Use `.route_layer(...)` instead of `.layer(...)` when it should only cover some of the routes, which is how the bearer check covers only the secured ones.

## Next Steps

- **[Validations](../../validations)** - the rules the handlers enforce before the backend is called
