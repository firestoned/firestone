//! Tests for the implementation firestone generated.
//!
//! Generated from the same OpenAPI document as the handlers, so a template change
//! that compiles but misbehaves fails here rather than in production. The router is
//! driven directly with `oneshot`, so nothing binds a port.

use std::sync::Arc;

use axum::body::Body;
use axum::http::Request;
use axum::http::StatusCode;
use http_body_util::BodyExt;
use serde_json::json;
use serde_json::Value;
use tower::ServiceExt;

use addressbook_server::backend::InMemory;
use addressbook_server::router;
use addressbook_server::Api;

const TOKEN: &str = "test-token";

/// A server with nothing stored and one accepted token.
fn server() -> (axum::Router, Arc<InMemory>) {
    let backend = Arc::new(InMemory::new());

    (
        router(Api::with_tokens(backend.clone(), [TOKEN.to_string()])),
        backend,
    )
}

async fn call(
    app: axum::Router,
    method: &str,
    uri: &str,
    scheme: Option<&str>,
    body: Option<Value>,
) -> (StatusCode, Value) {
    let mut request = Request::builder()
        .method(method)
        .uri(uri)
        // The generated handlers extract Host, so a request without one is
        // rejected before it reaches them.
        .header("host", "localhost");
    if let Some(scheme) = scheme {
        request = request.header("authorization", format!("{scheme} {TOKEN}"));
    }
    let request = match body {
        Some(body) => request
            .header("content-type", "application/json")
            .body(Body::from(body.to_string())),
        None => request.body(Body::empty()),
    }
    .expect("the request builds");

    let response = app.oneshot(request).await.expect("the router answers");
    let status = response.status();
    let bytes = response
        .into_body()
        .collect()
        .await
        .expect("the body reads")
        .to_bytes();

    (
        status,
        serde_json::from_slice(&bytes).unwrap_or(Value::Null),
    )
}

/// A created addressbook comes back carrying the key it was given, and that key works.
///
/// Without it the caller has no way to GET, PUT or DELETE what it just made.
#[tokio::test]
async fn addressbook_create_returns_a_usable_key() {
    let (app, _backend) = server();

    let body: Value =
        serde_json::from_str("{\"addrtype\": \"work\", \"street\": \"x\", \"city\": \"x\", \"state\": \"x\", \"country\": \"x\"}").expect("the sample body parses");
    let (status, created) = call(
        app.clone(),
        "POST",
        "/addressbook",
        Some("Bearer"),
        Some(body),
    )
    .await;
    assert_eq!(status, StatusCode::CREATED, "create answered {created}");

    let key = created
        .get("address_key")
        .and_then(Value::as_str)
        .expect("the created resource carries its key")
        .to_string();

    let (status, _) = call(
        app,
        "GET",
        &format!("/addressbook/{}", key),
        Some("Bearer"),
        None,
    )
    .await;
    assert_eq!(
        status,
        StatusCode::OK,
        "the key a create returned should fetch"
    );
}

/// A created persons comes back carrying the key it was given, and that key works.
///
/// Without it the caller has no way to GET, PUT or DELETE what it just made.
#[tokio::test]
async fn persons_create_returns_a_usable_key() {
    let (app, _backend) = server();

    let body: Value = serde_json::from_str("{}").expect("the sample body parses");
    let (status, created) = call(app.clone(), "POST", "/persons", Some("Bearer"), Some(body)).await;
    assert_eq!(status, StatusCode::CREATED, "create answered {created}");

    let key = created
        .get("uuid")
        .and_then(Value::as_str)
        .expect("the created resource carries its key")
        .to_string();

    let (status, _) = call(
        app,
        "GET",
        &format!("/persons/{}", key),
        Some("Bearer"),
        None,
    )
    .await;
    assert_eq!(
        status,
        StatusCode::OK,
        "the key a create returned should fetch"
    );
}

