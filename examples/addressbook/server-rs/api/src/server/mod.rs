use std::collections::HashMap;

use axum::{body::Body, extract::*, response::Response, routing::*};
use axum_extra::extract::{CookieJar, Host, Query as QueryExtra};
use bytes::Bytes;
use http::{HeaderMap, HeaderName, HeaderValue, Method, StatusCode, header::CONTENT_TYPE};
use tracing::error;
use validator::{Validate, ValidationErrors};

use crate::{header, types::*};

#[allow(unused_imports)]
use crate::{apis, models};

#[allow(unused_imports)]
use crate::{
    models::check_xss_map, models::check_xss_map_nested, models::check_xss_map_string,
    models::check_xss_string, models::check_xss_vec_string,
};

/// Setup API Server.
pub fn new<I, A, E, C>(api_impl: I) -> Router
where
    I: AsRef<A> + Clone + Send + Sync + 'static,
    A: apis::addressbook::Addressbook<E>
        + apis::persons::Persons<E, Claims = C>
        + apis::postal_codes::PostalCodes<E, Claims = C>
        + apis::ApiAuthBasic<Claims = C>
        + Send
        + Sync
        + 'static,
    E: std::fmt::Debug + Send + Sync + 'static,
    C: Send + Sync + 'static,
{
    // build our application with a route
    Router::new()
        .route(
            "/addressbook",
            get(addressbook_get::<I, A, E>).post(addressbook_post::<I, A, E>),
        )
        .route(
            "/addressbook/{address_key}",
            delete(addressbook_address_key_delete::<I, A, E>)
                .get(addressbook_address_key_get::<I, A, E>)
                .head(addressbook_address_key_head::<I, A, E>)
                .put(addressbook_address_key_put::<I, A, E>),
        )
        .route(
            "/addressbook/{address_key}/addrtype",
            delete(addressbook_address_key_addrtype_delete::<I, A, E>)
                .get(addressbook_address_key_addrtype_get::<I, A, E>)
                .head(addressbook_address_key_addrtype_head::<I, A, E>)
                .put(addressbook_address_key_addrtype_put::<I, A, E>),
        )
        .route(
            "/addressbook/{address_key}/city",
            delete(addressbook_address_key_city_delete::<I, A, E>)
                .get(addressbook_address_key_city_get::<I, A, E>)
                .head(addressbook_address_key_city_head::<I, A, E>)
                .put(addressbook_address_key_city_put::<I, A, E>),
        )
        .route(
            "/addressbook/{address_key}/country",
            delete(addressbook_address_key_country_delete::<I, A, E>)
                .get(addressbook_address_key_country_get::<I, A, E>)
                .head(addressbook_address_key_country_head::<I, A, E>)
                .put(addressbook_address_key_country_put::<I, A, E>),
        )
        .route(
            "/addressbook/{address_key}/is_valid",
            delete(addressbook_address_key_is_valid_delete::<I, A, E>)
                .get(addressbook_address_key_is_valid_get::<I, A, E>)
                .head(addressbook_address_key_is_valid_head::<I, A, E>)
                .put(addressbook_address_key_is_valid_put::<I, A, E>),
        )
        .route(
            "/addressbook/{address_key}/people",
            delete(addressbook_address_key_people_delete::<I, A, E>)
                .get(addressbook_address_key_people_get::<I, A, E>)
                .head(addressbook_address_key_people_head::<I, A, E>)
                .put(addressbook_address_key_people_put::<I, A, E>),
        )
        .route(
            "/addressbook/{address_key}/person",
            delete(addressbook_address_key_person_delete::<I, A, E>)
                .get(addressbook_address_key_person_get::<I, A, E>)
                .head(addressbook_address_key_person_head::<I, A, E>)
                .patch(addressbook_address_key_person_patch::<I, A, E>)
                .post(addressbook_address_key_person_post::<I, A, E>),
        )
        .route(
            "/addressbook/{address_key}/state",
            delete(addressbook_address_key_state_delete::<I, A, E>)
                .get(addressbook_address_key_state_get::<I, A, E>)
                .head(addressbook_address_key_state_head::<I, A, E>)
                .put(addressbook_address_key_state_put::<I, A, E>),
        )
        .route(
            "/addressbook/{address_key}/street",
            delete(addressbook_address_key_street_delete::<I, A, E>)
                .get(addressbook_address_key_street_get::<I, A, E>)
                .head(addressbook_address_key_street_head::<I, A, E>)
                .put(addressbook_address_key_street_put::<I, A, E>),
        )
        .route(
            "/persons",
            get(persons_get::<I, A, E, C>).post(persons_post::<I, A, E, C>),
        )
        .route(
            "/persons/{uuid}",
            delete(persons_uuid_delete::<I, A, E, C>)
                .get(persons_uuid_get::<I, A, E, C>)
                .head(persons_uuid_head::<I, A, E, C>)
                .put(persons_uuid_put::<I, A, E, C>),
        )
        .route(
            "/postal_codes",
            get(postal_codes_get::<I, A, E, C>).post(postal_codes_post::<I, A, E, C>),
        )
        .route(
            "/postal_codes/{uuid}",
            delete(postal_codes_uuid_delete::<I, A, E, C>)
                .get(postal_codes_uuid_get::<I, A, E, C>)
                .head(postal_codes_uuid_head::<I, A, E, C>),
        )
        .route(
            "/postal_codes/{uuid}/name",
            delete(postal_codes_uuid_name_delete::<I, A, E, C>)
                .get(postal_codes_uuid_name_get::<I, A, E, C>),
        )
        .with_state(api_impl)
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_addrtype_delete_validation(
    path_params: models::AddressbookAddressKeyAddrtypeDeletePathParams,
) -> std::result::Result<(models::AddressbookAddressKeyAddrtypeDeletePathParams,), ValidationErrors>
{
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyAddrtypeDelete - DELETE /addressbook/{address_key}/addrtype
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_addrtype_delete<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyAddrtypeDeletePathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_addrtype_delete_validation(path_params)
    })
    .await
    .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_addrtype_delete(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyAddrtypeDeleteResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_addrtype_get_validation(
    path_params: models::AddressbookAddressKeyAddrtypeGetPathParams,
    query_params: models::AddressbookAddressKeyAddrtypeGetQueryParams,
) -> std::result::Result<
    (
        models::AddressbookAddressKeyAddrtypeGetPathParams,
        models::AddressbookAddressKeyAddrtypeGetQueryParams,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;

    Ok((path_params, query_params))
}
/// AddressbookAddressKeyAddrtypeGet - GET /addressbook/{address_key}/addrtype
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_addrtype_get<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyAddrtypeGetPathParams>,
    QueryExtra(query_params): QueryExtra<models::AddressbookAddressKeyAddrtypeGetQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_addrtype_get_validation(path_params, query_params)
    })
    .await
    .unwrap();

    let Ok((path_params, query_params)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_addrtype_get(&method, &host, &cookies, &path_params, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyAddrtypeGetResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_addrtype_head_validation(
    path_params: models::AddressbookAddressKeyAddrtypeHeadPathParams,
) -> std::result::Result<(models::AddressbookAddressKeyAddrtypeHeadPathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyAddrtypeHead - HEAD /addressbook/{address_key}/addrtype
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_addrtype_head<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyAddrtypeHeadPathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_addrtype_head_validation(path_params)
    })
    .await
    .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_addrtype_head(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyAddrtypeHeadResponse::Status200_DefaultHEADResponse
                                                => {
                                                  let mut response = response.status(200);
                                                  response.body(Body::empty())
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[derive(validator::Validate)]
#[allow(dead_code)]
struct AddressbookAddressKeyAddrtypePutBodyValidator<'a> {
    #[validate(custom(function = "check_xss_string"))]
    body: &'a String,
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_addrtype_put_validation(
    path_params: models::AddressbookAddressKeyAddrtypePutPathParams,
    body: String,
) -> std::result::Result<
    (models::AddressbookAddressKeyAddrtypePutPathParams, String),
    ValidationErrors,
> {
    path_params.validate()?;
    let b = AddressbookAddressKeyAddrtypePutBodyValidator { body: &body };
    b.validate()?;

    Ok((path_params, body))
}
/// AddressbookAddressKeyAddrtypePut - PUT /addressbook/{address_key}/addrtype
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_addrtype_put<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyAddrtypePutPathParams>,
    State(api_impl): State<I>,
    Json(body): Json<String>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_addrtype_put_validation(path_params, body)
    })
    .await
    .unwrap();

    let Ok((path_params, body)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_addrtype_put(&method, &host, &cookies, &path_params, &body)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyAddrtypePutResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyAddrtypePutResponse::Status403_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(403);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyAddrtypePutResponse::Status422_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(422);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_city_delete_validation(
    path_params: models::AddressbookAddressKeyCityDeletePathParams,
) -> std::result::Result<(models::AddressbookAddressKeyCityDeletePathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyCityDelete - DELETE /addressbook/{address_key}/city
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_city_delete<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyCityDeletePathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_city_delete_validation(path_params)
    })
    .await
    .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_city_delete(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::addressbook::AddressbookAddressKeyCityDeleteResponse::Status200_ResponseForOK(
                body,
            ) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_city_get_validation(
    path_params: models::AddressbookAddressKeyCityGetPathParams,
    query_params: models::AddressbookAddressKeyCityGetQueryParams,
) -> std::result::Result<
    (
        models::AddressbookAddressKeyCityGetPathParams,
        models::AddressbookAddressKeyCityGetQueryParams,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;

    Ok((path_params, query_params))
}
/// AddressbookAddressKeyCityGet - GET /addressbook/{address_key}/city
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_city_get<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyCityGetPathParams>,
    QueryExtra(query_params): QueryExtra<models::AddressbookAddressKeyCityGetQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_city_get_validation(path_params, query_params)
    })
    .await
    .unwrap();

    let Ok((path_params, query_params)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_city_get(&method, &host, &cookies, &path_params, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::addressbook::AddressbookAddressKeyCityGetResponse::Status200_ResponseForOK(
                body,
            ) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_city_head_validation(
    path_params: models::AddressbookAddressKeyCityHeadPathParams,
) -> std::result::Result<(models::AddressbookAddressKeyCityHeadPathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyCityHead - HEAD /addressbook/{address_key}/city
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_city_head<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyCityHeadPathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_city_head_validation(path_params)
    })
    .await
    .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_city_head(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyCityHeadResponse::Status200_DefaultHEADResponse
                                                => {
                                                  let mut response = response.status(200);
                                                  response.body(Body::empty())
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[derive(validator::Validate)]
#[allow(dead_code)]
struct AddressbookAddressKeyCityPutBodyValidator<'a> {
    #[validate(custom(function = "check_xss_string"))]
    body: &'a String,
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_city_put_validation(
    path_params: models::AddressbookAddressKeyCityPutPathParams,
    body: String,
) -> std::result::Result<(models::AddressbookAddressKeyCityPutPathParams, String), ValidationErrors>
{
    path_params.validate()?;
    let b = AddressbookAddressKeyCityPutBodyValidator { body: &body };
    b.validate()?;

    Ok((path_params, body))
}
/// AddressbookAddressKeyCityPut - PUT /addressbook/{address_key}/city
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_city_put<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyCityPutPathParams>,
    State(api_impl): State<I>,
    Json(body): Json<String>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_city_put_validation(path_params, body)
    })
    .await
    .unwrap();

    let Ok((path_params, body)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_city_put(&method, &host, &cookies, &path_params, &body)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyCityPutResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyCityPutResponse::Status403_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(403);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyCityPutResponse::Status422_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(422);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_country_delete_validation(
    path_params: models::AddressbookAddressKeyCountryDeletePathParams,
) -> std::result::Result<(models::AddressbookAddressKeyCountryDeletePathParams,), ValidationErrors>
{
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyCountryDelete - DELETE /addressbook/{address_key}/country
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_country_delete<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyCountryDeletePathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_country_delete_validation(path_params)
    })
    .await
    .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_country_delete(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyCountryDeleteResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_country_get_validation(
    path_params: models::AddressbookAddressKeyCountryGetPathParams,
    query_params: models::AddressbookAddressKeyCountryGetQueryParams,
) -> std::result::Result<
    (
        models::AddressbookAddressKeyCountryGetPathParams,
        models::AddressbookAddressKeyCountryGetQueryParams,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;

    Ok((path_params, query_params))
}
/// AddressbookAddressKeyCountryGet - GET /addressbook/{address_key}/country
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_country_get<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyCountryGetPathParams>,
    QueryExtra(query_params): QueryExtra<models::AddressbookAddressKeyCountryGetQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_country_get_validation(path_params, query_params)
    })
    .await
    .unwrap();

    let Ok((path_params, query_params)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_country_get(&method, &host, &cookies, &path_params, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::addressbook::AddressbookAddressKeyCountryGetResponse::Status200_ResponseForOK(
                body,
            ) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_country_head_validation(
    path_params: models::AddressbookAddressKeyCountryHeadPathParams,
) -> std::result::Result<(models::AddressbookAddressKeyCountryHeadPathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyCountryHead - HEAD /addressbook/{address_key}/country
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_country_head<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyCountryHeadPathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_country_head_validation(path_params)
    })
    .await
    .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_country_head(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyCountryHeadResponse::Status200_DefaultHEADResponse
                                                => {
                                                  let mut response = response.status(200);
                                                  response.body(Body::empty())
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[derive(validator::Validate)]
#[allow(dead_code)]
struct AddressbookAddressKeyCountryPutBodyValidator<'a> {
    #[validate(custom(function = "check_xss_string"))]
    body: &'a String,
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_country_put_validation(
    path_params: models::AddressbookAddressKeyCountryPutPathParams,
    body: String,
) -> std::result::Result<
    (models::AddressbookAddressKeyCountryPutPathParams, String),
    ValidationErrors,
> {
    path_params.validate()?;
    let b = AddressbookAddressKeyCountryPutBodyValidator { body: &body };
    b.validate()?;

    Ok((path_params, body))
}
/// AddressbookAddressKeyCountryPut - PUT /addressbook/{address_key}/country
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_country_put<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyCountryPutPathParams>,
    State(api_impl): State<I>,
    Json(body): Json<String>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_country_put_validation(path_params, body)
    })
    .await
    .unwrap();

    let Ok((path_params, body)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_country_put(&method, &host, &cookies, &path_params, &body)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyCountryPutResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyCountryPutResponse::Status403_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(403);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyCountryPutResponse::Status422_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(422);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_delete_validation(
    path_params: models::AddressbookAddressKeyDeletePathParams,
) -> std::result::Result<(models::AddressbookAddressKeyDeletePathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyDelete - DELETE /addressbook/{address_key}
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_delete<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyDeletePathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation =
        tokio::task::spawn_blocking(move || addressbook_address_key_delete_validation(path_params))
            .await
            .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_delete(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::addressbook::AddressbookAddressKeyDeleteResponse::Status200_ResponseForOK(
                body,
            ) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_get_validation(
    path_params: models::AddressbookAddressKeyGetPathParams,
    query_params: models::AddressbookAddressKeyGetQueryParams,
) -> std::result::Result<
    (
        models::AddressbookAddressKeyGetPathParams,
        models::AddressbookAddressKeyGetQueryParams,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;

    Ok((path_params, query_params))
}
/// AddressbookAddressKeyGet - GET /addressbook/{address_key}
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_get<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyGetPathParams>,
    QueryExtra(query_params): QueryExtra<models::AddressbookAddressKeyGetQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_get_validation(path_params, query_params)
    })
    .await
    .unwrap();

    let Ok((path_params, query_params)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_get(&method, &host, &cookies, &path_params, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::addressbook::AddressbookAddressKeyGetResponse::Status200_ResponseForOK(body) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_head_validation(
    path_params: models::AddressbookAddressKeyHeadPathParams,
) -> std::result::Result<(models::AddressbookAddressKeyHeadPathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyHead - HEAD /addressbook/{address_key}
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_head<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyHeadPathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation =
        tokio::task::spawn_blocking(move || addressbook_address_key_head_validation(path_params))
            .await
            .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_head(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::addressbook::AddressbookAddressKeyHeadResponse::Status200_DefaultHEADResponse => {
                let mut response = response.status(200);
                response.body(Body::empty())
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_is_valid_delete_validation(
    path_params: models::AddressbookAddressKeyIsValidDeletePathParams,
) -> std::result::Result<(models::AddressbookAddressKeyIsValidDeletePathParams,), ValidationErrors>
{
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyIsValidDelete - DELETE /addressbook/{address_key}/is_valid
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_is_valid_delete<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyIsValidDeletePathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_is_valid_delete_validation(path_params)
    })
    .await
    .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_is_valid_delete(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyIsValidDeleteResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_is_valid_get_validation(
    path_params: models::AddressbookAddressKeyIsValidGetPathParams,
    query_params: models::AddressbookAddressKeyIsValidGetQueryParams,
) -> std::result::Result<
    (
        models::AddressbookAddressKeyIsValidGetPathParams,
        models::AddressbookAddressKeyIsValidGetQueryParams,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;

    Ok((path_params, query_params))
}
/// AddressbookAddressKeyIsValidGet - GET /addressbook/{address_key}/is_valid
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_is_valid_get<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyIsValidGetPathParams>,
    QueryExtra(query_params): QueryExtra<models::AddressbookAddressKeyIsValidGetQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_is_valid_get_validation(path_params, query_params)
    })
    .await
    .unwrap();

    let Ok((path_params, query_params)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_is_valid_get(&method, &host, &cookies, &path_params, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::addressbook::AddressbookAddressKeyIsValidGetResponse::Status200_ResponseForOK(
                body,
            ) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_is_valid_head_validation(
    path_params: models::AddressbookAddressKeyIsValidHeadPathParams,
) -> std::result::Result<(models::AddressbookAddressKeyIsValidHeadPathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyIsValidHead - HEAD /addressbook/{address_key}/is_valid
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_is_valid_head<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyIsValidHeadPathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_is_valid_head_validation(path_params)
    })
    .await
    .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_is_valid_head(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyIsValidHeadResponse::Status200_DefaultHEADResponse
                                                => {
                                                  let mut response = response.status(200);
                                                  response.body(Body::empty())
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[derive(validator::Validate)]
#[allow(dead_code)]
struct AddressbookAddressKeyIsValidPutBodyValidator<'a> {
    body: &'a bool,
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_is_valid_put_validation(
    path_params: models::AddressbookAddressKeyIsValidPutPathParams,
    body: bool,
) -> std::result::Result<(models::AddressbookAddressKeyIsValidPutPathParams, bool), ValidationErrors>
{
    path_params.validate()?;
    let b = AddressbookAddressKeyIsValidPutBodyValidator { body: &body };
    b.validate()?;

    Ok((path_params, body))
}
/// AddressbookAddressKeyIsValidPut - PUT /addressbook/{address_key}/is_valid
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_is_valid_put<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyIsValidPutPathParams>,
    State(api_impl): State<I>,
    Json(body): Json<bool>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_is_valid_put_validation(path_params, body)
    })
    .await
    .unwrap();

    let Ok((path_params, body)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_is_valid_put(&method, &host, &cookies, &path_params, &body)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyIsValidPutResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyIsValidPutResponse::Status403_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(403);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyIsValidPutResponse::Status422_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(422);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_people_delete_validation(
    path_params: models::AddressbookAddressKeyPeopleDeletePathParams,
) -> std::result::Result<(models::AddressbookAddressKeyPeopleDeletePathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyPeopleDelete - DELETE /addressbook/{address_key}/people
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_people_delete<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyPeopleDeletePathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_people_delete_validation(path_params)
    })
    .await
    .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_people_delete(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyPeopleDeleteResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_people_get_validation(
    path_params: models::AddressbookAddressKeyPeopleGetPathParams,
    query_params: models::AddressbookAddressKeyPeopleGetQueryParams,
) -> std::result::Result<
    (
        models::AddressbookAddressKeyPeopleGetPathParams,
        models::AddressbookAddressKeyPeopleGetQueryParams,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;

    Ok((path_params, query_params))
}
/// AddressbookAddressKeyPeopleGet - GET /addressbook/{address_key}/people
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_people_get<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyPeopleGetPathParams>,
    QueryExtra(query_params): QueryExtra<models::AddressbookAddressKeyPeopleGetQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_people_get_validation(path_params, query_params)
    })
    .await
    .unwrap();

    let Ok((path_params, query_params)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_people_get(&method, &host, &cookies, &path_params, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::addressbook::AddressbookAddressKeyPeopleGetResponse::Status200_ResponseForOK(
                body,
            ) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_people_head_validation(
    path_params: models::AddressbookAddressKeyPeopleHeadPathParams,
) -> std::result::Result<(models::AddressbookAddressKeyPeopleHeadPathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyPeopleHead - HEAD /addressbook/{address_key}/people
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_people_head<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyPeopleHeadPathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_people_head_validation(path_params)
    })
    .await
    .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_people_head(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyPeopleHeadResponse::Status200_DefaultHEADResponse
                                                => {
                                                  let mut response = response.status(200);
                                                  response.body(Body::empty())
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[derive(validator::Validate)]
#[allow(dead_code)]
struct AddressbookAddressKeyPeoplePutBodyValidator<'a> {
    #[validate(custom(function = "check_xss_vec_string"))]
    body: &'a Vec<String>,
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_people_put_validation(
    path_params: models::AddressbookAddressKeyPeoplePutPathParams,
    body: Vec<String>,
) -> std::result::Result<
    (
        models::AddressbookAddressKeyPeoplePutPathParams,
        Vec<String>,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    let b = AddressbookAddressKeyPeoplePutBodyValidator { body: &body };
    b.validate()?;

    Ok((path_params, body))
}
/// AddressbookAddressKeyPeoplePut - PUT /addressbook/{address_key}/people
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_people_put<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyPeoplePutPathParams>,
    State(api_impl): State<I>,
    Json(body): Json<Vec<String>>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_people_put_validation(path_params, body)
    })
    .await
    .unwrap();

    let Ok((path_params, body)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_people_put(&method, &host, &cookies, &path_params, &body)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyPeoplePutResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyPeoplePutResponse::Status403_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(403);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyPeoplePutResponse::Status422_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(422);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_person_delete_validation(
    path_params: models::AddressbookAddressKeyPersonDeletePathParams,
    query_params: models::AddressbookAddressKeyPersonDeleteQueryParams,
) -> std::result::Result<
    (
        models::AddressbookAddressKeyPersonDeletePathParams,
        models::AddressbookAddressKeyPersonDeleteQueryParams,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;

    Ok((path_params, query_params))
}
/// AddressbookAddressKeyPersonDelete - DELETE /addressbook/{address_key}/person
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_person_delete<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyPersonDeletePathParams>,
    QueryExtra(query_params): QueryExtra<models::AddressbookAddressKeyPersonDeleteQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_person_delete_validation(path_params, query_params)
    })
    .await
    .unwrap();

    let Ok((path_params, query_params)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_person_delete(
            &method,
            &host,
            &cookies,
            &path_params,
            &query_params,
        )
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyPersonDeleteResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_person_get_validation(
    path_params: models::AddressbookAddressKeyPersonGetPathParams,
    query_params: models::AddressbookAddressKeyPersonGetQueryParams,
) -> std::result::Result<
    (
        models::AddressbookAddressKeyPersonGetPathParams,
        models::AddressbookAddressKeyPersonGetQueryParams,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;

    Ok((path_params, query_params))
}
/// AddressbookAddressKeyPersonGet - GET /addressbook/{address_key}/person
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_person_get<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyPersonGetPathParams>,
    QueryExtra(query_params): QueryExtra<models::AddressbookAddressKeyPersonGetQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_person_get_validation(path_params, query_params)
    })
    .await
    .unwrap();

    let Ok((path_params, query_params)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_person_get(&method, &host, &cookies, &path_params, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::addressbook::AddressbookAddressKeyPersonGetResponse::Status200_ResponseForOK(
                body,
            ) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_person_head_validation(
    path_params: models::AddressbookAddressKeyPersonHeadPathParams,
    query_params: models::AddressbookAddressKeyPersonHeadQueryParams,
) -> std::result::Result<
    (
        models::AddressbookAddressKeyPersonHeadPathParams,
        models::AddressbookAddressKeyPersonHeadQueryParams,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;

    Ok((path_params, query_params))
}
/// AddressbookAddressKeyPersonHead - HEAD /addressbook/{address_key}/person
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_person_head<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyPersonHeadPathParams>,
    QueryExtra(query_params): QueryExtra<models::AddressbookAddressKeyPersonHeadQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_person_head_validation(path_params, query_params)
    })
    .await
    .unwrap();

    let Ok((path_params, query_params)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_person_head(&method, &host, &cookies, &path_params, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyPersonHeadResponse::Status200_DefaultHEADResponse
                                                => {
                                                  let mut response = response.status(200);
                                                  response.body(Body::empty())
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_person_patch_validation(
    path_params: models::AddressbookAddressKeyPersonPatchPathParams,
    query_params: models::AddressbookAddressKeyPersonPatchQueryParams,
) -> std::result::Result<
    (
        models::AddressbookAddressKeyPersonPatchPathParams,
        models::AddressbookAddressKeyPersonPatchQueryParams,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;

    Ok((path_params, query_params))
}
/// AddressbookAddressKeyPersonPatch - PATCH /addressbook/{address_key}/person
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_person_patch<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyPersonPatchPathParams>,
    QueryExtra(query_params): QueryExtra<models::AddressbookAddressKeyPersonPatchQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_person_patch_validation(path_params, query_params)
    })
    .await
    .unwrap();

    let Ok((path_params, query_params)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_person_patch(&method, &host, &cookies, &path_params, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyPersonPatchResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyPersonPatchResponse::Status403_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(403);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyPersonPatchResponse::Status422_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(422);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[derive(validator::Validate)]
#[allow(dead_code)]
struct AddressbookAddressKeyPersonPostBodyValidator<'a> {
    #[validate(nested)]
    body: &'a models::CreatePerson,
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_person_post_validation(
    path_params: models::AddressbookAddressKeyPersonPostPathParams,
    query_params: models::AddressbookAddressKeyPersonPostQueryParams,
    body: models::CreatePerson,
) -> std::result::Result<
    (
        models::AddressbookAddressKeyPersonPostPathParams,
        models::AddressbookAddressKeyPersonPostQueryParams,
        models::CreatePerson,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;
    let b = AddressbookAddressKeyPersonPostBodyValidator { body: &body };
    b.validate()?;

    Ok((path_params, query_params, body))
}
/// AddressbookAddressKeyPersonPost - POST /addressbook/{address_key}/person
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_person_post<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyPersonPostPathParams>,
    QueryExtra(query_params): QueryExtra<models::AddressbookAddressKeyPersonPostQueryParams>,
    State(api_impl): State<I>,
    Json(body): Json<models::CreatePerson>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_person_post_validation(path_params, query_params, body)
    })
    .await
    .unwrap();

    let Ok((path_params, query_params, body)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_person_post(
            &method,
            &host,
            &cookies,
            &path_params,
            &query_params,
            &body,
        )
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyPersonPostResponse::Status201_ResponseForCREATED
                                                    (body)
                                                => {
                                                  let mut response = response.status(201);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyPersonPostResponse::Status422_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(422);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[derive(validator::Validate)]
#[allow(dead_code)]
struct AddressbookAddressKeyPutBodyValidator<'a> {
    #[validate(nested)]
    body: &'a models::UpdateAddressbook,
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_put_validation(
    path_params: models::AddressbookAddressKeyPutPathParams,
    body: models::UpdateAddressbook,
) -> std::result::Result<
    (
        models::AddressbookAddressKeyPutPathParams,
        models::UpdateAddressbook,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    let b = AddressbookAddressKeyPutBodyValidator { body: &body };
    b.validate()?;

    Ok((path_params, body))
}
/// AddressbookAddressKeyPut - PUT /addressbook/{address_key}
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_put<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyPutPathParams>,
    State(api_impl): State<I>,
    Json(body): Json<models::UpdateAddressbook>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_put_validation(path_params, body)
    })
    .await
    .unwrap();

    let Ok((path_params, body)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_put(&method, &host, &cookies, &path_params, &body)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyPutResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyPutResponse::Status403_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(403);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyPutResponse::Status422_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(422);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_state_delete_validation(
    path_params: models::AddressbookAddressKeyStateDeletePathParams,
) -> std::result::Result<(models::AddressbookAddressKeyStateDeletePathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyStateDelete - DELETE /addressbook/{address_key}/state
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_state_delete<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyStateDeletePathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_state_delete_validation(path_params)
    })
    .await
    .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_state_delete(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyStateDeleteResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_state_get_validation(
    path_params: models::AddressbookAddressKeyStateGetPathParams,
    query_params: models::AddressbookAddressKeyStateGetQueryParams,
) -> std::result::Result<
    (
        models::AddressbookAddressKeyStateGetPathParams,
        models::AddressbookAddressKeyStateGetQueryParams,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;

    Ok((path_params, query_params))
}
/// AddressbookAddressKeyStateGet - GET /addressbook/{address_key}/state
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_state_get<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyStateGetPathParams>,
    QueryExtra(query_params): QueryExtra<models::AddressbookAddressKeyStateGetQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_state_get_validation(path_params, query_params)
    })
    .await
    .unwrap();

    let Ok((path_params, query_params)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_state_get(&method, &host, &cookies, &path_params, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::addressbook::AddressbookAddressKeyStateGetResponse::Status200_ResponseForOK(
                body,
            ) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_state_head_validation(
    path_params: models::AddressbookAddressKeyStateHeadPathParams,
) -> std::result::Result<(models::AddressbookAddressKeyStateHeadPathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyStateHead - HEAD /addressbook/{address_key}/state
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_state_head<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyStateHeadPathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_state_head_validation(path_params)
    })
    .await
    .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_state_head(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyStateHeadResponse::Status200_DefaultHEADResponse
                                                => {
                                                  let mut response = response.status(200);
                                                  response.body(Body::empty())
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[derive(validator::Validate)]
#[allow(dead_code)]
struct AddressbookAddressKeyStatePutBodyValidator<'a> {
    #[validate(custom(function = "check_xss_string"))]
    body: &'a String,
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_state_put_validation(
    path_params: models::AddressbookAddressKeyStatePutPathParams,
    body: String,
) -> std::result::Result<(models::AddressbookAddressKeyStatePutPathParams, String), ValidationErrors>
{
    path_params.validate()?;
    let b = AddressbookAddressKeyStatePutBodyValidator { body: &body };
    b.validate()?;

    Ok((path_params, body))
}
/// AddressbookAddressKeyStatePut - PUT /addressbook/{address_key}/state
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_state_put<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyStatePutPathParams>,
    State(api_impl): State<I>,
    Json(body): Json<String>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_state_put_validation(path_params, body)
    })
    .await
    .unwrap();

    let Ok((path_params, body)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_state_put(&method, &host, &cookies, &path_params, &body)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyStatePutResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyStatePutResponse::Status403_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(403);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyStatePutResponse::Status422_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(422);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_street_delete_validation(
    path_params: models::AddressbookAddressKeyStreetDeletePathParams,
) -> std::result::Result<(models::AddressbookAddressKeyStreetDeletePathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyStreetDelete - DELETE /addressbook/{address_key}/street
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_street_delete<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyStreetDeletePathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_street_delete_validation(path_params)
    })
    .await
    .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_street_delete(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyStreetDeleteResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_street_get_validation(
    path_params: models::AddressbookAddressKeyStreetGetPathParams,
    query_params: models::AddressbookAddressKeyStreetGetQueryParams,
) -> std::result::Result<
    (
        models::AddressbookAddressKeyStreetGetPathParams,
        models::AddressbookAddressKeyStreetGetQueryParams,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;

    Ok((path_params, query_params))
}
/// AddressbookAddressKeyStreetGet - GET /addressbook/{address_key}/street
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_street_get<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyStreetGetPathParams>,
    QueryExtra(query_params): QueryExtra<models::AddressbookAddressKeyStreetGetQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_street_get_validation(path_params, query_params)
    })
    .await
    .unwrap();

    let Ok((path_params, query_params)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_street_get(&method, &host, &cookies, &path_params, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::addressbook::AddressbookAddressKeyStreetGetResponse::Status200_ResponseForOK(
                body,
            ) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_street_head_validation(
    path_params: models::AddressbookAddressKeyStreetHeadPathParams,
) -> std::result::Result<(models::AddressbookAddressKeyStreetHeadPathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// AddressbookAddressKeyStreetHead - HEAD /addressbook/{address_key}/street
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_street_head<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyStreetHeadPathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_street_head_validation(path_params)
    })
    .await
    .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_street_head(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyStreetHeadResponse::Status200_DefaultHEADResponse
                                                => {
                                                  let mut response = response.status(200);
                                                  response.body(Body::empty())
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[derive(validator::Validate)]
#[allow(dead_code)]
struct AddressbookAddressKeyStreetPutBodyValidator<'a> {
    #[validate(custom(function = "check_xss_string"))]
    body: &'a String,
}

#[tracing::instrument(skip_all)]
fn addressbook_address_key_street_put_validation(
    path_params: models::AddressbookAddressKeyStreetPutPathParams,
    body: String,
) -> std::result::Result<(models::AddressbookAddressKeyStreetPutPathParams, String), ValidationErrors>
{
    path_params.validate()?;
    let b = AddressbookAddressKeyStreetPutBodyValidator { body: &body };
    b.validate()?;

    Ok((path_params, body))
}
/// AddressbookAddressKeyStreetPut - PUT /addressbook/{address_key}/street
#[tracing::instrument(skip_all)]
async fn addressbook_address_key_street_put<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::AddressbookAddressKeyStreetPutPathParams>,
    State(api_impl): State<I>,
    Json(body): Json<String>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        addressbook_address_key_street_put_validation(path_params, body)
    })
    .await
    .unwrap();

    let Ok((path_params, body)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_address_key_street_put(&method, &host, &cookies, &path_params, &body)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookAddressKeyStreetPutResponse::Status200_ResponseForOK
                                                    (body)
                                                => {
                                                  let mut response = response.status(200);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyStreetPutResponse::Status403_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(403);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookAddressKeyStreetPutResponse::Status422_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(422);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn addressbook_get_validation(
    query_params: models::AddressbookGetQueryParams,
) -> std::result::Result<(models::AddressbookGetQueryParams,), ValidationErrors> {
    query_params.validate()?;

    Ok((query_params,))
}
/// AddressbookGet - GET /addressbook
#[tracing::instrument(skip_all)]
async fn addressbook_get<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    QueryExtra(query_params): QueryExtra<models::AddressbookGetQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || addressbook_get_validation(query_params))
        .await
        .unwrap();

    let Ok((query_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_get(&method, &host, &cookies, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::addressbook::AddressbookGetResponse::Status200_ResponseForOK(body) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[derive(validator::Validate)]
#[allow(dead_code)]
struct AddressbookPostBodyValidator<'a> {
    #[validate(nested)]
    body: &'a models::CreateAddressbook,
}

#[tracing::instrument(skip_all)]
fn addressbook_post_validation(
    query_params: models::AddressbookPostQueryParams,
    body: models::CreateAddressbook,
) -> std::result::Result<
    (
        models::AddressbookPostQueryParams,
        models::CreateAddressbook,
    ),
    ValidationErrors,
> {
    query_params.validate()?;
    let b = AddressbookPostBodyValidator { body: &body };
    b.validate()?;

    Ok((query_params, body))
}
/// AddressbookPost - POST /addressbook
#[tracing::instrument(skip_all)]
async fn addressbook_post<I, A, E>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    QueryExtra(query_params): QueryExtra<models::AddressbookPostQueryParams>,
    State(api_impl): State<I>,
    Json(body): Json<models::CreateAddressbook>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::addressbook::Addressbook<E> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation =
        tokio::task::spawn_blocking(move || addressbook_post_validation(query_params, body))
            .await
            .unwrap();

    let Ok((query_params, body)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .addressbook_post(&method, &host, &cookies, &query_params, &body)
        .await;

    let mut response = Response::builder();

    let resp = match result {
                                            Ok(rsp) => match rsp {
                                                apis::addressbook::AddressbookPostResponse::Status201_ResponseForCREATED
                                                    (body)
                                                => {
                                                  let mut response = response.status(201);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                                apis::addressbook::AddressbookPostResponse::Status422_OneOrMoreValidationRulesFailed
                                                    (body)
                                                => {
                                                  let mut response = response.status(422);
                                                  {
                                                    let mut response_headers = response.headers_mut().unwrap();
                                                    response_headers.insert(
                                                        CONTENT_TYPE,
                                                        HeaderValue::from_static("application/problem+json"));
                                                  }

                                                  let body_content =  tokio::task::spawn_blocking(move ||
                                                      serde_json::to_vec(&body).map_err(|e| {
                                                        error!(error = ?e);
                                                        StatusCode::INTERNAL_SERVER_ERROR
                                                      })).await.unwrap()?;
                                                  response.body(Body::from(body_content))
                                                },
                                            },
                                            Err(why) => {
                                                    // Application code returned an error. This should not happen, as the implementation should
                                                    // return a valid response.
                                                    return api_impl.as_ref().handle_error(&method, &host, &cookies, why).await;
                                            },
                                        };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn persons_get_validation(
    query_params: models::PersonsGetQueryParams,
) -> std::result::Result<(models::PersonsGetQueryParams,), ValidationErrors> {
    query_params.validate()?;

    Ok((query_params,))
}
/// PersonsGet - GET /persons
#[tracing::instrument(skip_all)]
async fn persons_get<I, A, E, C>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    QueryExtra(query_params): QueryExtra<models::PersonsGetQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::persons::Persons<E, Claims = C> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || persons_get_validation(query_params))
        .await
        .unwrap();

    let Ok((query_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .persons_get(&method, &host, &cookies, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::persons::PersonsGetResponse::Status200_ResponseForOK(body) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[derive(validator::Validate)]
#[allow(dead_code)]
struct PersonsPostBodyValidator<'a> {
    #[validate(nested)]
    body: &'a models::CreatePerson,
}

#[tracing::instrument(skip_all)]
fn persons_post_validation(
    query_params: models::PersonsPostQueryParams,
    body: models::CreatePerson,
) -> std::result::Result<(models::PersonsPostQueryParams, models::CreatePerson), ValidationErrors> {
    query_params.validate()?;
    let b = PersonsPostBodyValidator { body: &body };
    b.validate()?;

    Ok((query_params, body))
}
/// PersonsPost - POST /persons
#[tracing::instrument(skip_all)]
async fn persons_post<I, A, E, C>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    headers: HeaderMap,
    QueryExtra(query_params): QueryExtra<models::PersonsPostQueryParams>,
    State(api_impl): State<I>,
    Json(body): Json<models::CreatePerson>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::persons::Persons<E, Claims = C> + apis::ApiAuthBasic<Claims = C> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    // Authentication
    let claims_in_auth_header = api_impl
        .as_ref()
        .extract_claims_from_auth_header(apis::BasicAuthKind::Bearer, &headers, "authorization")
        .await;
    let claims = None.or(claims_in_auth_header);
    let Some(claims) = claims else {
        return response_with_status_code_only(StatusCode::UNAUTHORIZED);
    };

    #[allow(clippy::redundant_closure)]
    let validation =
        tokio::task::spawn_blocking(move || persons_post_validation(query_params, body))
            .await
            .unwrap();

    let Ok((query_params, body)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .persons_post(&method, &host, &cookies, &claims, &query_params, &body)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::persons::PersonsPostResponse::Status201_ResponseForCREATED(body) => {
                let mut response = response.status(201);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn persons_uuid_delete_validation(
    path_params: models::PersonsUuidDeletePathParams,
) -> std::result::Result<(models::PersonsUuidDeletePathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// PersonsUuidDelete - DELETE /persons/{uuid}
#[tracing::instrument(skip_all)]
async fn persons_uuid_delete<I, A, E, C>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    headers: HeaderMap,
    Path(path_params): Path<models::PersonsUuidDeletePathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::persons::Persons<E, Claims = C> + apis::ApiAuthBasic<Claims = C> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    // Authentication
    let claims_in_auth_header = api_impl
        .as_ref()
        .extract_claims_from_auth_header(apis::BasicAuthKind::Bearer, &headers, "authorization")
        .await;
    let claims = None.or(claims_in_auth_header);
    let Some(claims) = claims else {
        return response_with_status_code_only(StatusCode::UNAUTHORIZED);
    };

    #[allow(clippy::redundant_closure)]
    let validation =
        tokio::task::spawn_blocking(move || persons_uuid_delete_validation(path_params))
            .await
            .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .persons_uuid_delete(&method, &host, &cookies, &claims, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::persons::PersonsUuidDeleteResponse::Status200_ResponseForOK(body) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
            apis::persons::PersonsUuidDeleteResponse::Status409_OneOrMoreValidationRulesFailed(
                body,
            ) => {
                let mut response = response.status(409);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers.insert(
                        CONTENT_TYPE,
                        HeaderValue::from_static("application/problem+json"),
                    );
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn persons_uuid_get_validation(
    path_params: models::PersonsUuidGetPathParams,
    query_params: models::PersonsUuidGetQueryParams,
) -> std::result::Result<
    (
        models::PersonsUuidGetPathParams,
        models::PersonsUuidGetQueryParams,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;

    Ok((path_params, query_params))
}
/// PersonsUuidGet - GET /persons/{uuid}
#[tracing::instrument(skip_all)]
async fn persons_uuid_get<I, A, E, C>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::PersonsUuidGetPathParams>,
    QueryExtra(query_params): QueryExtra<models::PersonsUuidGetQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::persons::Persons<E, Claims = C> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation =
        tokio::task::spawn_blocking(move || persons_uuid_get_validation(path_params, query_params))
            .await
            .unwrap();

    let Ok((path_params, query_params)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .persons_uuid_get(&method, &host, &cookies, &path_params, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::persons::PersonsUuidGetResponse::Status200_ResponseForOK(body) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn persons_uuid_head_validation(
    path_params: models::PersonsUuidHeadPathParams,
) -> std::result::Result<(models::PersonsUuidHeadPathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// PersonsUuidHead - HEAD /persons/{uuid}
#[tracing::instrument(skip_all)]
async fn persons_uuid_head<I, A, E, C>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::PersonsUuidHeadPathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::persons::Persons<E, Claims = C> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || persons_uuid_head_validation(path_params))
        .await
        .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .persons_uuid_head(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::persons::PersonsUuidHeadResponse::Status200_DefaultHEADResponse => {
                let mut response = response.status(200);
                response.body(Body::empty())
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[derive(validator::Validate)]
#[allow(dead_code)]
struct PersonsUuidPutBodyValidator<'a> {
    #[validate(nested)]
    body: &'a models::UpdatePerson,
}

#[tracing::instrument(skip_all)]
fn persons_uuid_put_validation(
    path_params: models::PersonsUuidPutPathParams,
    body: models::UpdatePerson,
) -> std::result::Result<(models::PersonsUuidPutPathParams, models::UpdatePerson), ValidationErrors>
{
    path_params.validate()?;
    let b = PersonsUuidPutBodyValidator { body: &body };
    b.validate()?;

    Ok((path_params, body))
}
/// PersonsUuidPut - PUT /persons/{uuid}
#[tracing::instrument(skip_all)]
async fn persons_uuid_put<I, A, E, C>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    headers: HeaderMap,
    Path(path_params): Path<models::PersonsUuidPutPathParams>,
    State(api_impl): State<I>,
    Json(body): Json<models::UpdatePerson>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::persons::Persons<E, Claims = C> + apis::ApiAuthBasic<Claims = C> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    // Authentication
    let claims_in_auth_header = api_impl
        .as_ref()
        .extract_claims_from_auth_header(apis::BasicAuthKind::Bearer, &headers, "authorization")
        .await;
    let claims = None.or(claims_in_auth_header);
    let Some(claims) = claims else {
        return response_with_status_code_only(StatusCode::UNAUTHORIZED);
    };

    #[allow(clippy::redundant_closure)]
    let validation =
        tokio::task::spawn_blocking(move || persons_uuid_put_validation(path_params, body))
            .await
            .unwrap();

    let Ok((path_params, body)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .persons_uuid_put(&method, &host, &cookies, &claims, &path_params, &body)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::persons::PersonsUuidPutResponse::Status200_ResponseForOK(body) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn postal_codes_get_validation(
    query_params: models::PostalCodesGetQueryParams,
) -> std::result::Result<(models::PostalCodesGetQueryParams,), ValidationErrors> {
    query_params.validate()?;

    Ok((query_params,))
}
/// PostalCodesGet - GET /postal_codes
#[tracing::instrument(skip_all)]
async fn postal_codes_get<I, A, E, C>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    QueryExtra(query_params): QueryExtra<models::PostalCodesGetQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::postal_codes::PostalCodes<E, Claims = C> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || postal_codes_get_validation(query_params))
        .await
        .unwrap();

    let Ok((query_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .postal_codes_get(&method, &host, &cookies, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::postal_codes::PostalCodesGetResponse::Status200_ResponseForOK(body) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[derive(validator::Validate)]
#[allow(dead_code)]
struct PostalCodesPostBodyValidator<'a> {
    #[validate(nested)]
    body: &'a models::CreatePostalCode,
}

#[tracing::instrument(skip_all)]
fn postal_codes_post_validation(
    query_params: models::PostalCodesPostQueryParams,
    body: models::CreatePostalCode,
) -> std::result::Result<
    (models::PostalCodesPostQueryParams, models::CreatePostalCode),
    ValidationErrors,
> {
    query_params.validate()?;
    let b = PostalCodesPostBodyValidator { body: &body };
    b.validate()?;

    Ok((query_params, body))
}
/// PostalCodesPost - POST /postal_codes
#[tracing::instrument(skip_all)]
async fn postal_codes_post<I, A, E, C>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    headers: HeaderMap,
    QueryExtra(query_params): QueryExtra<models::PostalCodesPostQueryParams>,
    State(api_impl): State<I>,
    Json(body): Json<models::CreatePostalCode>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::postal_codes::PostalCodes<E, Claims = C>
        + apis::ApiAuthBasic<Claims = C>
        + Send
        + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    // Authentication
    let claims_in_auth_header = api_impl
        .as_ref()
        .extract_claims_from_auth_header(apis::BasicAuthKind::Bearer, &headers, "authorization")
        .await;
    let claims = None.or(claims_in_auth_header);
    let Some(claims) = claims else {
        return response_with_status_code_only(StatusCode::UNAUTHORIZED);
    };

    #[allow(clippy::redundant_closure)]
    let validation =
        tokio::task::spawn_blocking(move || postal_codes_post_validation(query_params, body))
            .await
            .unwrap();

    let Ok((query_params, body)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .postal_codes_post(&method, &host, &cookies, &claims, &query_params, &body)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::postal_codes::PostalCodesPostResponse::Status201_ResponseForCREATED(body) => {
                let mut response = response.status(201);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn postal_codes_uuid_delete_validation(
    path_params: models::PostalCodesUuidDeletePathParams,
) -> std::result::Result<(models::PostalCodesUuidDeletePathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// PostalCodesUuidDelete - DELETE /postal_codes/{uuid}
#[tracing::instrument(skip_all)]
async fn postal_codes_uuid_delete<I, A, E, C>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    headers: HeaderMap,
    Path(path_params): Path<models::PostalCodesUuidDeletePathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::postal_codes::PostalCodes<E, Claims = C>
        + apis::ApiAuthBasic<Claims = C>
        + Send
        + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    // Authentication
    let claims_in_auth_header = api_impl
        .as_ref()
        .extract_claims_from_auth_header(apis::BasicAuthKind::Bearer, &headers, "authorization")
        .await;
    let claims = None.or(claims_in_auth_header);
    let Some(claims) = claims else {
        return response_with_status_code_only(StatusCode::UNAUTHORIZED);
    };

    #[allow(clippy::redundant_closure)]
    let validation =
        tokio::task::spawn_blocking(move || postal_codes_uuid_delete_validation(path_params))
            .await
            .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .postal_codes_uuid_delete(&method, &host, &cookies, &claims, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::postal_codes::PostalCodesUuidDeleteResponse::Status200_ResponseForOK(body) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn postal_codes_uuid_get_validation(
    path_params: models::PostalCodesUuidGetPathParams,
    query_params: models::PostalCodesUuidGetQueryParams,
) -> std::result::Result<
    (
        models::PostalCodesUuidGetPathParams,
        models::PostalCodesUuidGetQueryParams,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;

    Ok((path_params, query_params))
}
/// PostalCodesUuidGet - GET /postal_codes/{uuid}
#[tracing::instrument(skip_all)]
async fn postal_codes_uuid_get<I, A, E, C>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::PostalCodesUuidGetPathParams>,
    QueryExtra(query_params): QueryExtra<models::PostalCodesUuidGetQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::postal_codes::PostalCodes<E, Claims = C> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        postal_codes_uuid_get_validation(path_params, query_params)
    })
    .await
    .unwrap();

    let Ok((path_params, query_params)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .postal_codes_uuid_get(&method, &host, &cookies, &path_params, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::postal_codes::PostalCodesUuidGetResponse::Status200_ResponseForOK(body) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn postal_codes_uuid_head_validation(
    path_params: models::PostalCodesUuidHeadPathParams,
) -> std::result::Result<(models::PostalCodesUuidHeadPathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// PostalCodesUuidHead - HEAD /postal_codes/{uuid}
#[tracing::instrument(skip_all)]
async fn postal_codes_uuid_head<I, A, E, C>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::PostalCodesUuidHeadPathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::postal_codes::PostalCodes<E, Claims = C> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation =
        tokio::task::spawn_blocking(move || postal_codes_uuid_head_validation(path_params))
            .await
            .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .postal_codes_uuid_head(&method, &host, &cookies, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::postal_codes::PostalCodesUuidHeadResponse::Status200_DefaultHEADResponse => {
                let mut response = response.status(200);
                response.body(Body::empty())
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn postal_codes_uuid_name_delete_validation(
    path_params: models::PostalCodesUuidNameDeletePathParams,
) -> std::result::Result<(models::PostalCodesUuidNameDeletePathParams,), ValidationErrors> {
    path_params.validate()?;

    Ok((path_params,))
}
/// PostalCodesUuidNameDelete - DELETE /postal_codes/{uuid}/name
#[tracing::instrument(skip_all)]
async fn postal_codes_uuid_name_delete<I, A, E, C>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    headers: HeaderMap,
    Path(path_params): Path<models::PostalCodesUuidNameDeletePathParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::postal_codes::PostalCodes<E, Claims = C>
        + apis::ApiAuthBasic<Claims = C>
        + Send
        + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    // Authentication
    let claims_in_auth_header = api_impl
        .as_ref()
        .extract_claims_from_auth_header(apis::BasicAuthKind::Bearer, &headers, "authorization")
        .await;
    let claims = None.or(claims_in_auth_header);
    let Some(claims) = claims else {
        return response_with_status_code_only(StatusCode::UNAUTHORIZED);
    };

    #[allow(clippy::redundant_closure)]
    let validation =
        tokio::task::spawn_blocking(move || postal_codes_uuid_name_delete_validation(path_params))
            .await
            .unwrap();

    let Ok((path_params,)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .postal_codes_uuid_name_delete(&method, &host, &cookies, &claims, &path_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::postal_codes::PostalCodesUuidNameDeleteResponse::Status200_ResponseForOK(
                body,
            ) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[tracing::instrument(skip_all)]
fn postal_codes_uuid_name_get_validation(
    path_params: models::PostalCodesUuidNameGetPathParams,
    query_params: models::PostalCodesUuidNameGetQueryParams,
) -> std::result::Result<
    (
        models::PostalCodesUuidNameGetPathParams,
        models::PostalCodesUuidNameGetQueryParams,
    ),
    ValidationErrors,
> {
    path_params.validate()?;
    query_params.validate()?;

    Ok((path_params, query_params))
}
/// PostalCodesUuidNameGet - GET /postal_codes/{uuid}/name
#[tracing::instrument(skip_all)]
async fn postal_codes_uuid_name_get<I, A, E, C>(
    method: Method,
    host: Host,
    cookies: CookieJar,
    Path(path_params): Path<models::PostalCodesUuidNameGetPathParams>,
    QueryExtra(query_params): QueryExtra<models::PostalCodesUuidNameGetQueryParams>,
    State(api_impl): State<I>,
) -> Result<Response, StatusCode>
where
    I: AsRef<A> + Send + Sync,
    A: apis::postal_codes::PostalCodes<E, Claims = C> + Send + Sync,
    E: std::fmt::Debug + Send + Sync + 'static,
{
    #[allow(clippy::redundant_closure)]
    let validation = tokio::task::spawn_blocking(move || {
        postal_codes_uuid_name_get_validation(path_params, query_params)
    })
    .await
    .unwrap();

    let Ok((path_params, query_params)) = validation else {
        return Response::builder()
            .status(StatusCode::BAD_REQUEST)
            .body(Body::from(validation.unwrap_err().to_string()))
            .map_err(|_| StatusCode::BAD_REQUEST);
    };

    let result = api_impl
        .as_ref()
        .postal_codes_uuid_name_get(&method, &host, &cookies, &path_params, &query_params)
        .await;

    let mut response = Response::builder();

    let resp = match result {
        Ok(rsp) => match rsp {
            apis::postal_codes::PostalCodesUuidNameGetResponse::Status200_ResponseForOK(body) => {
                let mut response = response.status(200);
                {
                    let mut response_headers = response.headers_mut().unwrap();
                    response_headers
                        .insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
                }

                let body_content = tokio::task::spawn_blocking(move || {
                    serde_json::to_vec(&body).map_err(|e| {
                        error!(error = ?e);
                        StatusCode::INTERNAL_SERVER_ERROR
                    })
                })
                .await
                .unwrap()?;
                response.body(Body::from(body_content))
            }
        },
        Err(why) => {
            // Application code returned an error. This should not happen, as the implementation should
            // return a valid response.
            return api_impl
                .as_ref()
                .handle_error(&method, &host, &cookies, why)
                .await;
        }
    };

    resp.map_err(|e| {
        error!(error = ?e);
        StatusCode::INTERNAL_SERVER_ERROR
    })
}

#[allow(dead_code)]
#[inline]
fn response_with_status_code_only(code: StatusCode) -> Result<Response, StatusCode> {
    Response::builder()
        .status(code)
        .body(Body::empty())
        .map_err(|_| code)
}
