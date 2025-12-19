+++
title = "AsyncAPI Spec Structure"
linkTitle = "Spec Structure"
weight = 4
description = "Mapping Firestone resource blueprints to AsyncAPI 2.x components."
+++

## From Blueprint to AsyncAPI

Firestone bridges the gap between RESTful resource definitions and Event-Driven Architectures (EDA) by generating AsyncAPI 2.x specifications from the same `resource.yaml`.

**Mapping Reference:**

| Firestone Field | AsyncAPI Section | Description |
| :--- | :--- | :--- |
| **`asyncapi.servers`** | **`servers`** | Defines your message brokers (Kafka, RabbitMQ) or WebSocket endpoints. |
| **`asyncapi.channels`** | **`channels`** | Determines which channels are generated (`resource`, `instance`, etc.). |
| **`kind`** | **Channel Path** | Used to construct channel names (e.g., `/books`, `/books/{book_id}`). |
| **`schema.items`** | **`components/schemas`** | The payload schema for your messages. |
| **`schema.items`** (implied) | **`components/messages`** | Wraps the schema into a reusable Message object. |

**Key Feature: Channel Generation**
Firestone automatically generates channels based on your configuration:
*   `resources: true` -> Generates collection-level channel (e.g., `user/created`).
*   `instances: true` -> Generates instance-level channel (e.g., `user/{id}/updated`).

For a detailed reference of the target specification format:
*   [**AsyncAPI Specification 2.6.0**](https://www.asyncapi.com/docs/reference/specification/v2.6.0)
*   [**AsyncAPI Concepts**](https://www.asyncapi.com/docs/concepts)
