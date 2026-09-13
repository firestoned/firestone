#![allow(unused_qualifications)]

use http::HeaderValue;
use validator::Validate;

#[cfg(feature = "server")]
use crate::header;
use crate::{models, types::*};

#[allow(dead_code)]
fn from_validation_error(e: validator::ValidationError) -> validator::ValidationErrors {
    let mut errs = validator::ValidationErrors::new();
    errs.add("na", e);
    errs
}

#[allow(dead_code)]
pub fn check_xss_string(v: &str) -> std::result::Result<(), validator::ValidationError> {
    if ammonia::is_html(v) {
        std::result::Result::Err(validator::ValidationError::new("xss detected"))
    } else {
        std::result::Result::Ok(())
    }
}

#[allow(dead_code)]
pub fn check_xss_vec_string(v: &[String]) -> std::result::Result<(), validator::ValidationError> {
    if v.iter().any(|i| ammonia::is_html(i)) {
        std::result::Result::Err(validator::ValidationError::new("xss detected"))
    } else {
        std::result::Result::Ok(())
    }
}

#[allow(dead_code)]
pub fn check_xss_map_string(
    v: &std::collections::HashMap<String, String>,
) -> std::result::Result<(), validator::ValidationError> {
    if v.keys().any(|k| ammonia::is_html(k)) || v.values().any(|v| ammonia::is_html(v)) {
        std::result::Result::Err(validator::ValidationError::new("xss detected"))
    } else {
        std::result::Result::Ok(())
    }
}

#[allow(dead_code)]
pub fn check_xss_map_nested<T>(
    v: &std::collections::HashMap<String, T>,
) -> std::result::Result<(), validator::ValidationError>
where
    T: validator::Validate,
{
    if v.keys().any(|k| ammonia::is_html(k)) || v.values().any(|v| v.validate().is_err()) {
        std::result::Result::Err(validator::ValidationError::new("xss detected"))
    } else {
        std::result::Result::Ok(())
    }
}

