---
title: "validations"
linkTitle: "validations"
weight: 52
description: >
  Declare relationships between resources, and the rules that govern them, in the schema instead of in every handler.
---

## Rules That Outgrow JSON Schema

JSON Schema covers the shape of a single request body: this field is a string, that one is required, this one is an enum. It cannot answer the questions that involve the rest of your data:

- Can I create this address, given that it names a person?
- Does this postal code actually belong to the city on the body?
- Is this caller allowed to flip that flag?
- Can I delete this person, or is something still pointing at them?

Those checks normally end up hand-written in every handler, one at a time, and they drift. Firestone lets you declare them in the resource file instead. There are two ways to do it, and most projects need mostly the first.

Both are entirely optional. A resource that declares neither generates exactly what it always did.

## 1. `references`, on a property

Most cross-resource checks are a foreign key. Declare it on the property that holds it:

```yaml
schema:
  items:
    properties:
      person:
        description: The person who lives at this address.
        schema:
          $ref: "person.yaml#/schema"
        references:
          kind: persons
          key: first_name
          value: person.first_name
          on_missing: reject
          immutable: false
```

| Field | Required | Default | Meaning |
|-------|----------|---------|---------|
| `kind` | yes | | The resource being referenced |
| `key` | no | the target's `schema.key.name` | The attribute of the target to match on |
| `value` | no | the property's own name | The dotted path in the request body holding the value to look up |
| `on_missing` | no | `reject` | `reject` to refuse the request, `ignore` to allow a dangling reference |
| `immutable` | no | `false` | Whether the reference can be repointed after creation |
| `description` | no | generated | What this relationship means |

`value` matters when the property is an object rather than a scalar. Above, `person` is an embedded object, so the value to look up lives at `person.first_name`. For a plain `person_id: str` property you would leave `value` out entirely.

A `references` block generates up to two rules for you:

- `<property>_must_exist`, on POST, PUT and PATCH, returning **422** when the target does not exist. Omitted when `on_missing: ignore`.
- `<property>_is_immutable`, on PUT and PATCH, returning **409** when the reference changes. Only when `immutable: true`.

## 2. `validations.rules`, for everything else

Anything conditional goes in a top-level `validations` block. Each rule declares the lookups it needs and a [CEL](https://github.com/google/cel-spec) expression that has to evaluate to true:

```yaml
validations:
  rules:
    - name: postal_code_matches_city
      description: A postal code has to belong to the city it is filed under.
      methods:
        - post
        - put
      refs:
        postal:
          kind: postal_codes
          key: name
          value: postal_code
      expr: refs.postal.city == self.city
      error:
        status: 422
        message: "{self.postal_code} belongs to {refs.postal.city}, not {self.city}."
```

| Field | Required | Default | Meaning |
|-------|----------|---------|---------|
| `name` | yes | | Unique within the resource; violations are reported under it |
| `description` | no | | What this rule enforces, and why |
| `methods` | no | `[post, put, patch]` | Which methods to run on: `post`, `put`, `patch`, `delete` |
| `refs` | no | none | The resources this rule needs, keyed by the name the expression uses |
| `expr` | yes | | A CEL expression that must be true for the request to be accepted |
| `error.status` | no | `422` | The HTTP status to respond with |
| `error.message` | no | generated | The message, with optional `{self.city}` style placeholders |
| `examples` | no | none | Cases the rule must accept or reject, used to [generate tests](../../../generation-guides/validations/testing) |

Each entry under `refs` also takes an optional `optional` flag, `false` by default.

Each entry under `refs` takes a `kind`, an optional `key`, a `value` and an optional `optional`, exactly as `references` does. The name you give it is how the expression refers to it: `postal` above becomes `refs.postal`.

### Lookups are required by default

If a lookup finds nothing, the rule fails with `No postal_codes found with name 'K1A'.` and the rule's status. The expression is not evaluated, so `refs.postal.city` above is safe as written and cannot produce a 500 for a postal code that does not exist.

A rule that is *about* absence needs the opposite, so mark its lookup `optional` and guard the expression with `has()`:

```yaml
    - name: person_is_not_in_use
      methods: [delete]
      refs:
        address:
          kind: addressbook
          key: person.first_name
          value: first_name
          optional: true          # finding nothing is the passing case here
      expr: "!has(refs.address)"
      error:
        status: 409
        message: "{self.first_name} still has an address in the addressbook."
```

An optional lookup that resolves is in `refs`; one that does not is absent, which is what `has()` tests. Reading through an optional lookup without guarding it is the one way to get a `RuleEvaluationError`.

> **`methods`, not `on`.** YAML 1.1 parses a bare `on:` key as the boolean `true`, the same trap that catches people in GitHub Actions workflows. `methods` also matches the vocabulary firestone already uses elsewhere in the schema.

## What an expression can see

| Name | Contents |
|------|----------|
| `self` | The resource as it will be once the request succeeds |
| `old` | The resource as it currently stands, empty on POST |
| `refs` | The resources the resolver found, keyed by the names under `refs` |
| `ctx` | Request scoped context the caller passes in: roles, tenant, trace id |

Two things are worth knowing about `self`:

- On PATCH it is the **merged** state, the current resource with the request body applied over it. Embedded objects are merged, so a body that sets one field of `person` leaves the rest of `person` alone; everything else is replaced outright, lists wholesale and an explicit null as a null. That last point differs from [RFC 7386](https://www.rfc-editor.org/rfc/rfc7386) JSON Merge Patch, which *deletes* a member set to null. If your API implements merge patch properly, or JSON Patch, work the resulting document out yourself and pass it as `subject`. Rules therefore describe what the resource is allowed to become, not what the body happened to contain.
- On DELETE there is no body, so `self` is the resource being deleted.

A rule that reads `old` needs the current resource to be passed alongside the body. See [Implementing a Resolver](../../../generation-guides/validations/resolvers).

CEL is non-Turing-complete, so an expression always terminates. `has()` is the safe way to test for something that may not be there:

```yaml
expr: 'self.is_valid == old.is_valid || (has(ctx.roles) && "admin" in ctx.roles)'
```

## When a rule is skipped

A rule does not run if the value it looks up is not in the request at all, and an existence rule does not run if the reference is unchanged from `old`. A PATCH that only touches `city` therefore costs no lookups, and cannot be refused because of a person somebody else deleted in the meantime.

## Referencing a resource generated elsewhere

`key` defaults to the target resource's `schema.key.name`, which firestone can only work out for a resource it was given. Pass every resource file to one `firestone generate` invocation, or give the reference an explicit `key`. A reference to a kind firestone has not seen, with no `key`, is an error at generation time rather than a lookup that fails at request time.

## Where the rules go

Rules are lowered into a single normalised form and used in two places:

- The OpenAPI document, under `x-firestone-validations`, plus a `422`/`409`/`403` response on each operation a rule covers. The rules' `examples` are build-time test data and are left out.
- The generated validation package, which is what actually runs them. See [Validations Generation](../../../generation-guides/validations).

## Next Steps

- **[How validations work](../../../generation-guides/validations/basics)** - the two layers, and which to reach for
- **[Implementing a Resolver](../../../generation-guides/validations/resolvers)** - the one piece you write yourself
