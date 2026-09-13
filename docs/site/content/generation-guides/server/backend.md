+++
title = "Implementing a Backend"
linkTitle = "Backend"
weight = 2
description = "The one trait the generated server leaves you to write, and how the validation rules reach your storage through it."
+++

## The One Trait

Firestone knows every route, model and rule in your API. It cannot know your storage, and should not guess, so that is the whole of what you write:

```rust
#[async_trait]
pub trait Backend: Send + Sync + 'static {
    async fn list(&self, resource: &str) -> Result<Vec<Value>, Error>;
    async fn get(&self, resource: &str, key: &str) -> Result<Option<Value>, Error>;
    async fn create(&self, resource: &str, body: Value) -> Result<(String, Value), Error>;
    async fn replace(&self, resource: &str, key: &str, body: Value) -> Result<Value, Error>;
    async fn patch(&self, resource: &str, key: &str, body: Value) -> Result<Value, Error>;
    async fn delete(&self, resource: &str, key: &str) -> Result<(), Error>;

    /// Find the first resource whose dotted `path` holds `value`.
    async fn find(&self, resource: &str, path: &str, value: &Value)
        -> Result<Option<Value>, Error>;
}
```

It is deliberately resource-agnostic: `resource` is the `kind` from the schema, so one implementation serves every resource rather than one per kind. Bodies have already been through the generated models by the time they arrive, so a malformed body was refused before your code ran.

`InMemory` is generated alongside the trait and wired into `main.rs`, so the server runs as it is. Swap it out and nothing else in the crate changes:

```rust
let api = Api::new(Arc::new(MyPostgres::new(pool)));
```

## `find` Is What the Rules Use

`find` is the one method that is not plain CRUD. It is how a validation rule reaches your storage:

```yaml
person:
  references:
    kind: persons
    key: first_name
    value: person.first_name
```

becomes `find("persons", "first_name", "Ann")` when an address naming Ann is created. `path` is a **path into the resource**, not a column name — `person.first_name` is a perfectly ordinary rule — so translating it into a query is your job and belongs in one mapping table:

```rust
const LOOKUPS: &[((&str, &str), &str)] = &[
    (("persons", "first_name"), "first_name = $1"),
    (("addressbook", "person.first_name"), "person->>'first_name' = $1"),
];
```

Raise on a pair you have not mapped rather than returning `None`, otherwise a typo in a schema becomes a rule that quietly rejects everything.

## Transactions

The generated handler validates and then writes, and those are two separate calls. A referenced resource can disappear in between, so for anything that matters:

- Build the backend per request around the transaction that performs the write, so the lookups and the mutation see one snapshot.
- Take the locks the check implies, or run `SERIALIZABLE` and retry.
- Keep the foreign keys. Validation turns a constraint violation into a clear 422 naming the rule; it is not the guarantee itself.

## Errors

Return `Error` and the response shape is handled for you:

| Variant | Status |
|---------|--------|
| `NotFound` | 404 |
| `Validation` | whatever the rule asked for, usually 422 |
| `NotImplemented` | 501 |
| `Internal` | 500 |

A 401 is not in that list: the generated server refuses an unauthenticated request
to a secured operation before a handler runs, from the `security` block in the
schema, so it never reaches your backend.

All of them leave as an RFC 9457 problem document served as `application/problem+json`, which is what the generated OpenAPI document declares:

```json
{
  "type": "about:blank",
  "title": "Validation failed",
  "status": 422,
  "detail": "No persons found with first_name 'Ann'.",
  "violations": [
    {
      "rule": "person_must_exist",
      "resource": "addressbook",
      "field": "person.first_name",
      "message": "No persons found with first_name 'Ann'."
    }
  ]
}
```

## Next Steps

- **[Generating a Server](./generating)** - both commands, and adding your own routes