/// A created postal_codes comes back carrying the key it was given, and that key works.
///
/// Without it the caller has no way to GET, PUT or DELETE what it just made.
#[tokio::test]
async fn postal_codes_create_returns_a_usable_key() {
    let (app, _backend) = server();

    let body: Value = serde_json::from_str("{}").expect("the sample body parses");
    let (status, created) = call(
        app.clone(),
        "POST",
        "/postal_codes",
        Some("Bearer"),
        Some(body),
    )
    .await;
    assert_eq!(status, StatusCode::CREATED, "create answered {created}");

    let key = created
        .get("uuid")
        .and_then(Value::as_str)
        .expect("the created resource carries its key")
        .to_string();

    let (status, _) = call(
        app,
        "GET",
        &format!("/postal_codes/{}", key),
        Some("Bearer"),
        None,
    )
    .await;
    assert_eq!(
        status,
        StatusCode::OK,
        "the key a create returned should fetch"
    );
}

/// A secured operation refuses a request with no credentials.
#[tokio::test]
async fn a_secured_operation_needs_a_token() {
    let (app, _) = server();
    let (status, _) = call(app, "POST", "/persons", None, Some(json!({}))).await;
    assert_eq!(
        status,
        StatusCode::UNAUTHORIZED,
        "POST /persons should need a token"
    );
    let (app, _) = server();
    let (status, _) = call(app, "DELETE", "/persons/test-key", None, Some(json!({}))).await;
    assert_eq!(
        status,
        StatusCode::UNAUTHORIZED,
        "DELETE /persons/test-key should need a token"
    );
    let (app, _) = server();
    let (status, _) = call(app, "PUT", "/persons/test-key", None, Some(json!({}))).await;
    assert_eq!(
        status,
        StatusCode::UNAUTHORIZED,
        "PUT /persons/test-key should need a token"
    );
    let (app, _) = server();
    let (status, _) = call(app, "POST", "/postal_codes", None, Some(json!({}))).await;
    assert_eq!(
        status,
        StatusCode::UNAUTHORIZED,
        "POST /postal_codes should need a token"
    );
    let (app, _) = server();
    let (status, _) = call(
        app,
        "DELETE",
        "/postal_codes/test-key",
        None,
        Some(json!({})),
    )
    .await;
    assert_eq!(
        status,
        StatusCode::UNAUTHORIZED,
        "DELETE /postal_codes/test-key should need a token"
    );
    let (app, _) = server();
    let (status, _) = call(
        app,
        "DELETE",
        "/postal_codes/test-key/name",
        None,
        Some(json!({})),
    )
    .await;
    assert_eq!(
        status,
        StatusCode::UNAUTHORIZED,
        "DELETE /postal_codes/test-key/name should need a token"
    );
}

/// The auth-scheme name is case insensitive, as RFC 7235 has it.
#[tokio::test]
async fn a_lowercase_scheme_is_accepted() {
    let (app, _) = server();
    let (status, _) = call(app, "POST", "/persons", Some("bearer"), Some(json!({}))).await;

    assert_ne!(
        status,
        StatusCode::UNAUTHORIZED,
        "'bearer' is as valid as 'Bearer'"
    );
}

/// A token that is not accepted is refused.
#[tokio::test]
async fn a_wrong_token_is_refused() {
    let (app, _) = server();
    let request = Request::builder()
        .method("POST")
        .uri("/persons")
        .header("host", "localhost")
        .header("authorization", "Bearer not-the-token")
        .header("content-type", "application/json")
        .body(Body::from("{}"))
        .expect("the request builds");
    let status = app.oneshot(request).await.expect("answers").status();

    assert_eq!(status, StatusCode::UNAUTHORIZED);
}
/// A resource that is not there is a 404, served as an RFC 9457 problem document.
#[tokio::test]
async fn a_missing_resource_is_a_problem_document() {
    let (app, _) = server();
    let (status, body) = call(app, "GET", "/addressbook/test-key", None, None).await;

    assert_eq!(status, StatusCode::NOT_FOUND);
    assert_eq!(body["status"], 404);
    assert_eq!(body["title"], "Not found");
}
