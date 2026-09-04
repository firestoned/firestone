//! The one piece of validation you write by hand, in rust.
//!
//! Firestone works out *what* every rule needs; this works out *how* to fetch it.
//! Swap the tables below for your database and nothing else about the generated
//! package changes.
//!
//! Run with `cargo run --example resolver`.

use std::collections::HashMap;

use addressbook_validation::validation::{
    validate, Error, RefRequest, Request, Resolved, Resolver, ResolverError,
};
use async_trait::async_trait;
use serde_json::{json, Value};

/// Stands in for the tables a real service would query.
struct InMemory {
    persons: HashMap<&'static str, Value>,
    addressbook: HashMap<&'static str, Value>,
}

impl InMemory {
    fn new() -> Self {
        InMemory {
            persons: HashMap::from([("foo", json!({"first_name": "foo", "uuid": "3fa8-4f66"}))]),
            addressbook: HashMap::from([("foo", json!({"address_key": "bar", "city": "foo"}))]),
        }
    }

    /// A rule's `key` is a path into the resource being looked up, not a column
    /// name, so the mapping from a logical path to a storage predicate lives here,
    /// written out once per backend.
    fn lookup(&self, request: &RefRequest) -> Option<Value> {
        let value = request.value.as_str()?;
        match (request.kind.as_str(), request.key.as_str()) {
            ("persons", "first_name") => self.persons.get(value).cloned(),
            ("addressbook", "person.first_name") => self.addressbook.get(value).cloned(),
            _ => None,
        }
    }
}

#[async_trait]
impl Resolver for InMemory {
    /// Resolve every lookup for one request.
    ///
    /// A real implementation would group by `(kind, key)` and issue one query per
    /// group. `ctx` is where a multi-tenant service would take the tenant from,
    /// rather than trusting the request body.
    async fn resolve(
        &mut self,
        requests: &[RefRequest],
        _ctx: &Value,
    ) -> Result<Resolved, ResolverError> {
        let mut found = Resolved::new();
        for request in requests {
            if let Some(resource) = self.lookup(request) {
                found.insert(request.id(), resource);
            }
        }

        Ok(found)
    }
}

async fn attempt(label: &str, request: Request<'_>, resolver: &mut InMemory) {
    match validate(request, Some(resolver)).await {
        Ok(()) => println!("{label:<22} accepted"),
        // RFC 9457 puts the problem members at the top level of the body, and it is
        // served as application/problem+json. Your framework's error type probably
        // wraps whatever you hand it, so build the response directly.
        Err(Error::Validation(failed)) => println!(
            "{label:<22} {} {}",
            failed.status(),
            serde_json::to_string(&failed.to_problem()).unwrap()
        ),
        Err(other) => println!("{label:<22} 500 {other}"),
    }
}

#[tokio::main(flavor = "current_thread")]
async fn main() {
    let mut resolver = InMemory::new();

    let known = json!({"person": {"first_name": "foo"}, "city": "foo"});
    attempt(
        "known person",
        Request::new("post", "addressbook").body(&known),
        &mut resolver,
    )
    .await;

    let unknown = json!({"person": {"first_name": "nobody"}});
    attempt(
        "unknown person",
        Request::new("post", "addressbook").body(&unknown),
        &mut resolver,
    )
    .await;

    let current = json!({"person": {"first_name": "foo"}, "is_valid": true});
    let flip = json!({"is_valid": false});
    let user = json!({"roles": ["user"]});
    let admin = json!({"roles": ["admin"]});
    attempt(
        "non-admin invalidate",
        Request::new("patch", "addressbook")
            .body(&flip)
            .old(&current)
            .ctx(&user),
        &mut resolver,
    )
    .await;
    attempt(
        "admin invalidate",
        Request::new("patch", "addressbook")
            .body(&flip)
            .old(&current)
            .ctx(&admin),
        &mut resolver,
    )
    .await;

    let in_use = json!({"first_name": "foo"});
    attempt(
        "delete person in use",
        Request::new("delete", "persons").old(&in_use),
        &mut resolver,
    )
    .await;
}