#[allow(dead_code)]
pub fn check_xss_map<T>(
    v: &std::collections::HashMap<String, T>,
) -> std::result::Result<(), validator::ValidationError> {
    if v.keys().any(|k| ammonia::is_html(k)) {
        std::result::Result::Err(validator::ValidationError::new("xss detected"))
    } else {
        std::result::Result::Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyAddrtypeDeletePathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyAddrtypeGetPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyAddrtypeGetQueryParams {
    /// Filter by city name
    #[serde(rename = "city")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub city: Option<String>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyAddrtypeHeadPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyAddrtypePutPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyCityDeletePathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyCityGetPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyCityGetQueryParams {
    /// Filter by city name
    #[serde(rename = "city")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub city: Option<String>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyCityHeadPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyCityPutPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyCountryDeletePathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyCountryGetPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyCountryGetQueryParams {
    /// Filter by city name
    #[serde(rename = "city")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub city: Option<String>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyCountryHeadPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyCountryPutPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyDeletePathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyGetPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyGetQueryParams {
    /// Filter by city name
    #[serde(rename = "city")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub city: Option<String>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyHeadPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyIsValidDeletePathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyIsValidGetPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyIsValidGetQueryParams {
    /// Filter by city name
    #[serde(rename = "city")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub city: Option<String>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyIsValidHeadPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyIsValidPutPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPeopleDeletePathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPeopleGetPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPeopleGetQueryParams {
    /// Filter by city name
    #[serde(rename = "city")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub city: Option<String>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPeopleHeadPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPeoplePutPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPersonDeletePathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPersonDeleteQueryParams {
    /// Limit the number of responses back
    #[serde(rename = "limit")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub limit: Option<i32>,
    /// The offset to start returning resources
    #[serde(rename = "offset")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offset: Option<i32>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPersonGetPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPersonGetQueryParams {
    /// Filter by last name
    #[serde(rename = "last_name")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub last_name: Option<String>,
    /// Limit the number of responses back
    #[serde(rename = "limit")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub limit: Option<i32>,
    /// The offset to start returning resources
    #[serde(rename = "offset")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offset: Option<i32>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPersonHeadPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPersonHeadQueryParams {
    /// Limit the number of responses back
    #[serde(rename = "limit")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub limit: Option<i32>,
    /// The offset to start returning resources
    #[serde(rename = "offset")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offset: Option<i32>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPersonPatchPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPersonPatchQueryParams {
    /// Limit the number of responses back
    #[serde(rename = "limit")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub limit: Option<i32>,
    /// The offset to start returning resources
    #[serde(rename = "offset")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offset: Option<i32>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPersonPostPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPersonPostQueryParams {
    /// Limit the number of responses back
    #[serde(rename = "limit")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub limit: Option<i32>,
    /// The offset to start returning resources
    #[serde(rename = "offset")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offset: Option<i32>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyPutPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyStateDeletePathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyStateGetPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyStateGetQueryParams {
    /// Filter by city name
    #[serde(rename = "city")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub city: Option<String>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyStateHeadPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyStatePutPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyStreetDeletePathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyStreetGetPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyStreetGetQueryParams {
    /// Filter by city name
    #[serde(rename = "city")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub city: Option<String>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyStreetHeadPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookAddressKeyStreetPutPathParams {
    pub address_key: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookGetQueryParams {
    /// Filter by city name
    #[serde(rename = "city")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub city: Option<String>,
    /// Limit the number of responses back
    #[serde(rename = "limit")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub limit: Option<i32>,
    /// The offset to start returning resources
    #[serde(rename = "offset")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offset: Option<i32>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct AddressbookPostQueryParams {
    /// Limit the number of responses back
    #[serde(rename = "limit")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub limit: Option<i32>,
    /// The offset to start returning resources
    #[serde(rename = "offset")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offset: Option<i32>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PersonsGetQueryParams {
    /// Filter by last name
    #[serde(rename = "last_name")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub last_name: Option<String>,
    /// Limit the number of responses back
    #[serde(rename = "limit")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub limit: Option<i32>,
    /// The offset to start returning resources
    #[serde(rename = "offset")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offset: Option<i32>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PersonsPostQueryParams {
    /// Limit the number of responses back
    #[serde(rename = "limit")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub limit: Option<i32>,
    /// The offset to start returning resources
    #[serde(rename = "offset")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offset: Option<i32>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PersonsUuidDeletePathParams {
    pub uuid: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PersonsUuidGetPathParams {
    pub uuid: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PersonsUuidGetQueryParams {
    /// Filter by last name
    #[serde(rename = "last_name")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub last_name: Option<String>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PersonsUuidHeadPathParams {
    pub uuid: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PersonsUuidPutPathParams {
    pub uuid: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PostalCodesGetQueryParams {
    /// Filter by name
    #[serde(rename = "name")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub name: Option<String>,
    /// Limit the number of responses back
    #[serde(rename = "limit")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub limit: Option<i32>,
    /// The offset to start returning resources
    #[serde(rename = "offset")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offset: Option<i32>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PostalCodesPostQueryParams {
    /// Limit the number of responses back
    #[serde(rename = "limit")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub limit: Option<i32>,
    /// The offset to start returning resources
    #[serde(rename = "offset")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offset: Option<i32>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PostalCodesUuidDeletePathParams {
    pub uuid: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PostalCodesUuidGetPathParams {
    pub uuid: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PostalCodesUuidGetQueryParams {
    /// Filter by name
    #[serde(rename = "name")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub name: Option<String>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PostalCodesUuidHeadPathParams {
    pub uuid: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PostalCodesUuidNameDeletePathParams {
    pub uuid: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PostalCodesUuidNameGetPathParams {
    pub uuid: String,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PostalCodesUuidNameGetQueryParams {
    /// Filter by name
    #[serde(rename = "name")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub name: Option<String>,
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct Addressbook {
    #[serde(rename = "address_key")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub address_key: Option<crate::types::Object>,

    /// The address type, e.g. work or home
    /// Note: inline enums are not fully supported by openapi-generator
    #[serde(rename = "addrtype")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub addrtype: Option<String>,

    /// The city of this address
    #[serde(rename = "city")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub city: Option<String>,

    /// The country of this address
    #[serde(rename = "country")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub country: Option<String>,

    /// Address is valid or not
    #[serde(rename = "is_valid")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub is_valid: Option<bool>,

    /// A list of people's names living there
    #[serde(rename = "people")]
    #[validate(custom(function = "check_xss_vec_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub people: Option<Vec<String>>,

    #[serde(rename = "person")]
    #[validate(nested)]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub person: Option<models::Person>,

    /// The state of this address
    #[serde(rename = "state")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub state: Option<String>,

    /// The street and civic number of this address
    #[serde(rename = "street")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub street: Option<String>,
}

impl Addressbook {
    #[allow(clippy::new_without_default, clippy::too_many_arguments)]
    pub fn new() -> Addressbook {
        Addressbook {
            address_key: None,
            addrtype: None,
            city: None,
            country: None,
            is_valid: None,
            people: None,
            person: None,
            state: None,
            street: None,
        }
    }
}

/// Converts the Addressbook value to the Query Parameters representation (style=form, explode=false)
/// specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde serializer
impl std::fmt::Display for Addressbook {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let params: Vec<Option<String>> = vec![
            // Skipping address_key in query parameter serialization
            self.addrtype
                .as_ref()
                .map(|addrtype| ["addrtype".to_string(), addrtype.to_string()].join(",")),
            self.city
                .as_ref()
                .map(|city| ["city".to_string(), city.to_string()].join(",")),
            self.country
                .as_ref()
                .map(|country| ["country".to_string(), country.to_string()].join(",")),
            self.is_valid
                .as_ref()
                .map(|is_valid| ["is_valid".to_string(), is_valid.to_string()].join(",")),
            self.people.as_ref().map(|people| {
                [
                    "people".to_string(),
                    people
                        .iter()
                        .map(|x| x.to_string())
                        .collect::<Vec<_>>()
                        .join(","),
                ]
                .join(",")
            }),
            // Skipping person in query parameter serialization
            self.state
                .as_ref()
                .map(|state| ["state".to_string(), state.to_string()].join(",")),
            self.street
                .as_ref()
                .map(|street| ["street".to_string(), street.to_string()].join(",")),
        ];

        write!(
            f,
            "{}",
            params.into_iter().flatten().collect::<Vec<_>>().join(",")
        )
    }
}

/// Converts Query Parameters representation (style=form, explode=false) to a Addressbook value
/// as specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde deserializer
impl std::str::FromStr for Addressbook {
    type Err = String;

    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        /// An intermediate representation of the struct to use for parsing.
        #[derive(Default)]
        #[allow(dead_code)]
        struct IntermediateRep {
            pub address_key: Vec<crate::types::Object>,
            pub addrtype: Vec<String>,
            pub city: Vec<String>,
            pub country: Vec<String>,
            pub is_valid: Vec<bool>,
            pub people: Vec<Vec<String>>,
            pub person: Vec<models::Person>,
            pub state: Vec<String>,
            pub street: Vec<String>,
        }

        let mut intermediate_rep = IntermediateRep::default();

        // Parse into intermediate representation
        let mut string_iter = s.split(',');
        let mut key_result = string_iter.next();

        while key_result.is_some() {
            let val = match string_iter.next() {
                Some(x) => x,
                None => {
                    return std::result::Result::Err(
                        "Missing value while parsing Addressbook".to_string(),
                    );
                }
            };

            if let Some(key) = key_result {
                #[allow(clippy::match_single_binding)]
                match key {
                    #[allow(clippy::redundant_clone)]
                    "address_key" => intermediate_rep.address_key.push(
                        <crate::types::Object as std::str::FromStr>::from_str(val)
                            .map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "addrtype" => intermediate_rep.addrtype.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "city" => intermediate_rep.city.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "country" => intermediate_rep.country.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "is_valid" => intermediate_rep.is_valid.push(
                        <bool as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    "people" => {
                        return std::result::Result::Err(
                            "Parsing a container in this style is not supported in Addressbook"
                                .to_string(),
                        );
                    }
                    #[allow(clippy::redundant_clone)]
                    "person" => intermediate_rep.person.push(
                        <models::Person as std::str::FromStr>::from_str(val)
                            .map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "state" => intermediate_rep.state.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "street" => intermediate_rep.street.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    _ => {
                        return std::result::Result::Err(
                            "Unexpected key while parsing Addressbook".to_string(),
                        );
                    }
                }
            }

            // Get the next key
            key_result = string_iter.next();
        }

        // Use the intermediate representation to return the struct
        std::result::Result::Ok(Addressbook {
            address_key: intermediate_rep.address_key.into_iter().next(),
            addrtype: intermediate_rep.addrtype.into_iter().next(),
            city: intermediate_rep.city.into_iter().next(),
            country: intermediate_rep.country.into_iter().next(),
            is_valid: intermediate_rep.is_valid.into_iter().next(),
            people: intermediate_rep.people.into_iter().next(),
            person: intermediate_rep.person.into_iter().next(),
            state: intermediate_rep.state.into_iter().next(),
            street: intermediate_rep.street.into_iter().next(),
        })
    }
}

// Methods for converting between header::IntoHeaderValue<Addressbook> and HeaderValue

#[cfg(feature = "server")]
impl std::convert::TryFrom<header::IntoHeaderValue<Addressbook>> for HeaderValue {
    type Error = String;

    fn try_from(
        hdr_value: header::IntoHeaderValue<Addressbook>,
    ) -> std::result::Result<Self, Self::Error> {
        let hdr_value = hdr_value.to_string();
        match HeaderValue::from_str(&hdr_value) {
            std::result::Result::Ok(value) => std::result::Result::Ok(value),
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Invalid header value for Addressbook - value: {hdr_value} is invalid {e}"#
            )),
        }
    }
}

#[cfg(feature = "server")]
impl std::convert::TryFrom<HeaderValue> for header::IntoHeaderValue<Addressbook> {
    type Error = String;

    fn try_from(hdr_value: HeaderValue) -> std::result::Result<Self, Self::Error> {
        match hdr_value.to_str() {
            std::result::Result::Ok(value) => {
                match <Addressbook as std::str::FromStr>::from_str(value) {
                    std::result::Result::Ok(value) => {
                        std::result::Result::Ok(header::IntoHeaderValue(value))
                    }
                    std::result::Result::Err(err) => std::result::Result::Err(format!(
                        r#"Unable to convert header value '{value}' into Addressbook - {err}"#
                    )),
                }
            }
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Unable to convert header: {hdr_value:?} to string: {e}"#
            )),
        }
    }
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct CreateAddressbook {
    #[serde(rename = "address_key")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub address_key: Option<crate::types::Object>,

    /// The address type, e.g. work or home
    /// Note: inline enums are not fully supported by openapi-generator
    #[serde(rename = "addrtype")]
    #[validate(custom(function = "check_xss_string"))]
    pub addrtype: String,

    /// The city of this address
    #[serde(rename = "city")]
    #[validate(custom(function = "check_xss_string"))]
    pub city: String,

    /// The country of this address
    #[serde(rename = "country")]
    #[validate(custom(function = "check_xss_string"))]
    pub country: String,

    /// Address is valid or not
    #[serde(rename = "is_valid")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub is_valid: Option<bool>,

    /// A list of people's names living there
    #[serde(rename = "people")]
    #[validate(custom(function = "check_xss_vec_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub people: Option<Vec<String>>,

    #[serde(rename = "person")]
    #[validate(nested)]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub person: Option<models::Person>,

    /// The state of this address
    #[serde(rename = "state")]
    #[validate(custom(function = "check_xss_string"))]
    pub state: String,

    /// The street and civic number of this address
    #[serde(rename = "street")]
    #[validate(custom(function = "check_xss_string"))]
    pub street: String,
}

impl CreateAddressbook {
    #[allow(clippy::new_without_default, clippy::too_many_arguments)]
    pub fn new(
        addrtype: String,
        city: String,
        country: String,
        state: String,
        street: String,
    ) -> CreateAddressbook {
        CreateAddressbook {
            address_key: None,
            addrtype,
            city,
            country,
            is_valid: None,
            people: None,
            person: None,
            state,
            street,
        }
    }
}

/// Converts the CreateAddressbook value to the Query Parameters representation (style=form, explode=false)
/// specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde serializer
impl std::fmt::Display for CreateAddressbook {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let params: Vec<Option<String>> = vec![
            // Skipping address_key in query parameter serialization
            Some("addrtype".to_string()),
            Some(self.addrtype.to_string()),
            Some("city".to_string()),
            Some(self.city.to_string()),
            Some("country".to_string()),
            Some(self.country.to_string()),
            self.is_valid
                .as_ref()
                .map(|is_valid| ["is_valid".to_string(), is_valid.to_string()].join(",")),
            self.people.as_ref().map(|people| {
                [
                    "people".to_string(),
                    people
                        .iter()
                        .map(|x| x.to_string())
                        .collect::<Vec<_>>()
                        .join(","),
                ]
                .join(",")
            }),
            // Skipping person in query parameter serialization
            Some("state".to_string()),
            Some(self.state.to_string()),
            Some("street".to_string()),
            Some(self.street.to_string()),
        ];

        write!(
            f,
            "{}",
            params.into_iter().flatten().collect::<Vec<_>>().join(",")
        )
    }
}

/// Converts Query Parameters representation (style=form, explode=false) to a CreateAddressbook value
/// as specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde deserializer
impl std::str::FromStr for CreateAddressbook {
    type Err = String;

    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        /// An intermediate representation of the struct to use for parsing.
        #[derive(Default)]
        #[allow(dead_code)]
        struct IntermediateRep {
            pub address_key: Vec<crate::types::Object>,
            pub addrtype: Vec<String>,
            pub city: Vec<String>,
            pub country: Vec<String>,
            pub is_valid: Vec<bool>,
            pub people: Vec<Vec<String>>,
            pub person: Vec<models::Person>,
            pub state: Vec<String>,
            pub street: Vec<String>,
        }

        let mut intermediate_rep = IntermediateRep::default();

        // Parse into intermediate representation
        let mut string_iter = s.split(',');
        let mut key_result = string_iter.next();

        while key_result.is_some() {
            let val = match string_iter.next() {
                Some(x) => x,
                None => {
                    return std::result::Result::Err(
                        "Missing value while parsing CreateAddressbook".to_string(),
                    );
                }
            };

            if let Some(key) = key_result {
                #[allow(clippy::match_single_binding)]
                match key {
                    #[allow(clippy::redundant_clone)]
                    "address_key" => intermediate_rep.address_key.push(
                        <crate::types::Object as std::str::FromStr>::from_str(val)
                            .map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "addrtype" => intermediate_rep.addrtype.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "city" => intermediate_rep.city.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "country" => intermediate_rep.country.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "is_valid" => intermediate_rep.is_valid.push(
                        <bool as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    "people" => return std::result::Result::Err(
                        "Parsing a container in this style is not supported in CreateAddressbook"
                            .to_string(),
                    ),
                    #[allow(clippy::redundant_clone)]
                    "person" => intermediate_rep.person.push(
                        <models::Person as std::str::FromStr>::from_str(val)
                            .map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "state" => intermediate_rep.state.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "street" => intermediate_rep.street.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    _ => {
                        return std::result::Result::Err(
                            "Unexpected key while parsing CreateAddressbook".to_string(),
                        );
                    }
                }
            }

            // Get the next key
            key_result = string_iter.next();
        }

        // Use the intermediate representation to return the struct
        std::result::Result::Ok(CreateAddressbook {
            address_key: intermediate_rep.address_key.into_iter().next(),
            addrtype: intermediate_rep
                .addrtype
                .into_iter()
                .next()
                .ok_or_else(|| "addrtype missing in CreateAddressbook".to_string())?,
            city: intermediate_rep
                .city
                .into_iter()
                .next()
                .ok_or_else(|| "city missing in CreateAddressbook".to_string())?,
            country: intermediate_rep
                .country
                .into_iter()
                .next()
                .ok_or_else(|| "country missing in CreateAddressbook".to_string())?,
            is_valid: intermediate_rep.is_valid.into_iter().next(),
            people: intermediate_rep.people.into_iter().next(),
            person: intermediate_rep.person.into_iter().next(),
            state: intermediate_rep
                .state
                .into_iter()
                .next()
                .ok_or_else(|| "state missing in CreateAddressbook".to_string())?,
            street: intermediate_rep
                .street
                .into_iter()
                .next()
                .ok_or_else(|| "street missing in CreateAddressbook".to_string())?,
        })
    }
}

// Methods for converting between header::IntoHeaderValue<CreateAddressbook> and HeaderValue

#[cfg(feature = "server")]
impl std::convert::TryFrom<header::IntoHeaderValue<CreateAddressbook>> for HeaderValue {
    type Error = String;

    fn try_from(
        hdr_value: header::IntoHeaderValue<CreateAddressbook>,
    ) -> std::result::Result<Self, Self::Error> {
        let hdr_value = hdr_value.to_string();
        match HeaderValue::from_str(&hdr_value) {
            std::result::Result::Ok(value) => std::result::Result::Ok(value),
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Invalid header value for CreateAddressbook - value: {hdr_value} is invalid {e}"#
            )),
        }
    }
}

#[cfg(feature = "server")]
impl std::convert::TryFrom<HeaderValue> for header::IntoHeaderValue<CreateAddressbook> {
    type Error = String;

    fn try_from(hdr_value: HeaderValue) -> std::result::Result<Self, Self::Error> {
        match hdr_value.to_str() {
            std::result::Result::Ok(value) => {
                match <CreateAddressbook as std::str::FromStr>::from_str(value) {
                    std::result::Result::Ok(value) => {
                        std::result::Result::Ok(header::IntoHeaderValue(value))
                    }
                    std::result::Result::Err(err) => std::result::Result::Err(format!(
                        r#"Unable to convert header value '{value}' into CreateAddressbook - {err}"#
                    )),
                }
            }
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Unable to convert header: {hdr_value:?} to string: {e}"#
            )),
        }
    }
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct CreatePerson {
    /// The person's age
    #[serde(rename = "age")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub age: Option<i32>,

    /// The person's first name
    #[serde(rename = "first_name")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub first_name: Option<String>,

    /// The person's hobbies
    #[serde(rename = "hobbies")]
    #[validate(custom(function = "check_xss_vec_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub hobbies: Option<Vec<String>>,

    /// The person's last name
    #[serde(rename = "last_name")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub last_name: Option<String>,

    /// The person's timezone (e.g. UTC, America/New_York)
    #[serde(rename = "timezone")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub timezone: Option<String>,

    #[serde(rename = "uuid")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub uuid: Option<crate::types::Object>,
}

impl CreatePerson {
    #[allow(clippy::new_without_default, clippy::too_many_arguments)]
    pub fn new() -> CreatePerson {
        CreatePerson {
            age: None,
            first_name: None,
            hobbies: None,
            last_name: None,
            timezone: Some(r#"UTC"#.to_string()),
            uuid: None,
        }
    }
}

/// Converts the CreatePerson value to the Query Parameters representation (style=form, explode=false)
/// specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde serializer
impl std::fmt::Display for CreatePerson {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let params: Vec<Option<String>> = vec![
            self.age
                .as_ref()
                .map(|age| ["age".to_string(), age.to_string()].join(",")),
            self.first_name
                .as_ref()
                .map(|first_name| ["first_name".to_string(), first_name.to_string()].join(",")),
            self.hobbies.as_ref().map(|hobbies| {
                [
                    "hobbies".to_string(),
                    hobbies
                        .iter()
                        .map(|x| x.to_string())
                        .collect::<Vec<_>>()
                        .join(","),
                ]
                .join(",")
            }),
            self.last_name
                .as_ref()
                .map(|last_name| ["last_name".to_string(), last_name.to_string()].join(",")),
            self.timezone
                .as_ref()
                .map(|timezone| ["timezone".to_string(), timezone.to_string()].join(",")),
            // Skipping uuid in query parameter serialization
        ];

        write!(
            f,
            "{}",
            params.into_iter().flatten().collect::<Vec<_>>().join(",")
        )
    }
}

/// Converts Query Parameters representation (style=form, explode=false) to a CreatePerson value
/// as specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde deserializer
impl std::str::FromStr for CreatePerson {
    type Err = String;

    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        /// An intermediate representation of the struct to use for parsing.
        #[derive(Default)]
        #[allow(dead_code)]
        struct IntermediateRep {
            pub age: Vec<i32>,
            pub first_name: Vec<String>,
            pub hobbies: Vec<Vec<String>>,
            pub last_name: Vec<String>,
            pub timezone: Vec<String>,
            pub uuid: Vec<crate::types::Object>,
        }

        let mut intermediate_rep = IntermediateRep::default();

        // Parse into intermediate representation
        let mut string_iter = s.split(',');
        let mut key_result = string_iter.next();

        while key_result.is_some() {
            let val = match string_iter.next() {
                Some(x) => x,
                None => {
                    return std::result::Result::Err(
                        "Missing value while parsing CreatePerson".to_string(),
                    );
                }
            };

            if let Some(key) = key_result {
                #[allow(clippy::match_single_binding)]
                match key {
                    #[allow(clippy::redundant_clone)]
                    "age" => intermediate_rep.age.push(
                        <i32 as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "first_name" => intermediate_rep.first_name.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    "hobbies" => {
                        return std::result::Result::Err(
                            "Parsing a container in this style is not supported in CreatePerson"
                                .to_string(),
                        );
                    }
                    #[allow(clippy::redundant_clone)]
                    "last_name" => intermediate_rep.last_name.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "timezone" => intermediate_rep.timezone.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "uuid" => intermediate_rep.uuid.push(
                        <crate::types::Object as std::str::FromStr>::from_str(val)
                            .map_err(|x| x.to_string())?,
                    ),
                    _ => {
                        return std::result::Result::Err(
                            "Unexpected key while parsing CreatePerson".to_string(),
                        );
                    }
                }
            }

            // Get the next key
            key_result = string_iter.next();
        }

        // Use the intermediate representation to return the struct
        std::result::Result::Ok(CreatePerson {
            age: intermediate_rep.age.into_iter().next(),
            first_name: intermediate_rep.first_name.into_iter().next(),
            hobbies: intermediate_rep.hobbies.into_iter().next(),
            last_name: intermediate_rep.last_name.into_iter().next(),
            timezone: intermediate_rep.timezone.into_iter().next(),
            uuid: intermediate_rep.uuid.into_iter().next(),
        })
    }
}

// Methods for converting between header::IntoHeaderValue<CreatePerson> and HeaderValue

#[cfg(feature = "server")]
impl std::convert::TryFrom<header::IntoHeaderValue<CreatePerson>> for HeaderValue {
    type Error = String;

    fn try_from(
        hdr_value: header::IntoHeaderValue<CreatePerson>,
    ) -> std::result::Result<Self, Self::Error> {
        let hdr_value = hdr_value.to_string();
        match HeaderValue::from_str(&hdr_value) {
            std::result::Result::Ok(value) => std::result::Result::Ok(value),
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Invalid header value for CreatePerson - value: {hdr_value} is invalid {e}"#
            )),
        }
    }
}

#[cfg(feature = "server")]
impl std::convert::TryFrom<HeaderValue> for header::IntoHeaderValue<CreatePerson> {
    type Error = String;

    fn try_from(hdr_value: HeaderValue) -> std::result::Result<Self, Self::Error> {
        match hdr_value.to_str() {
            std::result::Result::Ok(value) => {
                match <CreatePerson as std::str::FromStr>::from_str(value) {
                    std::result::Result::Ok(value) => {
                        std::result::Result::Ok(header::IntoHeaderValue(value))
                    }
                    std::result::Result::Err(err) => std::result::Result::Err(format!(
                        r#"Unable to convert header value '{value}' into CreatePerson - {err}"#
                    )),
                }
            }
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Unable to convert header: {hdr_value:?} to string: {e}"#
            )),
        }
    }
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct CreatePostalCode {
    /// The postal code's name/id
    #[serde(rename = "name")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub name: Option<String>,

    #[serde(rename = "uuid")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub uuid: Option<crate::types::Object>,
}

impl CreatePostalCode {
    #[allow(clippy::new_without_default, clippy::too_many_arguments)]
    pub fn new() -> CreatePostalCode {
        CreatePostalCode {
            name: None,
            uuid: None,
        }
    }
}

/// Converts the CreatePostalCode value to the Query Parameters representation (style=form, explode=false)
/// specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde serializer
impl std::fmt::Display for CreatePostalCode {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let params: Vec<Option<String>> = vec![
            self.name
                .as_ref()
                .map(|name| ["name".to_string(), name.to_string()].join(",")),
            // Skipping uuid in query parameter serialization
        ];

        write!(
            f,
            "{}",
            params.into_iter().flatten().collect::<Vec<_>>().join(",")
        )
    }
}

/// Converts Query Parameters representation (style=form, explode=false) to a CreatePostalCode value
/// as specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde deserializer
impl std::str::FromStr for CreatePostalCode {
    type Err = String;

    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        /// An intermediate representation of the struct to use for parsing.
        #[derive(Default)]
        #[allow(dead_code)]
        struct IntermediateRep {
            pub name: Vec<String>,
            pub uuid: Vec<crate::types::Object>,
        }

        let mut intermediate_rep = IntermediateRep::default();

        // Parse into intermediate representation
        let mut string_iter = s.split(',');
        let mut key_result = string_iter.next();

        while key_result.is_some() {
            let val = match string_iter.next() {
                Some(x) => x,
                None => {
                    return std::result::Result::Err(
                        "Missing value while parsing CreatePostalCode".to_string(),
                    );
                }
            };

            if let Some(key) = key_result {
                #[allow(clippy::match_single_binding)]
                match key {
                    #[allow(clippy::redundant_clone)]
                    "name" => intermediate_rep.name.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "uuid" => intermediate_rep.uuid.push(
                        <crate::types::Object as std::str::FromStr>::from_str(val)
                            .map_err(|x| x.to_string())?,
                    ),
                    _ => {
                        return std::result::Result::Err(
                            "Unexpected key while parsing CreatePostalCode".to_string(),
                        );
                    }
                }
            }

            // Get the next key
            key_result = string_iter.next();
        }

        // Use the intermediate representation to return the struct
        std::result::Result::Ok(CreatePostalCode {
            name: intermediate_rep.name.into_iter().next(),
            uuid: intermediate_rep.uuid.into_iter().next(),
        })
    }
}

// Methods for converting between header::IntoHeaderValue<CreatePostalCode> and HeaderValue

#[cfg(feature = "server")]
impl std::convert::TryFrom<header::IntoHeaderValue<CreatePostalCode>> for HeaderValue {
    type Error = String;

    fn try_from(
        hdr_value: header::IntoHeaderValue<CreatePostalCode>,
    ) -> std::result::Result<Self, Self::Error> {
        let hdr_value = hdr_value.to_string();
        match HeaderValue::from_str(&hdr_value) {
            std::result::Result::Ok(value) => std::result::Result::Ok(value),
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Invalid header value for CreatePostalCode - value: {hdr_value} is invalid {e}"#
            )),
        }
    }
}

#[cfg(feature = "server")]
impl std::convert::TryFrom<HeaderValue> for header::IntoHeaderValue<CreatePostalCode> {
    type Error = String;

    fn try_from(hdr_value: HeaderValue) -> std::result::Result<Self, Self::Error> {
        match hdr_value.to_str() {
            std::result::Result::Ok(value) => {
                match <CreatePostalCode as std::str::FromStr>::from_str(value) {
                    std::result::Result::Ok(value) => {
                        std::result::Result::Ok(header::IntoHeaderValue(value))
                    }
                    std::result::Result::Err(err) => std::result::Result::Err(format!(
                        r#"Unable to convert header value '{value}' into CreatePostalCode - {err}"#
                    )),
                }
            }
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Unable to convert header: {hdr_value:?} to string: {e}"#
            )),
        }
    }
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct Person {
    /// The person's age
    #[serde(rename = "age")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub age: Option<i32>,

    /// The person's first name
    #[serde(rename = "first_name")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub first_name: Option<String>,

    /// The person's hobbies
    #[serde(rename = "hobbies")]
    #[validate(custom(function = "check_xss_vec_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub hobbies: Option<Vec<String>>,

    /// The person's last name
    #[serde(rename = "last_name")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub last_name: Option<String>,

    /// The person's timezone (e.g. UTC, America/New_York)
    #[serde(rename = "timezone")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub timezone: Option<String>,

    #[serde(rename = "uuid")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub uuid: Option<crate::types::Object>,
}

impl Person {
    #[allow(clippy::new_without_default, clippy::too_many_arguments)]
    pub fn new() -> Person {
        Person {
            age: None,
            first_name: None,
            hobbies: None,
            last_name: None,
            timezone: Some(r#"UTC"#.to_string()),
            uuid: None,
        }
    }
}

/// Converts the Person value to the Query Parameters representation (style=form, explode=false)
/// specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde serializer
impl std::fmt::Display for Person {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let params: Vec<Option<String>> = vec![
            self.age
                .as_ref()
                .map(|age| ["age".to_string(), age.to_string()].join(",")),
            self.first_name
                .as_ref()
                .map(|first_name| ["first_name".to_string(), first_name.to_string()].join(",")),
            self.hobbies.as_ref().map(|hobbies| {
                [
                    "hobbies".to_string(),
                    hobbies
                        .iter()
                        .map(|x| x.to_string())
                        .collect::<Vec<_>>()
                        .join(","),
                ]
                .join(",")
            }),
            self.last_name
                .as_ref()
                .map(|last_name| ["last_name".to_string(), last_name.to_string()].join(",")),
            self.timezone
                .as_ref()
                .map(|timezone| ["timezone".to_string(), timezone.to_string()].join(",")),
            // Skipping uuid in query parameter serialization
        ];

        write!(
            f,
            "{}",
            params.into_iter().flatten().collect::<Vec<_>>().join(",")
        )
    }
}

/// Converts Query Parameters representation (style=form, explode=false) to a Person value
/// as specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde deserializer
impl std::str::FromStr for Person {
    type Err = String;

    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        /// An intermediate representation of the struct to use for parsing.
        #[derive(Default)]
        #[allow(dead_code)]
        struct IntermediateRep {
            pub age: Vec<i32>,
            pub first_name: Vec<String>,
            pub hobbies: Vec<Vec<String>>,
            pub last_name: Vec<String>,
            pub timezone: Vec<String>,
            pub uuid: Vec<crate::types::Object>,
        }

        let mut intermediate_rep = IntermediateRep::default();

        // Parse into intermediate representation
        let mut string_iter = s.split(',');
        let mut key_result = string_iter.next();

        while key_result.is_some() {
            let val = match string_iter.next() {
                Some(x) => x,
                None => {
                    return std::result::Result::Err(
                        "Missing value while parsing Person".to_string(),
                    );
                }
            };

            if let Some(key) = key_result {
                #[allow(clippy::match_single_binding)]
                match key {
                    #[allow(clippy::redundant_clone)]
                    "age" => intermediate_rep.age.push(
                        <i32 as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "first_name" => intermediate_rep.first_name.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    "hobbies" => {
                        return std::result::Result::Err(
                            "Parsing a container in this style is not supported in Person"
                                .to_string(),
                        );
                    }
                    #[allow(clippy::redundant_clone)]
                    "last_name" => intermediate_rep.last_name.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "timezone" => intermediate_rep.timezone.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "uuid" => intermediate_rep.uuid.push(
                        <crate::types::Object as std::str::FromStr>::from_str(val)
                            .map_err(|x| x.to_string())?,
                    ),
                    _ => {
                        return std::result::Result::Err(
                            "Unexpected key while parsing Person".to_string(),
                        );
                    }
                }
            }

            // Get the next key
            key_result = string_iter.next();
        }

        // Use the intermediate representation to return the struct
        std::result::Result::Ok(Person {
            age: intermediate_rep.age.into_iter().next(),
            first_name: intermediate_rep.first_name.into_iter().next(),
            hobbies: intermediate_rep.hobbies.into_iter().next(),
            last_name: intermediate_rep.last_name.into_iter().next(),
            timezone: intermediate_rep.timezone.into_iter().next(),
            uuid: intermediate_rep.uuid.into_iter().next(),
        })
    }
}

// Methods for converting between header::IntoHeaderValue<Person> and HeaderValue

#[cfg(feature = "server")]
impl std::convert::TryFrom<header::IntoHeaderValue<Person>> for HeaderValue {
    type Error = String;

    fn try_from(
        hdr_value: header::IntoHeaderValue<Person>,
    ) -> std::result::Result<Self, Self::Error> {
        let hdr_value = hdr_value.to_string();
        match HeaderValue::from_str(&hdr_value) {
            std::result::Result::Ok(value) => std::result::Result::Ok(value),
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Invalid header value for Person - value: {hdr_value} is invalid {e}"#
            )),
        }
    }
}

