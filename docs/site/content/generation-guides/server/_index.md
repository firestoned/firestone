+++
title = "Server Generation"
weight = 45
description = "Generate a runnable axum server from your resource definitions, with the rules already enforced."
+++

# Server Generation

## Two Generators, One Document

A resource file already says what the paths are, which methods each exposes, what a body looks like, which operations need authentication and what rules the data has to satisfy. Turning that into a running API takes two steps, and firestone only owns one of them:

1. **`openapi-generator -g rust-axum`** turns the OpenAPI document firestone produces into the server: the router, the typed models, per-operation authentication and request validation. That is not firestone's job to duplicate.
2. **`firestone generate server`** implements the traits that server leaves behind - one required method per operation - wiring each to a `Backend` trait and enforcing the resources' validation rules on the way past.

Both read the same document, so they cannot disagree about an operation id, a model name or a response variant. What is left for you is the `Backend`, which is the one thing neither generator can know.

### 1. [Generating a Server](./generating)
Both commands, the crates they write, and what to run.

### 2. [Implementing a Backend](./backend)
The one trait you write, and how the validation rules reach your storage through it.
