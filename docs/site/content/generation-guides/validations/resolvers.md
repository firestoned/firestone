---
title: "Implementing a Resolver"
linkTitle: "Resolvers"
weight: 3
description: >
  Connect the generated rules to your own database, cache or service, and return the failures to the caller.
---

## The One Interface

Firestone cannot fetch your data, and should not try: every consumer has a different database. What it can do is work out exactly what each request needs, hand you the list, and let you answer it.

That interface, in `ports.py` or `ports.rs`, is the whole contract:

```python
@dataclasses.dataclass(frozen=True)
class RefRequest:
    kind: str      # the resource to look up, e.g. "persons"
    key: str       # the attribute to match on, e.g. "first_name"
    value: Any     # the value to match, taken from the request body

    @property
    def id(self) -> str: ...


class Resolver(typing.Protocol):
    def resolve(self, requests: Sequence[RefRequest], ctx: Mapping[str, Any]) -> Resolved:
        """Return a mapping of RefRequest.id to the resource found.

        Omit the entry, or map it to None, for anything that does not exist.
        """
```

In rust it is the same contract as a trait:

```rust
#[derive(Clone, Debug, PartialEq)]
pub struct RefRequest {
    pub kind: String,   // the resource to look up, e.g. "persons"
    pub key: String,    // the path into it to match on, e.g. "first_name"
    pub value: Value,   // the value to match, taken from the request body
}

#[async_trait]
pub trait Resolver: Send {
    async fn resolve(
        &mut self,
        requests: &[RefRequest],
        ctx: &Value,
    ) -> Result<Resolved, ResolverError>;
}
```

`&mut self` is deliberate. Validation has to read through the same transaction as the mutation it guards, and a transaction is normally held mutably, so building the resolver per request and passing it mutably is the straightforward path:

```rust
let mut tx = pool.begin().await?;
let mut resolver = TxResolver { tx: &mut tx };

validate(Request::new("post", "addressbook").body(&body), Some(&mut resolver)).await?;
drop(resolver);

// ... the insert, on the same tx, which the lookups above already read through
tx.commit().await?;
```

Taking `&self` would have forced anyone following that advice into an async mutex just to hold the transaction, which is exactly the locking the trait should not impose. An implementation needing no mutation simply ignores it.

You write one of these for your whole API, not one check per endpoint.

In python, `resolve` may be a coroutine or a plain function; the engine awaits it only if it needs to.

### A Resolver Is Only Needed for Lookups

Rules that read nothing but `self`, `old` and `ctx` - an authorisation check, a state transition - fetch nothing, so they need no resolver. Python takes `resolver=None`, rust takes `Option<&mut dyn Resolver>`, and both raise only once a lookup has actually been planned:

```rust
// no lookups on this path, so nothing to resolve
validate(Request::new("patch", "addressbook").body(&body).old(&old).ctx(&ctx), None).await?;
```

## `kind` and `key` Are Logical, Not Storage

This is the thing to get right before writing any of it.

`kind` is a resource kind from your schema, and `key` is a **path into that resource**, not a column name. The addressbook example declares:

```yaml
refs:
  address:
    kind: addressbook
    key: person.first_name
    value: first_name
```

which means *"the addressbook entry whose person's first_name is this"*. There is no portable storage predicate for that. In Postgres with a JSONB column it is `person->>'first_name'`, in a normalised schema it is a join, in Mongo it is the dotted field `person.first_name`, in Redis it is whatever secondary index you built.

So do not interpolate `key` into a query. Map each `(kind, key)` pair to a predicate your backend understands, once, in a table you can read:

```python
LOOKUPS = {
    ("persons", "first_name"): ("persons", "first_name = ANY($1)"),
    ("persons", "uuid"): ("persons", "uuid = ANY($1)"),
    ("addressbook", "person.first_name"): ("addressbook", "person->>'first_name' = ANY($1)"),
}
```

A pair with no entry is a rule you have not implemented yet. Raise on it rather than silently returning nothing, otherwise a typo in a schema becomes a rule that quietly rejects every request.

## A Real One

The requests arrive already de-duplicated and batched, which is the point: group them by `(kind, key)` and issue one query per group, so a request that trips ten rules still costs one round trip rather than ten.