#[cfg(feature = "server")]
impl std::convert::TryFrom<HeaderValue> for header::IntoHeaderValue<Person> {
    type Error = String;

    fn try_from(hdr_value: HeaderValue) -> std::result::Result<Self, Self::Error> {
        match hdr_value.to_str() {
            std::result::Result::Ok(value) => {
                match <Person as std::str::FromStr>::from_str(value) {
                    std::result::Result::Ok(value) => {
                        std::result::Result::Ok(header::IntoHeaderValue(value))
                    }
                    std::result::Result::Err(err) => std::result::Result::Err(format!(
                        r#"Unable to convert header value '{value}' into Person - {err}"#
                    )),
                }
            }
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Unable to convert header: {hdr_value:?} to string: {e}"#
            )),
        }
    }
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct PostalCode {
    /// The postal code's name/id
    #[serde(rename = "name")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub name: Option<String>,

    #[serde(rename = "uuid")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub uuid: Option<crate::types::Object>,
}

impl PostalCode {
    #[allow(clippy::new_without_default, clippy::too_many_arguments)]
    pub fn new() -> PostalCode {
        PostalCode {
            name: None,
            uuid: None,
        }
    }
}

/// Converts the PostalCode value to the Query Parameters representation (style=form, explode=false)
/// specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde serializer
impl std::fmt::Display for PostalCode {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let params: Vec<Option<String>> = vec![
            self.name
                .as_ref()
                .map(|name| ["name".to_string(), name.to_string()].join(",")),
            // Skipping uuid in query parameter serialization
        ];

