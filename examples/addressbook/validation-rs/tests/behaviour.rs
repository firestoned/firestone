//! Behaviour the generated examples cannot reach.
//!
//! Hand written, unlike `src/validation/tests.rs`. These pin down the parts of the
//! engine's contract that a rule's `examples` block has no way to express: how the
//! HTTP method is normalised, and when a resolver is actually required.

use addressbook_validation::validation::{
    validate, Error, RefRequest, Request, Resolved, Resolver, ResolverError,
};
use async_trait::async_trait;
use serde_json::{json, Value};

/// Answers every lookup, so a test fails for the reason it is about.
struct AlwaysFinds;

#[async_trait]
impl Resolver for AlwaysFinds {
    async fn resolve(
        &mut self,
        requests: &[RefRequest],
        _ctx: &Value,
    ) -> Result<Resolved, ResolverError> {
        Ok(requests
            .iter()
            .map(|request| (request.id(), json!({"found": true})))
            .collect())
    }
}

/// An uppercase method has to pick the rules and build the subject the same way.
///
/// The rule reads `self.is_valid`, which is only there once the body has been
/// merged over `old`. Selecting patch rules without merging leaves the expression
/// reading a field that is not there.
#[tokio::test]
async fn uppercase_patch_still_merges() {
    let body = json!({"city": "Toronto"});
    let old = json!({"is_valid": true, "city": "Ottawa"});
    let ctx = json!({"roles": ["user"]});

    let result = validate(
        Request::new("PATCH", "addressbook")
            .body(&body)
            .old(&old)
            .ctx(&ctx),
        Some(&mut AlwaysFinds),
    )
    .await;

    assert!(
        result.is_ok(),
        "expected the merged subject, got {result:?}"
    );
}

/// An uppercase DELETE has to validate the resource being deleted.
#[tokio::test]
async fn uppercase_delete_uses_old_as_the_subject() {
    let old = json!({"first_name": "foo"});

    let result = validate(
        Request::new("DELETE", "persons").old(&old),
        Some(&mut AlwaysFinds),
    )
    .await;

    match result {
        Err(Error::Validation(failed)) => {
            assert_eq!(failed.violations[0].rule, "person_is_not_in_use");
        }
        other => panic!("expected the delete rule to run, got {other:?}"),
    }
}

/// Lowercase behaves identically, so normalising cannot have changed the default.
#[tokio::test]
async fn lowercase_is_unchanged() {
    let body = json!({"city": "Toronto"});
    let old = json!({"is_valid": true, "city": "Ottawa"});
    let ctx = json!({"roles": ["user"]});

    let result = validate(
        Request::new("patch", "addressbook")
            .body(&body)
            .old(&old)
            .ctx(&ctx),
        Some(&mut AlwaysFinds),
    )
    .await;

    assert!(
        result.is_ok(),
        "expected the merged subject, got {result:?}"
    );
}

/// A rule reading only self, old and ctx needs nothing fetched, so needs no resolver.
#[tokio::test]
async fn rules_without_lookups_need_no_resolver() {
    let body = json!({"is_valid": false});
    let old = json!({"is_valid": true});
    let ctx = json!({"roles": ["user"]});

    let result = validate(
        Request::new("patch", "addressbook")
            .body(&body)
            .old(&old)
            .ctx(&ctx),
        None,
    )
    .await;

    match result {
        Err(Error::Validation(failed)) => {
            assert_eq!(failed.violations[0].rule, "only_admins_may_invalidate");
            assert_eq!(failed.status(), 403);
        }
        other => panic!("expected the rule to run without a resolver, got {other:?}"),
    }
}

/// A rule that does need a lookup says so, rather than quietly passing.
#[tokio::test]
async fn a_planned_lookup_without_a_resolver_is_an_error() {
    let body = json!({"person": {"first_name": "foo"}});

    let result = validate(Request::new("post", "addressbook").body(&body), None).await;

    match result {
        Err(Error::Rule(message)) => assert!(
            message.contains("no resolver was given"),
            "unexpected message: {message}"
        ),
        other => panic!("expected a rule error, got {other:?}"),
    }
}
