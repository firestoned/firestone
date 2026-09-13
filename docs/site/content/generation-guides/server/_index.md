+++
title = "Server Generation"
weight = 45
description = "Generate a runnable axum server from your resource definitions, with the routes, models, middleware and rules already wired in."
+++

# Server Generation

## From Resources to a Running API

A resource file already says what the paths are, which methods each exposes, what a body looks like, which operations need authentication and what rules the data has to satisfy. That is everything an HTTP server needs except one thing: where the data actually lives.

`firestone generate server --language rust` writes the rest — the router, the models, the handlers, the middleware and the RFC 9457 error handling — and leaves you a `Backend` trait for the part it cannot know. An in-memory implementation is generated alongside it, so the server compiles and answers requests before you have written anything.

### 1. [Generating a Server](./generating)
The command, the crate it writes, and what to run.

### 2. [Implementing a Backend](./backend)
The one trait you write, and how the validation rules reach your storage through it.

### 3. [Middleware](./middleware)
The bearer check and rate limiter that come with it, and how to add your own.