        write!(
            f,
            "{}",
            params.into_iter().flatten().collect::<Vec<_>>().join(",")
        )
    }
}

/// Converts Query Parameters representation (style=form, explode=false) to a PostalCode value
/// as specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde deserializer
impl std::str::FromStr for PostalCode {
    type Err = String;

    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        /// An intermediate representation of the struct to use for parsing.
        #[derive(Default)]
        #[allow(dead_code)]
        struct IntermediateRep {
            pub name: Vec<String>,
            pub uuid: Vec<crate::types::Object>,
        }

        let mut intermediate_rep = IntermediateRep::default();

        // Parse into intermediate representation
        let mut string_iter = s.split(',');
        let mut key_result = string_iter.next();

        while key_result.is_some() {
            let val = match string_iter.next() {
                Some(x) => x,
                None => {
                    return std::result::Result::Err(
                        "Missing value while parsing PostalCode".to_string(),
                    );
                }
            };

            if let Some(key) = key_result {
                #[allow(clippy::match_single_binding)]
                match key {
                    #[allow(clippy::redundant_clone)]
                    "name" => intermediate_rep.name.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "uuid" => intermediate_rep.uuid.push(
                        <crate::types::Object as std::str::FromStr>::from_str(val)
                            .map_err(|x| x.to_string())?,
                    ),
                    _ => {
                        return std::result::Result::Err(
                            "Unexpected key while parsing PostalCode".to_string(),
                        );
                    }
                }
            }

            // Get the next key
            key_result = string_iter.next();
        }

