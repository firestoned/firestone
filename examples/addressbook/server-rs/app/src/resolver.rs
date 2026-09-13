//! Connecting the generated validation rules to the backend.
//!
//! The rules say *what* has to exist; the [`Backend`](crate::backend::Backend) is
//! the only thing that knows how to look it up. This is the adapter, and it is
//! generated because both halves are.

use async_trait::async_trait;
use serde_json::Value;

use crate::error::Error;
use crate::validation::validate;
use crate::validation::Error as ValidationFailure;
use crate::validation::RefRequest;
use crate::validation::Request as ValidationRequest;
use crate::validation::Resolved;
use crate::validation::Resolver;
use crate::validation::ResolverError;
use crate::Api;

/// Answers a rule's lookups out of the backend.
pub struct BackendResolver<'a> {
    api: &'a Api,
}

#[async_trait]
impl Resolver for BackendResolver<'_> {
    async fn resolve(
        &mut self,
        requests: &[RefRequest],
        _ctx: &Value,
    ) -> Result<Resolved, ResolverError> {
        let mut resolved = Resolved::new();
        for request in requests {
            // 'key' is a path into the resource being looked up, not a column, so it
            // goes to the backend as one.
            if let Some(found) = self
                .api
                .backend
                .find(&request.kind, &request.key, &request.value)
                .await?
            {
                resolved.insert(request.id(), found);
            }
        }

        Ok(resolved)
    }
}

/// Run every rule that applies to this request.
pub async fn validate_request(
    api: &Api,
    op: &str,
    resource: &str,
    body: Option<&Value>,
    old: Option<&Value>,
) -> Result<(), Error> {
    let mut request = ValidationRequest::new(op, resource);
    if let Some(body) = body {
        request = request.body(body);
    }
    if let Some(old) = old {
        request = request.old(old);
    }

    run(api, request, op, resource).await
}

/// Run the rules against a resource you have already worked out.
///
/// An attribute endpoint changes one field, and the rules are written against the
/// whole resource, so they are handed the resource as it will be rather than being
/// asked to merge a fragment they would not understand.
pub async fn validate_subject(
    api: &Api,
    op: &str,
    resource: &str,
    subject: &Value,
    old: Option<&Value>,
) -> Result<(), Error> {
    let mut request = ValidationRequest::new(op, resource).subject(subject);
    if let Some(old) = old {
        request = request.old(old);
    }

    run(api, request, op, resource).await
}

async fn run(
    api: &Api,
    request: ValidationRequest<'_>,
    op: &str,
    resource: &str,
) -> Result<(), Error> {
    let mut resolver = BackendResolver { api };
    match validate(request, Some(&mut resolver)).await {
        Ok(()) => Ok(()),
        Err(ValidationFailure::Validation(failed)) => {
            tracing::info!(
                resource,
                op,
                "rejected by {} rule(s)",
                failed.violations.len()
            );
            Err(Error::Validation(failed.to_problem()))
        }
        Err(other) => Err(Error::Internal(other.to_string())),
    }
}
