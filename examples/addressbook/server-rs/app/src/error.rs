//! What a handler can fail with, and how that reaches the caller.
//!
//! The generated server's typed responses only cover what the OpenAPI document
//! declares, so anything else - a resource that is not there, a backend that could
//! not answer - travels as the error type and is rendered by the [`ErrorHandler`]
//! implementation in `lib.rs`.

use axum::http::header;
use axum::http::HeaderValue;
use axum::http::StatusCode;
use axum::response::IntoResponse;
use axum::response::Response;
use serde_json::json;
use serde_json::Value;

/// Anything a handler can fail with.
#[derive(Debug)]
pub enum Error {
    /// No such resource.
    NotFound { resource: String, key: String },
    /// The body did not survive the rules declared in the schema.
    Validation(Value),
    /// An operation firestone did not know how to answer.
    NotImplemented(String),
    /// This service's fault.
    Internal(String),
}

impl Error {
    /// A resource that is not there.
    pub fn not_found(resource: &str, key: &str) -> Self {
        Error::NotFound {
            resource: resource.to_string(),
            key: key.to_string(),
        }
    }

    /// The status this failure asks for.
    pub fn status(&self) -> StatusCode {
        match self {
            Error::NotFound { .. } => StatusCode::NOT_FOUND,
            Error::Validation(problem) => problem
                .get("status")
                .and_then(Value::as_u64)
                .and_then(|status| StatusCode::from_u16(status as u16).ok())
                .unwrap_or(StatusCode::UNPROCESSABLE_ENTITY),
            Error::NotImplemented(_) => StatusCode::NOT_IMPLEMENTED,
            Error::Internal(_) => StatusCode::INTERNAL_SERVER_ERROR,
        }
    }

    /// This failure as an RFC 9457 problem detail.
    pub fn to_problem(&self) -> Value {
        if let Error::Validation(problem) = self {
            return problem.clone();
        }

        let (title, detail) = match self {
            Error::NotFound { resource, key } => {
                ("Not found", format!("No {resource} with key '{key}'."))
            }
            Error::NotImplemented(detail) => ("Not implemented", detail.clone()),
            Error::Internal(detail) => ("Internal server error", detail.clone()),
            Error::Validation(_) => unreachable!("handled above"),
        };

        json!({
            "type": "about:blank",
            "title": title,
            "status": self.status().as_u16(),
            "detail": detail,
        })
    }
}

impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.to_problem())
    }
}

impl std::error::Error for Error {}

impl IntoResponse for Error {
    fn into_response(self) -> Response {
        let status = self.status();
        let body = self.to_problem();
        let content_type = (
            header::CONTENT_TYPE,
            HeaderValue::from_static("application/problem+json"),
        );

        (status, [content_type], axum::Json(body)).into_response()
    }
}

/// Deserialize what the backend returned into whatever the response declares.
pub fn from_json<T: serde::de::DeserializeOwned>(value: Value) -> Result<T, Error> {
    serde_json::from_value(value).map_err(|err| Error::Internal(err.to_string()))
}

/// Serialize a typed request body so the backend and the rules can work with it.
pub fn to_json<T: serde::Serialize>(value: &T) -> Result<Value, Error> {
    serde_json::to_value(value).map_err(|err| Error::Internal(err.to_string()))
}