        // Use the intermediate representation to return the struct
        std::result::Result::Ok(PostalCode {
            name: intermediate_rep.name.into_iter().next(),
            uuid: intermediate_rep.uuid.into_iter().next(),
        })
    }
}

// Methods for converting between header::IntoHeaderValue<PostalCode> and HeaderValue

#[cfg(feature = "server")]
impl std::convert::TryFrom<header::IntoHeaderValue<PostalCode>> for HeaderValue {
    type Error = String;

    fn try_from(
        hdr_value: header::IntoHeaderValue<PostalCode>,
    ) -> std::result::Result<Self, Self::Error> {
        let hdr_value = hdr_value.to_string();
        match HeaderValue::from_str(&hdr_value) {
            std::result::Result::Ok(value) => std::result::Result::Ok(value),
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Invalid header value for PostalCode - value: {hdr_value} is invalid {e}"#
            )),
        }
    }
}

#[cfg(feature = "server")]
impl std::convert::TryFrom<HeaderValue> for header::IntoHeaderValue<PostalCode> {
    type Error = String;

    fn try_from(hdr_value: HeaderValue) -> std::result::Result<Self, Self::Error> {
        match hdr_value.to_str() {
            std::result::Result::Ok(value) => {
                match <PostalCode as std::str::FromStr>::from_str(value) {
                    std::result::Result::Ok(value) => {
                        std::result::Result::Ok(header::IntoHeaderValue(value))
                    }
                    std::result::Result::Err(err) => std::result::Result::Err(format!(
                        r#"Unable to convert header value '{value}' into PostalCode - {err}"#
                    )),
                }
            }
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Unable to convert header: {hdr_value:?} to string: {e}"#
            )),
        }
    }
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct UpdateAddressbook {
    #[serde(rename = "address_key")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub address_key: Option<crate::types::Object>,

    /// The address type, e.g. work or home
    /// Note: inline enums are not fully supported by openapi-generator
    #[serde(rename = "addrtype")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub addrtype: Option<String>,

    /// The city of this address
    #[serde(rename = "city")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub city: Option<String>,

    /// The country of this address
    #[serde(rename = "country")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub country: Option<String>,

    /// Address is valid or not
    #[serde(rename = "is_valid")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub is_valid: Option<bool>,

    /// A list of people's names living there
    #[serde(rename = "people")]
    #[validate(custom(function = "check_xss_vec_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub people: Option<Vec<String>>,

    #[serde(rename = "person")]
    #[validate(nested)]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub person: Option<models::Person>,

    /// The state of this address
    #[serde(rename = "state")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub state: Option<String>,

    /// The street and civic number of this address
    #[serde(rename = "street")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub street: Option<String>,
}