```python
import collections


class PostgresResolver:
    def __init__(self, conn):
        self.conn = conn

    async def resolve(self, requests, ctx):
        by_lookup = collections.defaultdict(list)
        for request in requests:
            by_lookup[(request.kind, request.key)].append(request)

        found = {}
        for lookup, group in by_lookup.items():
            if lookup not in LOOKUPS:
                raise NotImplementedError(f"No lookup defined for {lookup}")

            table, predicate = LOOKUPS[lookup]
            values = [request.value for request in group]
            rows = await self.conn.fetch(
                f"SELECT * FROM {table} WHERE {predicate} AND tenant = $2",
                values,
                ctx["tenant"],
            )

            by_value = {self.key_of(row, lookup[1]): dict(row) for row in rows}
            for request in group:
                if request.value in by_value:
                    found[request.id] = by_value[request.value]

        return found
```

`table` and `predicate` come from your own `LOOKUPS` table rather than from a request, so interpolating them is safe; the *values* are always parameters.

A caching resolver is just a resolver that checks Redis first and falls through to this one.

### The Same Thing in Rust

```rust
use async_trait::async_trait;
use serde_json::Value;

pub struct PostgresResolver {
    pool: sqlx::PgPool,
}

#[async_trait]
impl Resolver for PostgresResolver {
    async fn resolve(
        &mut self,
        requests: &[RefRequest],
        ctx: &Value,
    ) -> Result<Resolved, ResolverError> {
        let mut by_lookup: HashMap<(&str, &str), Vec<&RefRequest>> = HashMap::new();
        for request in requests {
            by_lookup
                .entry((request.kind.as_str(), request.key.as_str()))
                .or_default()
                .push(request);
        }

        let mut found = Resolved::new();
        for (lookup, group) in by_lookup {
            let (table, predicate) = LOOKUPS
                .get(&lookup)
                .ok_or_else(|| format!("No lookup defined for {lookup:?}"))?;

            let values: Vec<&Value> = group.iter().map(|request| &request.value).collect();
            let rows = sqlx::query(&format!("SELECT * FROM {table} WHERE {predicate}"))
                .bind(&values)
                .fetch_all(&self.pool)
                .await?;

            // ... match each row back to the request whose value it answers
        }

        Ok(found)
    }
}
```

The database pool lives on the struct, exactly as the python session does, because it is not serialisable and so cannot travel in `ctx`. `ResolverError` is `Box<dyn Error + Send + Sync>`, so `?` on a `sqlx::Error` works and the engine reports it as `Error::Resolver` rather than as a rejected body.

`examples/addressbook/validation-rs` in the repository has a complete, runnable one: `cargo run --example resolver`.

## The Context

`ctx` is the same mapping you pass to `validate`, handed over read-only. It is where anything a lookup has to be **scoped** by belongs: the tenant, the caller's authorisation scope, a read-consistency preference, a trace id. Scoping from `ctx` rather than from the request body is what stops one tenant satisfying a reference with another tenant's data.

Rules can read `ctx` too, so it has to be JSON serialisable. A database session, a connection pool or an open transaction is not: bind those to the resolver instance instead, which is the usual per-request dependency anyway.

```python
resolver = PostgresResolver(conn=session)          # not serialisable, so it goes here
await validate("post", "addressbook", body,
               resolver=resolver,
               ctx={"tenant": tenant_id, "roles": roles})   # serialisable, so it goes here
```

## Calling It

```python
from addressbook.validation import ValidationError, validate

await validate("post", "addressbook", body, resolver=resolver)
```

| Argument | Meaning |
|----------|---------|
| `op` | The HTTP method, lowercase |
| `resource` | The resource `kind`, as written in the schema |
| `body` | The request body: a dict, or a pydantic model, which is unpacked for you |
| `old` | The resource as it currently stands |
| `resolver` | Your resolver |
| `ctx` | Request scoped context: the caller's roles, the tenant, a trace id. Read by the rules, and handed to the resolver, so it must be JSON serialisable |
| `subject` | The resource as it will be, when you would rather work that out than have `body` merged over `old` |

The method is normalised, so `"PATCH"` and `"patch"` pick the same rules *and* build the subject the same way.

`old` is required by any rule that reads it, which means most PUT, PATCH and DELETE rules:

- **PATCH** merges the body over `old`, so rules see the state the resource will end up in. Embedded objects are merged; lists and nulls are replaced outright. If that is not your API's update semantics, pass `subject` instead.
- **DELETE** has no body at all, so `old` *is* the subject: pass the resource being deleted.

## Returning the Failure

A failed request raises `ValidationError`, carrying every violation rather than just the first, and `to_problem()` renders the RFC 9457 document the OpenAPI spec advertises. Register a handler once and every route is covered:

```python
from fastapi.responses import JSONResponse


@app.exception_handler(ValidationError)
async def on_validation_error(request, exc):
    return JSONResponse(
        status_code=exc.status,
        content=exc.to_problem(),
        media_type="application/problem+json",
    )
```

