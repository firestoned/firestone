//! Adding your own routes and middleware to the generated server.
//!
//! Hand written, unlike everything under `src/`. `router(state)` hands back an
//! ordinary `axum::Router`, so anything axum can do you can do to it here, and
//! regenerating the crate will not touch this file.
//!
//! Run with `cargo run --example extend`, then:
//!
//!   curl localhost:8080/healthz
//!   curl -i localhost:8080/addressbook          # note the x-served-by header
//!
//! See <https://docs.rs/axum/latest/axum/> for what else a Router takes.

use std::net::SocketAddr;
use std::sync::Arc;
use std::time::Duration;

use addressbook_server::backend::InMemory;
use addressbook_server::middleware::Auth;
use addressbook_server::middleware::RateLimit;
use addressbook_server::router;
use addressbook_server::AppState;
use axum::extract::Request;
use axum::http::HeaderValue;
use axum::middleware::Next;
use axum::response::Response;
use axum::routing::get;
use axum::Json;
use axum::Router;
use serde_json::json;
use serde_json::Value;
use tokio::net::TcpListener;

/// A route the resource schemas know nothing about.
async fn healthz() -> Json<Value> {
    Json(json!({"status": "ok"}))
}

/// A middleware of your own: three lines, and it wraps every generated route.
async fn served_by(request: Request, next: Next) -> Response {
    let mut response = next.run(request).await;
    response
        .headers_mut()
        .insert("x-served-by", HeaderValue::from_static("addressbook"));

    response
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Seed the in-memory backend, so the validation rules have something to find.
    let backend = InMemory::new();
    backend.seed(
        "persons",
        "ann",
        json!({"first_name": "Ann", "last_name": "B"}),
    );

    let mut state = AppState::new(Arc::new(backend));
    state.auth = Arc::new(Auth::new(["s3cret".to_string()]));
    state.rate_limit = Arc::new(RateLimit::new(1_000, Duration::from_secs(60)));

    // The generated router, with your own on top.
    let app = Router::new()
        .route("/healthz", get(healthz))
        .merge(router(state))
        .layer(axum::middleware::from_fn(served_by));

    let listener = TcpListener::bind("127.0.0.1:8080").await?;
    println!("listening on http://127.0.0.1:8080 (try /healthz)");
    axum::serve(
        listener,
        app.into_make_service_with_connect_info::<SocketAddr>(),
    )
    .await?;

    Ok(())
}