impl UpdateAddressbook {
    #[allow(clippy::new_without_default, clippy::too_many_arguments)]
    pub fn new() -> UpdateAddressbook {
        UpdateAddressbook {
            address_key: None,
            addrtype: None,
            city: None,
            country: None,
            is_valid: None,
            people: None,
            person: None,
            state: None,
            street: None,
        }
    }
}

/// Converts the UpdateAddressbook value to the Query Parameters representation (style=form, explode=false)
/// specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde serializer
impl std::fmt::Display for UpdateAddressbook {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let params: Vec<Option<String>> = vec![
            // Skipping address_key in query parameter serialization
            self.addrtype
                .as_ref()
                .map(|addrtype| ["addrtype".to_string(), addrtype.to_string()].join(",")),
            self.city
                .as_ref()
                .map(|city| ["city".to_string(), city.to_string()].join(",")),
            self.country
                .as_ref()
                .map(|country| ["country".to_string(), country.to_string()].join(",")),
            self.is_valid
                .as_ref()
                .map(|is_valid| ["is_valid".to_string(), is_valid.to_string()].join(",")),
            self.people.as_ref().map(|people| {
                [
                    "people".to_string(),
                    people
                        .iter()
                        .map(|x| x.to_string())
                        .collect::<Vec<_>>()
                        .join(","),
                ]
                .join(",")
            }),
            // Skipping person in query parameter serialization
            self.state
                .as_ref()
                .map(|state| ["state".to_string(), state.to_string()].join(",")),
            self.street
                .as_ref()
                .map(|street| ["street".to_string(), street.to_string()].join(",")),
        ];

        write!(
            f,
            "{}",
            params.into_iter().flatten().collect::<Vec<_>>().join(",")
        )
    }
}

/// Converts Query Parameters representation (style=form, explode=false) to a UpdateAddressbook value
/// as specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde deserializer
impl std::str::FromStr for UpdateAddressbook {
    type Err = String;

    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        /// An intermediate representation of the struct to use for parsing.
        #[derive(Default)]
        #[allow(dead_code)]
        struct IntermediateRep {
            pub address_key: Vec<crate::types::Object>,
            pub addrtype: Vec<String>,
            pub city: Vec<String>,
            pub country: Vec<String>,
            pub is_valid: Vec<bool>,
            pub people: Vec<Vec<String>>,
            pub person: Vec<models::Person>,
            pub state: Vec<String>,
            pub street: Vec<String>,
        }

        let mut intermediate_rep = IntermediateRep::default();

        // Parse into intermediate representation
        let mut string_iter = s.split(',');
        let mut key_result = string_iter.next();

        while key_result.is_some() {
            let val = match string_iter.next() {
                Some(x) => x,
                None => {
                    return std::result::Result::Err(
                        "Missing value while parsing UpdateAddressbook".to_string(),
                    );
                }
            };

            if let Some(key) = key_result {
                #[allow(clippy::match_single_binding)]
                match key {
                    #[allow(clippy::redundant_clone)]
                    "address_key" => intermediate_rep.address_key.push(
                        <crate::types::Object as std::str::FromStr>::from_str(val)
                            .map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "addrtype" => intermediate_rep.addrtype.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "city" => intermediate_rep.city.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "country" => intermediate_rep.country.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "is_valid" => intermediate_rep.is_valid.push(
                        <bool as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    "people" => return std::result::Result::Err(
                        "Parsing a container in this style is not supported in UpdateAddressbook"
                            .to_string(),
                    ),
                    #[allow(clippy::redundant_clone)]
                    "person" => intermediate_rep.person.push(
                        <models::Person as std::str::FromStr>::from_str(val)
                            .map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "state" => intermediate_rep.state.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "street" => intermediate_rep.street.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    _ => {
                        return std::result::Result::Err(
                            "Unexpected key while parsing UpdateAddressbook".to_string(),
                        );
                    }
                }
            }

            // Get the next key
            key_result = string_iter.next();
        }

        // Use the intermediate representation to return the struct
        std::result::Result::Ok(UpdateAddressbook {
            address_key: intermediate_rep.address_key.into_iter().next(),
            addrtype: intermediate_rep.addrtype.into_iter().next(),
            city: intermediate_rep.city.into_iter().next(),
            country: intermediate_rep.country.into_iter().next(),
            is_valid: intermediate_rep.is_valid.into_iter().next(),
            people: intermediate_rep.people.into_iter().next(),
            person: intermediate_rep.person.into_iter().next(),
            state: intermediate_rep.state.into_iter().next(),
            street: intermediate_rep.street.into_iter().next(),
        })
    }
}

// Methods for converting between header::IntoHeaderValue<UpdateAddressbook> and HeaderValue

#[cfg(feature = "server")]
impl std::convert::TryFrom<header::IntoHeaderValue<UpdateAddressbook>> for HeaderValue {
    type Error = String;

    fn try_from(
        hdr_value: header::IntoHeaderValue<UpdateAddressbook>,
    ) -> std::result::Result<Self, Self::Error> {
        let hdr_value = hdr_value.to_string();
        match HeaderValue::from_str(&hdr_value) {
            std::result::Result::Ok(value) => std::result::Result::Ok(value),
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Invalid header value for UpdateAddressbook - value: {hdr_value} is invalid {e}"#
            )),
        }
    }
}

#[cfg(feature = "server")]
impl std::convert::TryFrom<HeaderValue> for header::IntoHeaderValue<UpdateAddressbook> {
    type Error = String;

    fn try_from(hdr_value: HeaderValue) -> std::result::Result<Self, Self::Error> {
        match hdr_value.to_str() {
            std::result::Result::Ok(value) => {
                match <UpdateAddressbook as std::str::FromStr>::from_str(value) {
                    std::result::Result::Ok(value) => {
                        std::result::Result::Ok(header::IntoHeaderValue(value))
                    }
                    std::result::Result::Err(err) => std::result::Result::Err(format!(
                        r#"Unable to convert header value '{value}' into UpdateAddressbook - {err}"#
                    )),
                }
            }
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Unable to convert header: {hdr_value:?} to string: {e}"#
            )),
        }
    }
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct UpdatePerson {
    /// The person's age
    #[serde(rename = "age")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub age: Option<i32>,

    /// The person's first name
    #[serde(rename = "first_name")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub first_name: Option<String>,

    /// The person's hobbies
    #[serde(rename = "hobbies")]
    #[validate(custom(function = "check_xss_vec_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub hobbies: Option<Vec<String>>,

    /// The person's last name
    #[serde(rename = "last_name")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub last_name: Option<String>,

    /// The person's timezone (e.g. UTC, America/New_York)
    #[serde(rename = "timezone")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub timezone: Option<String>,

    #[serde(rename = "uuid")]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub uuid: Option<crate::types::Object>,
}