Per-handler works too, as long as you **return** the response rather than raising `HTTPException`:

```python
try:
    await validate("post", "addressbook", body, resolver=resolver)
except ValidationError as exc:
    return problem_response(exc)
```

> `HTTPException` is the wrong tool here. FastAPI serialises it as `application/json` with your payload nested under a `detail` key, which is neither the media type nor the body shape the generated spec declares. RFC 9457 puts the problem members at the top level of the document.

The status is the highest of any violation's, so a request that trips both a 403 rule and a 422 rule is answered 422 with both reported:

```json
{
  "type": "about:blank",
  "title": "Validation failed",
  "status": 422,
  "detail": "No persons found with first_name 'Bob'.",
  "violations": [
    {
      "rule": "person_must_exist",
      "resource": "addressbook",
      "field": "person.first_name",
      "message": "No persons found with first_name 'Bob'."
    }
  ]
}
```

## Validation Is Not a Constraint

Everything here checks state *before* your handler writes. Nothing about that is atomic on its own, and the generated package cannot make it so:

- An address passes `person_must_exist`, and the person is deleted before the insert commits. You now have a dangling reference.
- A person passes `person_is_not_in_use`, and an address naming them is created before the delete commits. Same problem, from the other side.

So treat `validate` as part of the write, not as a step before it:

- **Run it inside the transaction that performs the mutation**, and make the resolver read through that same session, so the two see one consistent snapshot. Passing the session to the resolver, rather than putting it in `ctx`, is what makes this natural.
- **Take the locks the check implies.** Under Postgres read-committed, `SELECT ... FOR SHARE` on the referenced row holds it against deletion for the rest of the transaction. `SERIALIZABLE` gets you the same guarantee at the cost of retries.
- **Keep the database constraints.** Where the backend can express the rule - a foreign key, a unique index, a check constraint - it should, because that is the only place the guarantee actually holds. Validation exists to turn a constraint violation into a clear 422 naming the rule and the field, not to replace the constraint.
- **On a backend without constraints**, Mongo or Redis, the check and the write need a transaction or a compare-and-set. If neither is available, the race is real and needs designing around; a rule in a schema does not remove it.

The same applies to `references`. A generated existence rule is a better error message for a foreign key, not a substitute for one.

## Returning the Failure in Rust

`validate` returns `Result<(), Error>`, and the three variants are the three different things that can go wrong:

```rust
match validate(Request::new("post", "addressbook").body(&body), Some(&mut resolver)).await {
    Ok(()) => {}
    // Rules rejected the request: answer with the problem document.
    Err(Error::Validation(failed)) => {
        return (
            StatusCode::from_u16(failed.status()).unwrap(),
            [(header::CONTENT_TYPE, "application/problem+json")],
            Json(failed.to_problem()),
        )
            .into_response();
    }
    // A broken rule, or a resolver that could not answer: neither is the caller's fault.
    Err(other) => return internal_error(other),
}
```

Splitting them at the type level is the point: `Error::Validation` is a request to refuse, and the other two are failures on your side that must not be reported as a bad body.

## When a Rule Cannot Run

`RuleEvaluationError` means a rule could not be evaluated at all - a broken expression, a body that is not a mapping, a lookup with no resolver passed. That is a bug on your side, not a rejected request, and should surface as a 500. It is deliberately a different exception from `ValidationError` so you cannot report one as the other.

## Attribute Endpoints

Firestone can generate routes that update a single attribute, like `PUT /addressbook/{address_key}/person`. Those advertise the same validation responses as the whole-resource routes, because changing one attribute can break a rule about the resource just as easily.

The rules are written against the whole resource, though: `self` is an address, not a person. So the body of an attribute request is not something you can validate directly. Work out the resource as it will be, and pass it as `subject`:

```python
@router.put("/addressbook/{address_key}/person")
async def put_person(address_key: str, person: Person):
    current = await store.get(address_key)
    updated = {**current, "person": person.model_dump()}

    try:
        await validate("put", "addressbook", old=current, subject=updated, resolver=resolver)
    except ValidationError as exc:
        return problem_response(exc)

    await store.put(address_key, updated)
```

`subject` says "this is the resource as it will end up", and skips the merge entirely. It is the same escape hatch to reach for when your PATCH semantics are not a plain merge - true JSON Merge Patch with null deletion, or JSON Patch operations.

## A Working Example

`examples/addressbook/addressbook/impl/resolver.py` in the repository has a complete, runnable resolver and the FastAPI wiring for it.

## Next Steps

- **[Testing Your Rules](./testing)** - proving the rules do what you meant
