+++
title = "AsyncAPI Basics"
linkTitle = "AsyncAPI Basics"
weight = 1
description = "How firestone generates AsyncAPI specs for event-driven and real-time communication."
+++

## From Resource to WebSocket Spec - Automatically

AsyncAPI is the standard for describing event-driven APIs ([learn more](https://www.asyncapi.com/)). Where OpenAPI describes REST, AsyncAPI describes WebSockets, message queues, and real-time streams.

Here's the beautiful part: **the same resource definition that generates your OpenAPI spec also generates AsyncAPI**. Define it once, get both.

## How Firestone Generates AsyncAPI

Add an `asyncapi` block to your resource definition:

```yaml
kind: book
schema:
  type: array
  key:
    name: book_id
  items:
    type: object
    properties:
      title:
        type: string
      author:
        type: string

# Add this to enable AsyncAPI generation
asyncapi:
  servers:
    dev:
      url: ws://localhost:8080
      protocol: ws
  channels:
    resources: true  # Creates /books channel
    instances: true  # Creates /books/{book_id} channel
```

From this, firestone generates:
- **WebSocket channels** - `/books` for collection updates, `/books/{book_id}` for instance updates
- **Message schemas** - Subscribe and publish operations with proper payloads
- **Server configurations** - Connection details for your WebSocket server

**Your resource's JSON Schema becomes the message payload**. Add a field to your resource, and both REST and WebSocket specs update automatically.

> 💡 **One Definition, Four Outputs**
> This same resource definition also generates [OpenAPI](../openapi/) (REST specs), [CLI](../cli/) (command-line tools), and [Streamlit UI](../streamlit/) (web dashboards).

## Real-Time Use Cases

AsyncAPI specs from firestone are perfect for:
- **Live dashboards** - Subscribe to resource updates, display changes in real-time
- **Collaborative editing** - Multiple users editing, everyone sees changes
- **Notifications** - Server pushes updates when resources change
- **Event streams** - Audit logs, activity feeds, monitoring

## What You Can Do With the Generated AsyncAPI Spec

Once firestone generates your AsyncAPI spec:
- **Generate WebSocket clients** - Use AsyncAPI code generators
- **Document event flows** - AsyncAPI HTML templates create interactive docs
- **Validate messages** - Ensure WebSocket payloads match the contract
- **Design event architecture** - Use the spec as the source of truth for async communication

The power is in the consistency: your REST API and WebSocket API describe the same resource structure. Change it once, both update.

---
## Next Steps

Ready to generate your first AsyncAPI spec?
- **Next:** Learn the commands in **[Generating AsyncAPI Specs](./generating)**.