impl UpdatePerson {
    #[allow(clippy::new_without_default, clippy::too_many_arguments)]
    pub fn new() -> UpdatePerson {
        UpdatePerson {
            age: None,
            first_name: None,
            hobbies: None,
            last_name: None,
            timezone: Some(r#"UTC"#.to_string()),
            uuid: None,
        }
    }
}

/// Converts the UpdatePerson value to the Query Parameters representation (style=form, explode=false)
/// specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde serializer
impl std::fmt::Display for UpdatePerson {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let params: Vec<Option<String>> = vec![
            self.age
                .as_ref()
                .map(|age| ["age".to_string(), age.to_string()].join(",")),
            self.first_name
                .as_ref()
                .map(|first_name| ["first_name".to_string(), first_name.to_string()].join(",")),
            self.hobbies.as_ref().map(|hobbies| {
                [
                    "hobbies".to_string(),
                    hobbies
                        .iter()
                        .map(|x| x.to_string())
                        .collect::<Vec<_>>()
                        .join(","),
                ]
                .join(",")
            }),
            self.last_name
                .as_ref()
                .map(|last_name| ["last_name".to_string(), last_name.to_string()].join(",")),
            self.timezone
                .as_ref()
                .map(|timezone| ["timezone".to_string(), timezone.to_string()].join(",")),
            // Skipping uuid in query parameter serialization
        ];

        write!(
            f,
            "{}",
            params.into_iter().flatten().collect::<Vec<_>>().join(",")
        )
    }
}

/// Converts Query Parameters representation (style=form, explode=false) to a UpdatePerson value
/// as specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde deserializer
impl std::str::FromStr for UpdatePerson {
    type Err = String;

    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        /// An intermediate representation of the struct to use for parsing.
        #[derive(Default)]
        #[allow(dead_code)]
        struct IntermediateRep {
            pub age: Vec<i32>,
            pub first_name: Vec<String>,
            pub hobbies: Vec<Vec<String>>,
            pub last_name: Vec<String>,
            pub timezone: Vec<String>,
            pub uuid: Vec<crate::types::Object>,
        }

        let mut intermediate_rep = IntermediateRep::default();

        // Parse into intermediate representation
        let mut string_iter = s.split(',');
        let mut key_result = string_iter.next();

        while key_result.is_some() {
            let val = match string_iter.next() {
                Some(x) => x,
                None => {
                    return std::result::Result::Err(
                        "Missing value while parsing UpdatePerson".to_string(),
                    );
                }
            };

            if let Some(key) = key_result {
                #[allow(clippy::match_single_binding)]
                match key {
                    #[allow(clippy::redundant_clone)]
                    "age" => intermediate_rep.age.push(
                        <i32 as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "first_name" => intermediate_rep.first_name.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    "hobbies" => {
                        return std::result::Result::Err(
                            "Parsing a container in this style is not supported in UpdatePerson"
                                .to_string(),
                        );
                    }
                    #[allow(clippy::redundant_clone)]
                    "last_name" => intermediate_rep.last_name.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "timezone" => intermediate_rep.timezone.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "uuid" => intermediate_rep.uuid.push(
                        <crate::types::Object as std::str::FromStr>::from_str(val)
                            .map_err(|x| x.to_string())?,
                    ),
                    _ => {
                        return std::result::Result::Err(
                            "Unexpected key while parsing UpdatePerson".to_string(),
                        );
                    }
                }
            }

            // Get the next key
            key_result = string_iter.next();
        }

        // Use the intermediate representation to return the struct
        std::result::Result::Ok(UpdatePerson {
            age: intermediate_rep.age.into_iter().next(),
            first_name: intermediate_rep.first_name.into_iter().next(),
            hobbies: intermediate_rep.hobbies.into_iter().next(),
            last_name: intermediate_rep.last_name.into_iter().next(),
            timezone: intermediate_rep.timezone.into_iter().next(),
            uuid: intermediate_rep.uuid.into_iter().next(),
        })
    }
}

// Methods for converting between header::IntoHeaderValue<UpdatePerson> and HeaderValue

#[cfg(feature = "server")]
impl std::convert::TryFrom<header::IntoHeaderValue<UpdatePerson>> for HeaderValue {
    type Error = String;

    fn try_from(
        hdr_value: header::IntoHeaderValue<UpdatePerson>,
    ) -> std::result::Result<Self, Self::Error> {
        let hdr_value = hdr_value.to_string();
        match HeaderValue::from_str(&hdr_value) {
            std::result::Result::Ok(value) => std::result::Result::Ok(value),
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Invalid header value for UpdatePerson - value: {hdr_value} is invalid {e}"#
            )),
        }
    }
}

#[cfg(feature = "server")]
impl std::convert::TryFrom<HeaderValue> for header::IntoHeaderValue<UpdatePerson> {
    type Error = String;

    fn try_from(hdr_value: HeaderValue) -> std::result::Result<Self, Self::Error> {
        match hdr_value.to_str() {
            std::result::Result::Ok(value) => {
                match <UpdatePerson as std::str::FromStr>::from_str(value) {
                    std::result::Result::Ok(value) => {
                        std::result::Result::Ok(header::IntoHeaderValue(value))
                    }
                    std::result::Result::Err(err) => std::result::Result::Err(format!(
                        r#"Unable to convert header value '{value}' into UpdatePerson - {err}"#
                    )),
                }
            }
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Unable to convert header: {hdr_value:?} to string: {e}"#
            )),
        }
    }
}

/// An RFC 9457 problem detail, returned when one or more validation rules fail.
#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct ValidationProblem {
    /// The first violation's message.
    #[serde(rename = "detail")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub detail: Option<String>,

    /// The HTTP status code.
    #[serde(rename = "status")]
    pub status: i32,

    /// A short summary of the problem.
    #[serde(rename = "title")]
    #[validate(custom(function = "check_xss_string"))]
    pub title: String,

    #[serde(rename = "type")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub r_type: Option<String>,

    /// Every rule that failed for this request.
    #[serde(rename = "violations")]
    #[validate(nested)]
    pub violations: Vec<models::ValidationProblemViolationsInner>,
}

impl ValidationProblem {
    #[allow(clippy::new_without_default, clippy::too_many_arguments)]
    pub fn new(
        status: i32,
        title: String,
        violations: Vec<models::ValidationProblemViolationsInner>,
    ) -> ValidationProblem {
        ValidationProblem {
            detail: None,
            status,
            title,
            r_type: Some(r#"about:blank"#.to_string()),
            violations,
        }
    }
}

/// Converts the ValidationProblem value to the Query Parameters representation (style=form, explode=false)
/// specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde serializer
impl std::fmt::Display for ValidationProblem {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let params: Vec<Option<String>> = vec![
            self.detail
                .as_ref()
                .map(|detail| ["detail".to_string(), detail.to_string()].join(",")),
            Some("status".to_string()),
            Some(self.status.to_string()),
            Some("title".to_string()),
            Some(self.title.to_string()),
            self.r_type
                .as_ref()
                .map(|r_type| ["type".to_string(), r_type.to_string()].join(",")),
            // Skipping violations in query parameter serialization
        ];

        write!(
            f,
            "{}",
            params.into_iter().flatten().collect::<Vec<_>>().join(",")
        )
    }
}

/// Converts Query Parameters representation (style=form, explode=false) to a ValidationProblem value
/// as specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde deserializer
impl std::str::FromStr for ValidationProblem {
    type Err = String;

    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        /// An intermediate representation of the struct to use for parsing.
        #[derive(Default)]
        #[allow(dead_code)]
        struct IntermediateRep {
            pub detail: Vec<String>,
            pub status: Vec<i32>,
            pub title: Vec<String>,
            pub r_type: Vec<String>,
            pub violations: Vec<Vec<models::ValidationProblemViolationsInner>>,
        }

        let mut intermediate_rep = IntermediateRep::default();

        // Parse into intermediate representation
        let mut string_iter = s.split(',');
        let mut key_result = string_iter.next();

