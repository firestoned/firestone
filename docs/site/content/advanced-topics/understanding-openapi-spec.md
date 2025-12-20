+++
title = "Understanding the Generated OpenAPI Spec"
weight = 2
+++

# Understanding Firestone's Generated OpenAPI Specification

The primary output of the `firestone generate openapi` command is a single `openapi.yaml` (or JSON) file. This file is a standard OpenAPI 3.x specification that describes your entire API, meticulously generated from your Firestone resource blueprints. Understanding its structure is key to integrating with other tools and debugging issues.

## How Firestone Maps Resources to Paths

Firestone translates the `methods` you define in your resource schema into OpenAPI `paths`.

Given this `methods` block in a `users.yaml` schema:

```yaml
methods:
  resource: [get, post]
  instance: [get, put, delete]
```

Firestone generates two primary paths:

1. **The Resource Path**: `/users`
    - `get`: Operation to list all users (corresponds to `methods.resource.get`).
    - `post`: Operation to create a new user (corresponds to `methods.resource.post`).

2. **The Instance Path**: `/users/{user_id}`
    - `get`: Operation to retrieve a single user by its ID (corresponds to `methods.instance.get`).
    - `put`: Operation to update a user (corresponds to `methods.instance.put`).
    - `delete`: Operation to delete a user (corresponds to `methods.instance.delete`).

The name of the path parameter (`user_id` in this case) is taken directly from the `schema.key.name` field in your resource schema.

## How Firestone Maps Schemas to Components

To promote reusability and keep the specification clean, Firestone places all your data models (JSON Schemas) into the `components/schemas` section.

Your resource schema's `items` definition:

```yaml
schema:
  type: array
  items:
    type: object
    properties:
      first_name:
        type: string
      email:
        type: string
        format: email
    required: [first_name, email]
```

Is translated into a reusable component schema, typically named after the resource's `kind`. For a `users` resource, you might find a `User` schema in the components section:

**`openapi.yaml`:**

```yaml
components:
  schemas:
    User:
      type: object
      properties:
        first_name:
          type: string
        email:
          type: string
          format: email
      required: [first_name, email]
```

The operations in the `paths` section will then reference this component using `$ref`:

```yaml
paths:
  /users:
    post:
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      responses:
        '201':
          description: "User created successfully"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
```

## Troubleshooting with the Generated Spec

- **Endpoint Not Appearing?** Check the `methods` section of the corresponding resource schema. Ensure the HTTP verb you're looking for is listed for either the `resource` or `instance`.
- **Incorrect Request/Response Body?** Examine the `schema.items` definition in your resource schema. The structure defined here is what Firestone uses to create the component schema. Check for missing properties or incorrect `type` declarations.
- **Authentication Not Working?** Look at the `securitySchemes` and `security` sections at the top level of the spec, as well as at the individual operations under `paths`. This will tell you exactly how Firestone interpreted your security definitions.
