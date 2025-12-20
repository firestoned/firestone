+++
title = "OpenAPI Extensions"
linkTitle = "Extensions"
weight = 50
description = "Adding custom vendor extensions (x-fields) to your Firestone blueprints."
+++

## Customizing Output with Extensions

OpenAPI supports "Vendor Extensions" (fields starting with `x-`) to add custom metadata to your spec. Firestone transparently passes these fields from your resource schema to the generated OpenAPI output.

**Usage:**
Add `x-` fields anywhere in your resource schema (metadata, descriptions, properties).

**Example:**
```yaml
kind: products
apiVersion: v1
metadata:
  x-service-owner: "inventory-team" # Added to OpenAPI 'info' or top-level tags

descriptions:
  resource:
    get:
      x-rate-limit: 100 # Added to the GET operation object
```

**Common Use Cases:**
1.  **Code Generation:** `x-go-name`, `x-java-class`.
2.  **API Gateways:** `x-amazon-apigateway-integration`, `x-kong-plugin`.
3.  **Documentation:** `x-code-samples` (supported by ReDoc).

Firestone ensures your custom metadata survives the generation process intact.
