+++
title = "AsyncAPI Patterns"
linkTitle = "Patterns"
weight = 3
description = "Implementing Event-Driven Architectures with Firestone."
+++

## Event-Driven Patterns with Firestone

Firestone's AsyncAPI generation is designed to support common event-driven architecture (EDA) patterns. By configuring your resource schema, you can define the contract for various communication styles.

**Supported Patterns:**

1.  **Pub/Sub (Publish/Subscribe):**
    *   **Concept:** A resource change (e.g., `OrderCreated`) is published to a topic. Multiple subscribers react to it.
    *   **Firestone Config:** Enable `channels: { resources: true }`. This generates a channel for the collection (e.g., `orders`).
    *   **AsyncAPI Output:** Defines a `publish` operation on the `orders` channel.

2.  **Event Sourcing (State Streaming):**
    *   **Concept:** Streaming the state changes of a specific entity (e.g., `StockPrice` updates).
    *   **Firestone Config:** Enable `channels: { instances: true }`. This generates a channel for specific IDs (e.g., `stocks/{symbol}`).
    *   **AsyncAPI Output:** Defines a `subscribe` operation on the `stocks/{symbol}` channel.

3.  **Attribute-Level Notifications:**
    *   **Concept:** Notifying only when a specific field changes (e.g., `DocumentContent` update).
    *   **Firestone Config:** Enable `channels: { instance_attrs: true }`.
    *   **AsyncAPI Output:** Generates granular channels like `documents/{id}/content`.

For architectural guidance on implementing these patterns in your backend, refer to:

*   [**Event-Driven Architecture (AWS)**](https://aws.amazon.com/event-driven-architecture/)
*   [**Pub/Sub Pattern (Microsoft Azure)**](https://docs.microsoft.com/en-us/azure/architecture/patterns/publisher-subscriber)
*   [**AsyncAPI for EDA (AsyncAPI Blog)**](https://www.asyncapi.com/docs/)

Firestone ensures your event schemas stay strictly synchronized with your resource definitions, preventing "schema drift" between your REST and Async interfaces.
