+++
title = "Advanced AsyncAPI Features"
linkTitle = "Advanced Features"
weight = 5
description = "Tuning AsyncAPI generation for complex event architectures."
+++

## Fine-Tuning Event Streams

Firestone's AsyncAPI generation is highly configurable.

**1. Multiple Servers:**
Define development, staging, and production brokers.

```yaml
asyncapi:
  servers:
    dev:
      url: ws://localhost:8080
      protocol: ws
    prod:
      url: wss://api.example.com/events
      protocol: wss
      security:
        - user-password: []
```

**2. Granular Channel Control:**
Reduce noise by enabling only specific event types.

```yaml
asyncapi:
  channels:
    resources: false       # Disable collection events
    instances: true        # Enable item updates
    instance_attrs: false  # Disable field-level updates
```

**3. Security Schemes:**
Firestone reuses the global `securitySchemes` definition for AsyncAPI.

```yaml
securitySchemes:
  user-password:
    type: userPassword
```

**4. Payload Composition:**
Use `oneOf` in `schema.items` to define polymorphic event payloads (e.g., `UserLogin` vs `UserLogout` events on the same channel).
