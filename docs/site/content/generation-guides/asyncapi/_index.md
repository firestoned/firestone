+++
title = "AsyncAPI Generation"
weight = 30
description = "Learn how firestone helps you design and document event-driven, real-time APIs using AsyncAPI specifications."
+++

# AsyncAPI Generation

## Building Event-Driven APIs

In today's interconnected world, many applications rely on real-time communication, instant notifications, and event-driven architectures. While OpenAPI excels at describing traditional request-response (RESTful) APIs, it doesn't quite fit the model for asynchronous, message-based communication.

This is where **AsyncAPI** comes in.

AsyncAPI is an open-source specification for describing event-driven APIs, much like OpenAPI does for RESTful APIs. It provides a universal language to define message formats, channels (topics), and server interactions for systems using WebSockets, Kafka, AMQP, MQTT, and other asynchronous protocols.

`firestone` understands the power of event-driven architectures. It allows you to extend your resource blueprints to include AsyncAPI definitions, automatically generating compliant specifications that can then be used to create client code, documentation, and tooling for your real-time applications.

## What You'll Learn Here

This section will guide you through how `firestone` supports AsyncAPI generation, from basic concepts to practical implementation.

### 1. [AsyncAPI Basics](./basics)
Start here to understand the fundamental concepts of AsyncAPI and why it's essential for event-driven communication.

### 2. [Generating Your First AsyncAPI Spec](./generating)
Learn the `firestone` commands to produce a compliant AsyncAPI specification from your resource definitions.

### 3. [AsyncAPI Use Cases](./use-cases)
Explore common real-world scenarios where AsyncAPI shines, such as real-time notifications, live dashboards, and chat applications.

### 4. [Understanding the Generated Structure](./spec-structure)
Dive into the key sections of a `firestone`-generated AsyncAPI spec, from servers and channels to message schemas.

### 5. [Advanced AsyncAPI Features](./advanced-features)
Uncover how to fine-tune your AsyncAPI output for complex event-driven designs.

## Next Steps

Ready to build APIs that react in real-time?
- **Next:** Begin your journey with **[AsyncAPI Basics](./basics)**.