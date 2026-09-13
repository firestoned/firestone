//! The middleware the generated router layers on.
//!
//! Both of these are ordinary `axum::middleware::from_fn_with_state` functions
//! rather than hand-written `tower::Service` implementations, which is the short
//! way to add your own: write an async fn taking `Request` and `Next`, and layer
//! it on in `routes.rs`.

use std::collections::HashMap;
use std::net::IpAddr;
use std::net::SocketAddr;
use std::sync::Mutex;
use std::time::Duration;
use std::time::Instant;

use axum::extract::ConnectInfo;
use axum::extract::Request;
use axum::extract::State;
use axum::http::header;
use axum::middleware::Next;
use axum::response::IntoResponse;
use axum::response::Response;

use crate::error::ApiError;
use crate::AppState;

/// Which bearer tokens this service accepts.
///
/// The resource files say *which* operations need authentication, via their
/// `security` block, so the router only wraps those routes. What counts as a valid
/// token is a deployment question, and lives here.
#[derive(Clone, Debug, Default)]
pub struct Auth {
    tokens: Vec<String>,
}

impl Auth {
    /// Accept the given bearer tokens. No tokens means every request is refused,
    /// which is the safe way round for a service that asked for authentication.
    pub fn new(tokens: impl IntoIterator<Item = String>) -> Self {
        Auth {
            tokens: tokens.into_iter().collect(),
        }
    }

    /// Read the accepted tokens from `API_TOKENS`, comma separated.
    pub fn from_env() -> Self {
        let tokens = std::env::var("API_TOKENS").unwrap_or_default();

        Auth::new(
            tokens
                .split(',')
                .map(str::trim)
                .filter(|token| !token.is_empty())
                .map(str::to_string),
        )
    }

    fn accepts(&self, token: &str) -> bool {
        // Compared in full rather than with a short circuit, so a wrong token
        // cannot be narrowed down by timing the response.
        self.tokens
            .iter()
            .fold(false, |found, known| found | constant_time_eq(known, token))
    }
}

fn constant_time_eq(left: &str, right: &str) -> bool {
    if left.len() != right.len() {
        return false;
    }

    left.bytes()
        .zip(right.bytes())
        .fold(0u8, |difference, (a, b)| difference | (a ^ b))
        == 0
}

/// Refuse anything without an acceptable `Authorization: Bearer` header.
///
/// Only wrapped around the operations the resource files marked as secured.
pub async fn require_bearer(
    State(state): State<AppState>,
    request: Request,
    next: Next,
) -> Response {
    let presented = request
        .headers()
        .get(header::AUTHORIZATION)
        .and_then(|value| value.to_str().ok())
        .and_then(|value| value.strip_prefix("Bearer "))
        .map(str::trim);

    match presented {
        Some(token) if state.auth.accepts(token) => next.run(request).await,
        Some(_) => {
            ApiError::Unauthorized("That bearer token is not accepted.".into()).into_response()
        }
        None => {
            ApiError::Unauthorized("This operation needs an Authorization: Bearer header.".into())
                .into_response()
        }
    }
}

/// A fixed window rate limiter, keyed by caller address.
///
/// Small on purpose: it is here to show where a limiter goes and what it needs to
/// return, and is a reasonable default for a single instance. Anything running on
/// more than one replica wants a shared counter instead, at which point this is the
/// shape to write it in.
#[derive(Debug)]
pub struct RateLimit {
    limit: u32,
    window: Duration,
    seen: Mutex<HashMap<IpAddr, (Instant, u32)>>,
}

impl RateLimit {
    /// Allow `limit` requests from one caller per `window`.
    pub fn new(limit: u32, window: Duration) -> Self {
        RateLimit {
            limit,
            window,
            seen: Mutex::new(HashMap::new()),
        }
    }

    /// Read the limit from `RATE_LIMIT` and `RATE_LIMIT_WINDOW_SECS`.
    pub fn from_env() -> Self {
        let limit = std::env::var("RATE_LIMIT")
            .ok()
            .and_then(|value| value.parse().ok())
            .unwrap_or(120);
        let window = std::env::var("RATE_LIMIT_WINDOW_SECS")
            .ok()
            .and_then(|value| value.parse().ok())
            .unwrap_or(60);

        RateLimit::new(limit, Duration::from_secs(window))
    }

    /// Whether this caller may proceed, and how long to wait if not.
    pub fn check(&self, caller: IpAddr) -> Result<(), u64> {
        let mut seen = self.seen.lock().expect("the limiter is not poisoned");
        let now = Instant::now();

        // Callers that have gone quiet are dropped here rather than on a timer, so
        // the map cannot grow without bound.
        seen.retain(|_, (started, _)| now.duration_since(*started) < self.window);

        let (started, count) = seen.entry(caller).or_insert((now, 0));
        if now.duration_since(*started) >= self.window {
            *started = now;
            *count = 0;
        }
        *count += 1;

        if *count > self.limit {
            let elapsed = now.duration_since(*started);
            return Err(self.window.saturating_sub(elapsed).as_secs() + 1);
        }

        Ok(())
    }
}

/// Refuse a caller that has asked too often, with a Retry-After.
pub async fn rate_limit(State(state): State<AppState>, request: Request, next: Next) -> Response {
    // Read rather than extracted, because the extension is absent when the app is
    // driven directly rather than served over a socket, as the generated tests do.
    // Those share one bucket instead of failing.
    let caller = request
        .extensions()
        .get::<ConnectInfo<SocketAddr>>()
        .map(|ConnectInfo(address)| address.ip())
        .unwrap_or(IpAddr::from([0, 0, 0, 0]));

    match state.rate_limit.check(caller) {
        Ok(()) => next.run(request).await,
        Err(retry_after) => ApiError::RateLimited { retry_after }.into_response(),
    }
}
