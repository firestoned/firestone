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
pub enum AddressbookAddressKeyAddrtypeDeleteResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyAddrtypeGetResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyAddrtypeHeadResponse {
    /// Default HEAD response
    Status200_DefaultHEADResponse,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyAddrtypePutResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
    /// One or more validation rules failed
    Status403_OneOrMoreValidationRulesFailed(models::ValidationProblem),
    /// One or more validation rules failed
    Status422_OneOrMoreValidationRulesFailed(models::ValidationProblem),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyCityDeleteResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyCityGetResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyCityHeadResponse {
    /// Default HEAD response
    Status200_DefaultHEADResponse,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyCityPutResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
    /// One or more validation rules failed
    Status403_OneOrMoreValidationRulesFailed(models::ValidationProblem),
    /// One or more validation rules failed
    Status422_OneOrMoreValidationRulesFailed(models::ValidationProblem),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyCountryDeleteResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyCountryGetResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyCountryHeadResponse {
    /// Default HEAD response
    Status200_DefaultHEADResponse,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyCountryPutResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
    /// One or more validation rules failed
    Status403_OneOrMoreValidationRulesFailed(models::ValidationProblem),
    /// One or more validation rules failed
    Status422_OneOrMoreValidationRulesFailed(models::ValidationProblem),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyDeleteResponse {
    /// Response for OK
    Status200_ResponseForOK(models::Addressbook),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyGetResponse {
    /// Response for OK
    Status200_ResponseForOK(models::Addressbook),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyHeadResponse {
    /// Default HEAD response
    Status200_DefaultHEADResponse,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyIsValidDeleteResponse {
    /// Response for OK
    Status200_ResponseForOK(bool),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyIsValidGetResponse {
    /// Response for OK
    Status200_ResponseForOK(bool),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyIsValidHeadResponse {
    /// Default HEAD response
    Status200_DefaultHEADResponse,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyIsValidPutResponse {
    /// Response for OK
    Status200_ResponseForOK(bool),
    /// One or more validation rules failed
    Status403_OneOrMoreValidationRulesFailed(models::ValidationProblem),
    /// One or more validation rules failed
    Status422_OneOrMoreValidationRulesFailed(models::ValidationProblem),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyPeopleDeleteResponse {
    /// Response for OK
    Status200_ResponseForOK(Vec<String>),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyPeopleGetResponse {
    /// Response for OK
    Status200_ResponseForOK(Vec<String>),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyPeopleHeadResponse {
    /// Default HEAD response
    Status200_DefaultHEADResponse,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyPeoplePutResponse {
    /// Response for OK
    Status200_ResponseForOK(Vec<String>),
    /// One or more validation rules failed
    Status403_OneOrMoreValidationRulesFailed(models::ValidationProblem),
    /// One or more validation rules failed
    Status422_OneOrMoreValidationRulesFailed(models::ValidationProblem),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyPersonDeleteResponse {
    /// Response for OK
    Status200_ResponseForOK(models::Person),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyPersonGetResponse {
    /// Response for OK
    Status200_ResponseForOK(Vec<models::Person>),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyPersonHeadResponse {
    /// Default HEAD response
    Status200_DefaultHEADResponse,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyPersonPatchResponse {
    /// Response for OK
    Status200_ResponseForOK(models::Person),
    /// One or more validation rules failed
    Status403_OneOrMoreValidationRulesFailed(models::ValidationProblem),
    /// One or more validation rules failed
    Status422_OneOrMoreValidationRulesFailed(models::ValidationProblem),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyPersonPostResponse {
    /// Response for CREATED
    Status201_ResponseForCREATED(models::CreatePerson),
    /// One or more validation rules failed
    Status422_OneOrMoreValidationRulesFailed(models::ValidationProblem),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyPutResponse {
    /// Response for OK
    Status200_ResponseForOK(models::UpdateAddressbook),
    /// One or more validation rules failed
    Status403_OneOrMoreValidationRulesFailed(models::ValidationProblem),
    /// One or more validation rules failed
    Status422_OneOrMoreValidationRulesFailed(models::ValidationProblem),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyStateDeleteResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyStateGetResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyStateHeadResponse {
    /// Default HEAD response
    Status200_DefaultHEADResponse,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyStatePutResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
    /// One or more validation rules failed
    Status403_OneOrMoreValidationRulesFailed(models::ValidationProblem),
    /// One or more validation rules failed
    Status422_OneOrMoreValidationRulesFailed(models::ValidationProblem),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyStreetDeleteResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyStreetGetResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyStreetHeadResponse {
    /// Default HEAD response
    Status200_DefaultHEADResponse,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookAddressKeyStreetPutResponse {
    /// Response for OK
    Status200_ResponseForOK(String),
    /// One or more validation rules failed
    Status403_OneOrMoreValidationRulesFailed(models::ValidationProblem),
    /// One or more validation rules failed
    Status422_OneOrMoreValidationRulesFailed(models::ValidationProblem),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookGetResponse {
    /// Response for OK
    Status200_ResponseForOK(Vec<models::Addressbook>),
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum AddressbookPostResponse {
    /// Response for CREATED
    Status201_ResponseForCREATED(models::CreateAddressbook),
    /// One or more validation rules failed
    Status422_OneOrMoreValidationRulesFailed(models::ValidationProblem),
}

/// Addressbook
#[async_trait]
#[allow(clippy::ptr_arg)]
pub trait Addressbook<E: std::fmt::Debug + Send + Sync + 'static = ()>:
    super::ErrorHandler<E>
{
    /// AddressbookAddressKeyAddrtypeDelete - DELETE /addressbook/{address_key}/addrtype
    async fn addressbook_address_key_addrtype_delete(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyAddrtypeDeletePathParams,
    ) -> Result<AddressbookAddressKeyAddrtypeDeleteResponse, E>;

    /// AddressbookAddressKeyAddrtypeGet - GET /addressbook/{address_key}/addrtype
    async fn addressbook_address_key_addrtype_get(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyAddrtypeGetPathParams,
        query_params: &models::AddressbookAddressKeyAddrtypeGetQueryParams,
    ) -> Result<AddressbookAddressKeyAddrtypeGetResponse, E>;

    /// AddressbookAddressKeyAddrtypeHead - HEAD /addressbook/{address_key}/addrtype
    async fn addressbook_address_key_addrtype_head(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyAddrtypeHeadPathParams,
    ) -> Result<AddressbookAddressKeyAddrtypeHeadResponse, E>;

    /// AddressbookAddressKeyAddrtypePut - PUT /addressbook/{address_key}/addrtype
    async fn addressbook_address_key_addrtype_put(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyAddrtypePutPathParams,
        body: &String,
    ) -> Result<AddressbookAddressKeyAddrtypePutResponse, E>;

    /// AddressbookAddressKeyCityDelete - DELETE /addressbook/{address_key}/city
    async fn addressbook_address_key_city_delete(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyCityDeletePathParams,
    ) -> Result<AddressbookAddressKeyCityDeleteResponse, E>;

    /// AddressbookAddressKeyCityGet - GET /addressbook/{address_key}/city
    async fn addressbook_address_key_city_get(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyCityGetPathParams,
        query_params: &models::AddressbookAddressKeyCityGetQueryParams,
    ) -> Result<AddressbookAddressKeyCityGetResponse, E>;

    /// AddressbookAddressKeyCityHead - HEAD /addressbook/{address_key}/city
    async fn addressbook_address_key_city_head(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyCityHeadPathParams,
    ) -> Result<AddressbookAddressKeyCityHeadResponse, E>;

    /// AddressbookAddressKeyCityPut - PUT /addressbook/{address_key}/city
    async fn addressbook_address_key_city_put(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyCityPutPathParams,
        body: &String,
    ) -> Result<AddressbookAddressKeyCityPutResponse, E>;

    /// AddressbookAddressKeyCountryDelete - DELETE /addressbook/{address_key}/country
    async fn addressbook_address_key_country_delete(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyCountryDeletePathParams,
    ) -> Result<AddressbookAddressKeyCountryDeleteResponse, E>;

    /// AddressbookAddressKeyCountryGet - GET /addressbook/{address_key}/country
    async fn addressbook_address_key_country_get(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyCountryGetPathParams,
        query_params: &models::AddressbookAddressKeyCountryGetQueryParams,
    ) -> Result<AddressbookAddressKeyCountryGetResponse, E>;

    /// AddressbookAddressKeyCountryHead - HEAD /addressbook/{address_key}/country
    async fn addressbook_address_key_country_head(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyCountryHeadPathParams,
    ) -> Result<AddressbookAddressKeyCountryHeadResponse, E>;

    /// AddressbookAddressKeyCountryPut - PUT /addressbook/{address_key}/country
    async fn addressbook_address_key_country_put(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyCountryPutPathParams,
        body: &String,
    ) -> Result<AddressbookAddressKeyCountryPutResponse, E>;

    /// AddressbookAddressKeyDelete - DELETE /addressbook/{address_key}
    async fn addressbook_address_key_delete(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyDeletePathParams,
    ) -> Result<AddressbookAddressKeyDeleteResponse, E>;

    /// AddressbookAddressKeyGet - GET /addressbook/{address_key}
    async fn addressbook_address_key_get(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyGetPathParams,
        query_params: &models::AddressbookAddressKeyGetQueryParams,
    ) -> Result<AddressbookAddressKeyGetResponse, E>;

    /// AddressbookAddressKeyHead - HEAD /addressbook/{address_key}
    async fn addressbook_address_key_head(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyHeadPathParams,
    ) -> Result<AddressbookAddressKeyHeadResponse, E>;

    /// AddressbookAddressKeyIsValidDelete - DELETE /addressbook/{address_key}/is_valid
    async fn addressbook_address_key_is_valid_delete(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyIsValidDeletePathParams,
    ) -> Result<AddressbookAddressKeyIsValidDeleteResponse, E>;

    /// AddressbookAddressKeyIsValidGet - GET /addressbook/{address_key}/is_valid
    async fn addressbook_address_key_is_valid_get(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyIsValidGetPathParams,
        query_params: &models::AddressbookAddressKeyIsValidGetQueryParams,
    ) -> Result<AddressbookAddressKeyIsValidGetResponse, E>;

    /// AddressbookAddressKeyIsValidHead - HEAD /addressbook/{address_key}/is_valid
    async fn addressbook_address_key_is_valid_head(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyIsValidHeadPathParams,
    ) -> Result<AddressbookAddressKeyIsValidHeadResponse, E>;

    /// AddressbookAddressKeyIsValidPut - PUT /addressbook/{address_key}/is_valid
    async fn addressbook_address_key_is_valid_put(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyIsValidPutPathParams,
        body: &bool,
    ) -> Result<AddressbookAddressKeyIsValidPutResponse, E>;

    /// AddressbookAddressKeyPeopleDelete - DELETE /addressbook/{address_key}/people
    async fn addressbook_address_key_people_delete(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyPeopleDeletePathParams,
    ) -> Result<AddressbookAddressKeyPeopleDeleteResponse, E>;

    /// AddressbookAddressKeyPeopleGet - GET /addressbook/{address_key}/people
    async fn addressbook_address_key_people_get(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyPeopleGetPathParams,
        query_params: &models::AddressbookAddressKeyPeopleGetQueryParams,
    ) -> Result<AddressbookAddressKeyPeopleGetResponse, E>;

    /// AddressbookAddressKeyPeopleHead - HEAD /addressbook/{address_key}/people
    async fn addressbook_address_key_people_head(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyPeopleHeadPathParams,
    ) -> Result<AddressbookAddressKeyPeopleHeadResponse, E>;

    /// AddressbookAddressKeyPeoplePut - PUT /addressbook/{address_key}/people
    async fn addressbook_address_key_people_put(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyPeoplePutPathParams,
        body: &Vec<String>,
    ) -> Result<AddressbookAddressKeyPeoplePutResponse, E>;

    /// AddressbookAddressKeyPersonDelete - DELETE /addressbook/{address_key}/person
    async fn addressbook_address_key_person_delete(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyPersonDeletePathParams,
        query_params: &models::AddressbookAddressKeyPersonDeleteQueryParams,
    ) -> Result<AddressbookAddressKeyPersonDeleteResponse, E>;

    /// AddressbookAddressKeyPersonGet - GET /addressbook/{address_key}/person
    async fn addressbook_address_key_person_get(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyPersonGetPathParams,
        query_params: &models::AddressbookAddressKeyPersonGetQueryParams,
    ) -> Result<AddressbookAddressKeyPersonGetResponse, E>;

    /// AddressbookAddressKeyPersonHead - HEAD /addressbook/{address_key}/person
    async fn addressbook_address_key_person_head(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyPersonHeadPathParams,
        query_params: &models::AddressbookAddressKeyPersonHeadQueryParams,
    ) -> Result<AddressbookAddressKeyPersonHeadResponse, E>;

    /// AddressbookAddressKeyPersonPatch - PATCH /addressbook/{address_key}/person
    async fn addressbook_address_key_person_patch(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyPersonPatchPathParams,
        query_params: &models::AddressbookAddressKeyPersonPatchQueryParams,
    ) -> Result<AddressbookAddressKeyPersonPatchResponse, E>;

    /// AddressbookAddressKeyPersonPost - POST /addressbook/{address_key}/person
    async fn addressbook_address_key_person_post(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyPersonPostPathParams,
        query_params: &models::AddressbookAddressKeyPersonPostQueryParams,
        body: &models::CreatePerson,
    ) -> Result<AddressbookAddressKeyPersonPostResponse, E>;

    /// AddressbookAddressKeyPut - PUT /addressbook/{address_key}
    async fn addressbook_address_key_put(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyPutPathParams,
        body: &models::UpdateAddressbook,
    ) -> Result<AddressbookAddressKeyPutResponse, E>;

    /// AddressbookAddressKeyStateDelete - DELETE /addressbook/{address_key}/state
    async fn addressbook_address_key_state_delete(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyStateDeletePathParams,
    ) -> Result<AddressbookAddressKeyStateDeleteResponse, E>;

    /// AddressbookAddressKeyStateGet - GET /addressbook/{address_key}/state
    async fn addressbook_address_key_state_get(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyStateGetPathParams,
        query_params: &models::AddressbookAddressKeyStateGetQueryParams,
    ) -> Result<AddressbookAddressKeyStateGetResponse, E>;

    /// AddressbookAddressKeyStateHead - HEAD /addressbook/{address_key}/state
    async fn addressbook_address_key_state_head(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyStateHeadPathParams,
    ) -> Result<AddressbookAddressKeyStateHeadResponse, E>;

    /// AddressbookAddressKeyStatePut - PUT /addressbook/{address_key}/state
    async fn addressbook_address_key_state_put(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyStatePutPathParams,
        body: &String,
    ) -> Result<AddressbookAddressKeyStatePutResponse, E>;

    /// AddressbookAddressKeyStreetDelete - DELETE /addressbook/{address_key}/street
    async fn addressbook_address_key_street_delete(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyStreetDeletePathParams,
    ) -> Result<AddressbookAddressKeyStreetDeleteResponse, E>;

    /// AddressbookAddressKeyStreetGet - GET /addressbook/{address_key}/street
    async fn addressbook_address_key_street_get(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyStreetGetPathParams,
        query_params: &models::AddressbookAddressKeyStreetGetQueryParams,
    ) -> Result<AddressbookAddressKeyStreetGetResponse, E>;

    /// AddressbookAddressKeyStreetHead - HEAD /addressbook/{address_key}/street
    async fn addressbook_address_key_street_head(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyStreetHeadPathParams,
    ) -> Result<AddressbookAddressKeyStreetHeadResponse, E>;

    /// AddressbookAddressKeyStreetPut - PUT /addressbook/{address_key}/street
    async fn addressbook_address_key_street_put(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        path_params: &models::AddressbookAddressKeyStreetPutPathParams,
        body: &String,
    ) -> Result<AddressbookAddressKeyStreetPutResponse, E>;

    /// AddressbookGet - GET /addressbook
    async fn addressbook_get(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        query_params: &models::AddressbookGetQueryParams,
    ) -> Result<AddressbookGetResponse, E>;

    /// AddressbookPost - POST /addressbook
    async fn addressbook_post(
        &self,

        method: &Method,
        host: &Host,
        cookies: &CookieJar,
        query_params: &models::AddressbookPostQueryParams,
        body: &models::CreateAddressbook,
    ) -> Result<AddressbookPostResponse, E>;
}
