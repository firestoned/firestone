+++
title = "How Validations Work"
linkTitle = "How Validations Work"
weight = 1
description = "The two ways to declare a rule, and what happens when one runs."
+++

## The Problem

Take an addressbook API with a `persons` resource and an `addressbook` resource. An address embeds a person, and you only want an address created for somebody already on file. Without firestone that check lives in the POST handler, and again in the PUT handler, and again in PATCH. Multiply by ten resources and a dozen rules each, and the rules exist only in code, are hard to find, and are almost never tested.

The relationship is a property of the schema. It should be declared there.

## Two Layers

### `references` handles the relationships

Most of what gets hand-written is a foreign key:

```yaml
person:
  schema:
    $ref: "person.yaml#/schema"
  references:
    kind: persons
    key: first_name
    value: person.first_name
```

That is a mapping, not logic, and it generates the existence check on POST, PUT and PATCH, an optional immutability check, and the error responses in the OpenAPI document. Reach for this first; at most shops it covers the large majority of the checks.

### `validations.rules` handles the judgement calls

Anything conditional is a [CEL](https://github.com/google/cel-spec) expression over the lookups it declares:

```yaml
validations:
  rules:
    - name: only_admins_may_invalidate
      methods: [put, patch]
      expr: 'self.is_valid == old.is_valid || (has(ctx.roles) && "admin" in ctx.roles)'
      error:
        status: 403
        message: Only an admin may change is_valid on an address.
```

## Why CEL

CEL is Google's Common Expression Language, and it is already the convention for rules embedded in a schema: Kubernetes uses it for CRD `x-kubernetes-validations`, protovalidate uses it for protobuf, Envoy uses it for its policies. It is non-Turing-complete, so an expression is guaranteed to terminate, and there are maintained runtimes in Go, Rust and Python.

The alternatives were considered and rejected: JSON Schema `if`/`then` cannot see other resources and becomes unreadable quickly, JSONLogic's JSON-as-syntax-tree is painful at any real scale, and OPA/Rego is excellent but is a service to deploy and operate rather than a library to import.

## What Happens on a Request

Both layers lower to the same rule structure, so there is one engine, and one code path:

1. **Select.** The rules for this resource that run on this method. Nothing to do? Return immediately.
2. **Plan.** Work out every lookup those rules need. Skip any rule whose lookup value is not in the request, and any existence rule whose reference has not changed.
3. **Resolve.** Hand the whole batch, de-duplicated, to your `Resolver` in one call, along with the request context so lookups can be scoped by tenant or authorisation. A request that trips ten rules costs one round trip, not ten.
4. **Evaluate.** A rule whose required lookup found nothing fails there and then, without evaluating its expression. The rest run against `self`, `old`, `refs` and `ctx`.
5. **Report.** Collect *every* violation, not just the first, and raise a `ValidationError` carrying them.

## The Boundary

This is the part worth understanding, because it is what makes the feature portable:

- **Firestone knows what.** From `kind`, `key` and `value` it can say "this request needs the `persons` whose `first_name` is `Ann`". `key` is a path into the referenced resource, a logical question rather than a storage one.
- **You know how.** Postgres, DynamoDB, an ORM, a Redis cache, another service. Turning `person.first_name` into a column, a JSON expression, a join or an index is your call, and firestone has no opinion about it.

You implement one `Resolver` for your whole API, not one check per endpoint. See [Implementing a Resolver](./resolvers).

## Not a Replacement for a Constraint

A rule runs before your write and is not atomic with it, so a referenced resource can still disappear between the two. Run `validate` inside the mutation's transaction, and keep the foreign keys and unique indexes your database already gives you. Validation turns a constraint violation into a clear 422 naming the rule; it is not the guarantee itself. See [Implementing a Resolver](./resolvers).

## Python and Rust

The rules are extracted once and rendered twice. `--language python` writes a package built around a `Resolver` protocol; `--language rust` writes a module built around a `Resolver` trait. The engine is the same design in both, and the same schema produces the same decisions, statuses and messages under either runtime.

CEL is what makes that possible: `cel-python` and `cel-interpreter` both implement the same specification, so an expression means the same thing on both sides.

## Server Side Only

Validations are generated for the server and nowhere else, in either language. The generated CLIs have no access to your database, so a rule could not be evaluated there without a round trip to the API that is about to evaluate it anyway. Note that `generate cli --language rust` produces a *client*, while `generate validations --language rust` produces something to run inside your server.

## Next Steps

- **[Generating the Package](./generating)** - the command and its output
