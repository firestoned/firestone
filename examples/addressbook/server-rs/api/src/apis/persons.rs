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
pub enum PersonsGetResponse {
    /// Response for OK
    Status200_ResponseForOK(Vec<models::Person>),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum PersonsPostResponse {
    /// Response for CREATED
    Status201_ResponseForCREATED(models::CreatePerson),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum PersonsUuidDeleteResponse {
    /// Response for OK
    Status200_ResponseForOK(models::Person),
    /// One or more validation rules failed
    Status409_OneOrMoreValidationRulesFailed(models::ValidationProblem),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum PersonsUuidGetResponse {
    /// Response for OK
    Status200_ResponseForOK(models::Person),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum PersonsUuidHeadResponse {
    /// Default HEAD response
    Status200_DefaultHEADResponse,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum PersonsUuidPutResponse {
    /// Response for OK
    Status200_ResponseForOK(models::UpdatePerson),
}

/// Persons
#[async_trait]
#[allow(clippy::ptr_arg)]
pub trait Persons<E: std::fmt::Debug + Send + Sync + 'static = ()>: super::ErrorHandler<E> {
    type Claims;

    /// PersonsGet - GET /persons
    async fn persons_get(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        query_params: &models::PersonsGetQueryParams,
    ) -> Result<PersonsGetResponse, E>;

    /// PersonsPost - POST /persons
    async fn persons_post(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        claims: &Self::Claims,
        query_params: &models::PersonsPostQueryParams,
        body: &models::CreatePerson,
    ) -> Result<PersonsPostResponse, E>;

    /// PersonsUuidDelete - DELETE /persons/{uuid}
    async fn persons_uuid_delete(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        claims: &Self::Claims,
        path_params: &models::PersonsUuidDeletePathParams,
    ) -> Result<PersonsUuidDeleteResponse, E>;

    /// PersonsUuidGet - GET /persons/{uuid}
    async fn persons_uuid_get(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::PersonsUuidGetPathParams,
        query_params: &models::PersonsUuidGetQueryParams,
    ) -> Result<PersonsUuidGetResponse, E>;

    /// PersonsUuidHead - HEAD /persons/{uuid}
    async fn persons_uuid_head(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::PersonsUuidHeadPathParams,
    ) -> Result<PersonsUuidHeadResponse, E>;

    /// PersonsUuidPut - PUT /persons/{uuid}
    async fn persons_uuid_put(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        claims: &Self::Claims,
        path_params: &models::PersonsUuidPutPathParams,
        body: &models::UpdatePerson,
    ) -> Result<PersonsUuidPutResponse, E>;
}