        while key_result.is_some() {
            let val = match string_iter.next() {
                Some(x) => x,
                None => {
                    return std::result::Result::Err(
                        "Missing value while parsing ValidationProblem".to_string(),
                    );
                }
            };

            if let Some(key) = key_result {
                #[allow(clippy::match_single_binding)]
                match key {
                    #[allow(clippy::redundant_clone)]
                    "detail" => intermediate_rep.detail.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "status" => intermediate_rep.status.push(
                        <i32 as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "title" => intermediate_rep.title.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "type" => intermediate_rep.r_type.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    "violations" => return std::result::Result::Err(
                        "Parsing a container in this style is not supported in ValidationProblem"
                            .to_string(),
                    ),
                    _ => {
                        return std::result::Result::Err(
                            "Unexpected key while parsing ValidationProblem".to_string(),
                        );
                    }
                }
            }

            // Get the next key
            key_result = string_iter.next();
        }

        // Use the intermediate representation to return the struct
        std::result::Result::Ok(ValidationProblem {
            detail: intermediate_rep.detail.into_iter().next(),
            status: intermediate_rep
                .status
                .into_iter()
                .next()
                .ok_or_else(|| "status missing in ValidationProblem".to_string())?,
            title: intermediate_rep
                .title
                .into_iter()
                .next()
                .ok_or_else(|| "title missing in ValidationProblem".to_string())?,
            r_type: intermediate_rep.r_type.into_iter().next(),
            violations: intermediate_rep
                .violations
                .into_iter()
                .next()
                .ok_or_else(|| "violations missing in ValidationProblem".to_string())?,
        })
    }
}

// Methods for converting between header::IntoHeaderValue<ValidationProblem> and HeaderValue

#[cfg(feature = "server")]
impl std::convert::TryFrom<header::IntoHeaderValue<ValidationProblem>> for HeaderValue {
    type Error = String;

    fn try_from(
        hdr_value: header::IntoHeaderValue<ValidationProblem>,
    ) -> std::result::Result<Self, Self::Error> {
        let hdr_value = hdr_value.to_string();
        match HeaderValue::from_str(&hdr_value) {
            std::result::Result::Ok(value) => std::result::Result::Ok(value),
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Invalid header value for ValidationProblem - value: {hdr_value} is invalid {e}"#
            )),
        }
    }
}

#[cfg(feature = "server")]
impl std::convert::TryFrom<HeaderValue> for header::IntoHeaderValue<ValidationProblem> {
    type Error = String;

    fn try_from(hdr_value: HeaderValue) -> std::result::Result<Self, Self::Error> {
        match hdr_value.to_str() {
            std::result::Result::Ok(value) => {
                match <ValidationProblem as std::str::FromStr>::from_str(value) {
                    std::result::Result::Ok(value) => {
                        std::result::Result::Ok(header::IntoHeaderValue(value))
                    }
                    std::result::Result::Err(err) => std::result::Result::Err(format!(
                        r#"Unable to convert header value '{value}' into ValidationProblem - {err}"#
                    )),
                }
            }
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Unable to convert header: {hdr_value:?} to string: {e}"#
            )),
        }
    }
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize, validator::Validate)]
#[cfg_attr(feature = "conversion", derive(frunk::LabelledGeneric))]
pub struct ValidationProblemViolationsInner {
    /// The field the rule applies to, if any.
    #[serde(rename = "field")]
    #[validate(custom(function = "check_xss_string"))]
    #[serde(skip_serializing_if = "Option::is_none")]
    pub field: Option<String>,

    /// Why the rule failed.
    #[serde(rename = "message")]
    #[validate(custom(function = "check_xss_string"))]
    pub message: String,

    /// The resource validated.
    #[serde(rename = "resource")]
    #[validate(custom(function = "check_xss_string"))]
    pub resource: String,

    /// The name of the rule.
    #[serde(rename = "rule")]
    #[validate(custom(function = "check_xss_string"))]
    pub rule: String,
}

impl ValidationProblemViolationsInner {
    #[allow(clippy::new_without_default, clippy::too_many_arguments)]
    pub fn new(
        message: String,
        resource: String,
        rule: String,
    ) -> ValidationProblemViolationsInner {
        ValidationProblemViolationsInner {
            field: None,
            message,
            resource,
            rule,
        }
    }
}

/// Converts the ValidationProblemViolationsInner value to the Query Parameters representation (style=form, explode=false)
/// specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde serializer
impl std::fmt::Display for ValidationProblemViolationsInner {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let params: Vec<Option<String>> = vec![
            self.field
                .as_ref()
                .map(|field| ["field".to_string(), field.to_string()].join(",")),
            Some("message".to_string()),
            Some(self.message.to_string()),
            Some("resource".to_string()),
            Some(self.resource.to_string()),
            Some("rule".to_string()),
            Some(self.rule.to_string()),
        ];

        write!(
            f,
            "{}",
            params.into_iter().flatten().collect::<Vec<_>>().join(",")
        )
    }
}

/// Converts Query Parameters representation (style=form, explode=false) to a ValidationProblemViolationsInner value
/// as specified in https://swagger.io/docs/specification/serialization/
/// Should be implemented in a serde deserializer
impl std::str::FromStr for ValidationProblemViolationsInner {
    type Err = String;

    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        /// An intermediate representation of the struct to use for parsing.
        #[derive(Default)]
        #[allow(dead_code)]
        struct IntermediateRep {
            pub field: Vec<String>,
            pub message: Vec<String>,
            pub resource: Vec<String>,
            pub rule: Vec<String>,
        }

        let mut intermediate_rep = IntermediateRep::default();

        // Parse into intermediate representation
        let mut string_iter = s.split(',');
        let mut key_result = string_iter.next();

        while key_result.is_some() {
            let val = match string_iter.next() {
                Some(x) => x,
                None => {
                    return std::result::Result::Err(
                        "Missing value while parsing ValidationProblemViolationsInner".to_string(),
                    );
                }
            };

            if let Some(key) = key_result {
                #[allow(clippy::match_single_binding)]
                match key {
                    #[allow(clippy::redundant_clone)]
                    "field" => intermediate_rep.field.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "message" => intermediate_rep.message.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "resource" => intermediate_rep.resource.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    #[allow(clippy::redundant_clone)]
                    "rule" => intermediate_rep.rule.push(
                        <String as std::str::FromStr>::from_str(val).map_err(|x| x.to_string())?,
                    ),
                    _ => {
                        return std::result::Result::Err(
                            "Unexpected key while parsing ValidationProblemViolationsInner"
                                .to_string(),
                        );
                    }
                }
            }

            // Get the next key
            key_result = string_iter.next();
        }

        // Use the intermediate representation to return the struct
        std::result::Result::Ok(ValidationProblemViolationsInner {
            field: intermediate_rep.field.into_iter().next(),
            message: intermediate_rep
                .message
                .into_iter()
                .next()
                .ok_or_else(|| "message missing in ValidationProblemViolationsInner".to_string())?,
            resource: intermediate_rep
                .resource
                .into_iter()
                .next()
                .ok_or_else(|| {
                    "resource missing in ValidationProblemViolationsInner".to_string()
                })?,
            rule: intermediate_rep
                .rule
                .into_iter()
                .next()
                .ok_or_else(|| "rule missing in ValidationProblemViolationsInner".to_string())?,
        })
    }
}

// Methods for converting between header::IntoHeaderValue<ValidationProblemViolationsInner> and HeaderValue

#[cfg(feature = "server")]
impl std::convert::TryFrom<header::IntoHeaderValue<ValidationProblemViolationsInner>>
    for HeaderValue
{
    type Error = String;

    fn try_from(
        hdr_value: header::IntoHeaderValue<ValidationProblemViolationsInner>,
    ) -> std::result::Result<Self, Self::Error> {
        let hdr_value = hdr_value.to_string();
        match HeaderValue::from_str(&hdr_value) {
            std::result::Result::Ok(value) => std::result::Result::Ok(value),
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Invalid header value for ValidationProblemViolationsInner - value: {hdr_value} is invalid {e}"#
            )),
        }
    }
}

#[cfg(feature = "server")]
impl std::convert::TryFrom<HeaderValue>
    for header::IntoHeaderValue<ValidationProblemViolationsInner>
{
    type Error = String;

    fn try_from(hdr_value: HeaderValue) -> std::result::Result<Self, Self::Error> {
        match hdr_value.to_str() {
            std::result::Result::Ok(value) => {
                match <ValidationProblemViolationsInner as std::str::FromStr>::from_str(value) {
                    std::result::Result::Ok(value) => {
                        std::result::Result::Ok(header::IntoHeaderValue(value))
                    }
                    std::result::Result::Err(err) => std::result::Result::Err(format!(
                        r#"Unable to convert header value '{value}' into ValidationProblemViolationsInner - {err}"#
                    )),
                }
            }
            std::result::Result::Err(e) => std::result::Result::Err(format!(
                r#"Unable to convert header: {hdr_value:?} to string: {e}"#
            )),
        }
    }
}
