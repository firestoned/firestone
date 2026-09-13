use async_trait::async_trait;
use axum::extract::*;
use axum_extra::extract::{CookieJar, Host};
use bytes::Bytes;
use http::Method;
use serde::{Deserialize, Serialize};

use crate::{models, types::*};

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum PostalCodesGetResponse {
    /// Response for OK
    Status200_ResponseForOK(Vec<models::PostalCode>),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum PostalCodesPostResponse {
    /// Response for CREATED
    Status201_ResponseForCREATED(models::CreatePostalCode),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum PostalCodesUuidDeleteResponse {
    /// Response for OK
    Status200_ResponseForOK(models::PostalCode),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum PostalCodesUuidGetResponse {
    /// Response for OK
    Status200_ResponseForOK(models::PostalCode),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum PostalCodesUuidHeadResponse {
    /// Default HEAD response
    Status200_DefaultHEADResponse,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum PostalCodesUuidNameDeleteResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum PostalCodesUuidNameGetResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
}

/// PostalCodes
#[async_trait]
#[allow(clippy::ptr_arg)]
pub trait PostalCodes<E: std::fmt::Debug + Send + Sync + 'static = ()>:
    super::ErrorHandler<E>
{
    type Claims;

    /// PostalCodesGet - GET /postal_codes
    async fn postal_codes_get(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        query_params: &models::PostalCodesGetQueryParams,
    ) -> Result<PostalCodesGetResponse, E>;

    /// PostalCodesPost - POST /postal_codes
    async fn postal_codes_post(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        claims: &Self::Claims,
        query_params: &models::PostalCodesPostQueryParams,
        body: &models::CreatePostalCode,
    ) -> Result<PostalCodesPostResponse, E>;

    /// PostalCodesUuidDelete - DELETE /postal_codes/{uuid}
    async fn postal_codes_uuid_delete(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        claims: &Self::Claims,
        path_params: &models::PostalCodesUuidDeletePathParams,
    ) -> Result<PostalCodesUuidDeleteResponse, E>;

    /// PostalCodesUuidGet - GET /postal_codes/{uuid}
    async fn postal_codes_uuid_get(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::PostalCodesUuidGetPathParams,
        query_params: &models::PostalCodesUuidGetQueryParams,
    ) -> Result<PostalCodesUuidGetResponse, E>;

    /// PostalCodesUuidHead - HEAD /postal_codes/{uuid}
    async fn postal_codes_uuid_head(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::PostalCodesUuidHeadPathParams,
    ) -> Result<PostalCodesUuidHeadResponse, E>;

    /// PostalCodesUuidNameDelete - DELETE /postal_codes/{uuid}/name
    async fn postal_codes_uuid_name_delete(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        claims: &Self::Claims,
        path_params: &models::PostalCodesUuidNameDeletePathParams,
    ) -> Result<PostalCodesUuidNameDeleteResponse, E>;

    /// PostalCodesUuidNameGet - GET /postal_codes/{uuid}/name
    async fn postal_codes_uuid_name_get(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::PostalCodesUuidNameGetPathParams,
        query_params: &models::PostalCodesUuidNameGetQueryParams,
    ) -> Result<PostalCodesUuidNameGetResponse, E>;
}
