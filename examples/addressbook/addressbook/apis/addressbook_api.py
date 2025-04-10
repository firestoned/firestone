# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from addressbook.apis.addressbook_api_base import BaseAddressbookApi
import addressbook.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from addressbook.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Any, List, Optional
from typing_extensions import Annotated
from addressbook.models.addressbook import Addressbook
from addressbook.models.create_addressbook import CreateAddressbook
from addressbook.models.create_person import CreatePerson
from addressbook.models.person import Person
from addressbook.models.update_addressbook import UpdateAddressbook


router = APIRouter()

ns_pkg = addressbook.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/addressbook/{address_key}/addrtype",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_addrtype_delete(
    address_key: StrictStr = Path(..., description=""),
) -> str:
    """delete operation for /addressbook/{address_key}/addrtype"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_addrtype_delete(
        address_key
    )


@router.get(
    "/addressbook/{address_key}/addrtype",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_addrtype_get(
    address_key: StrictStr = Path(..., description=""),
    city: Annotated[Optional[StrictStr], Field(description="Filter by city name")] = Query(
        None, description="Filter by city name", alias="city"
    ),
) -> str:
    """get operation for /addressbook/{address_key}/addrtype"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_addrtype_get(
        address_key, city
    )


@router.head(
    "/addressbook/{address_key}/addrtype",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_addrtype_head(
    address_key: StrictStr = Path(..., description=""),
) -> None:
    """head operation for /addressbook/{address_key}/addrtype"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_addrtype_head(
        address_key
    )


@router.put(
    "/addressbook/{address_key}/addrtype",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_addrtype_put(
    address_key: StrictStr = Path(..., description=""),
    body: Annotated[
        StrictStr, Field(description="The request body for /addressbook/{address_key}/addrtype")
    ] = Body(None, description="The request body for /addressbook/{address_key}/addrtype"),
) -> str:
    """put operation for /addressbook/{address_key}/addrtype"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_addrtype_put(
        address_key, body
    )


@router.delete(
    "/addressbook/{address_key}/city",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_city_delete(
    address_key: StrictStr = Path(..., description=""),
) -> str:
    """delete operation for /addressbook/{address_key}/city"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_city_delete(address_key)


@router.get(
    "/addressbook/{address_key}/city",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_city_get(
    address_key: StrictStr = Path(..., description=""),
    city: Annotated[Optional[StrictStr], Field(description="Filter by city name")] = Query(
        None, description="Filter by city name", alias="city"
    ),
) -> str:
    """get operation for /addressbook/{address_key}/city"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_city_get(
        address_key, city
    )


@router.head(
    "/addressbook/{address_key}/city",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_city_head(
    address_key: StrictStr = Path(..., description=""),
) -> None:
    """head operation for /addressbook/{address_key}/city"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_city_head(address_key)


@router.put(
    "/addressbook/{address_key}/city",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_city_put(
    address_key: StrictStr = Path(..., description=""),
    body: Annotated[
        StrictStr, Field(description="The request body for /addressbook/{address_key}/city")
    ] = Body(None, description="The request body for /addressbook/{address_key}/city"),
) -> str:
    """put operation for /addressbook/{address_key}/city"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_city_put(
        address_key, body
    )


@router.delete(
    "/addressbook/{address_key}/country",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_country_delete(
    address_key: StrictStr = Path(..., description=""),
) -> str:
    """delete operation for /addressbook/{address_key}/country"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_country_delete(
        address_key
    )


@router.get(
    "/addressbook/{address_key}/country",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_country_get(
    address_key: StrictStr = Path(..., description=""),
    city: Annotated[Optional[StrictStr], Field(description="Filter by city name")] = Query(
        None, description="Filter by city name", alias="city"
    ),
) -> str:
    """get operation for /addressbook/{address_key}/country"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_country_get(
        address_key, city
    )


@router.head(
    "/addressbook/{address_key}/country",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_country_head(
    address_key: StrictStr = Path(..., description=""),
) -> None:
    """head operation for /addressbook/{address_key}/country"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_country_head(
        address_key
    )


@router.put(
    "/addressbook/{address_key}/country",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_country_put(
    address_key: StrictStr = Path(..., description=""),
    body: Annotated[
        StrictStr, Field(description="The request body for /addressbook/{address_key}/country")
    ] = Body(None, description="The request body for /addressbook/{address_key}/country"),
) -> str:
    """put operation for /addressbook/{address_key}/country"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_country_put(
        address_key, body
    )


@router.delete(
    "/addressbook/{address_key}",
    responses={
        200: {"model": Addressbook, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_delete(
    address_key: StrictStr = Path(..., description=""),
) -> Addressbook:
    """Delete an address from this addressbook."""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_delete(address_key)


@router.get(
    "/addressbook/{address_key}",
    responses={
        200: {"model": Addressbook, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_get(
    address_key: StrictStr = Path(..., description=""),
    city: Annotated[Optional[StrictStr], Field(description="Filter by city name")] = Query(
        None, description="Filter by city name", alias="city"
    ),
) -> Addressbook:
    """Get a specific address from this addressbook."""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_get(address_key, city)


@router.head(
    "/addressbook/{address_key}",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_head(
    address_key: StrictStr = Path(..., description=""),
) -> None:
    """Determine the existence and size of this address."""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_head(address_key)


@router.delete(
    "/addressbook/{address_key}/is_valid",
    responses={
        200: {"model": bool, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_is_valid_delete(
    address_key: StrictStr = Path(..., description=""),
) -> bool:
    """delete operation for /addressbook/{address_key}/is_valid"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_is_valid_delete(
        address_key
    )


@router.get(
    "/addressbook/{address_key}/is_valid",
    responses={
        200: {"model": bool, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_is_valid_get(
    address_key: StrictStr = Path(..., description=""),
    city: Annotated[Optional[StrictStr], Field(description="Filter by city name")] = Query(
        None, description="Filter by city name", alias="city"
    ),
) -> bool:
    """get operation for /addressbook/{address_key}/is_valid"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_is_valid_get(
        address_key, city
    )


@router.head(
    "/addressbook/{address_key}/is_valid",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_is_valid_head(
    address_key: StrictStr = Path(..., description=""),
) -> None:
    """head operation for /addressbook/{address_key}/is_valid"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_is_valid_head(
        address_key
    )


@router.put(
    "/addressbook/{address_key}/is_valid",
    responses={
        200: {"model": bool, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_is_valid_put(
    address_key: StrictStr = Path(..., description=""),
    body: Annotated[
        StrictBool, Field(description="The request body for /addressbook/{address_key}/is_valid")
    ] = Body(None, description="The request body for /addressbook/{address_key}/is_valid"),
) -> bool:
    """put operation for /addressbook/{address_key}/is_valid"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_is_valid_put(
        address_key, body
    )


@router.delete(
    "/addressbook/{address_key}/people",
    responses={
        200: {"model": List[str], "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_people_delete(
    address_key: StrictStr = Path(..., description=""),
) -> List[str]:
    """delete operation for /addressbook/{address_key}/people"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_people_delete(
        address_key
    )


@router.get(
    "/addressbook/{address_key}/people",
    responses={
        200: {"model": List[str], "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_people_get(
    address_key: StrictStr = Path(..., description=""),
    city: Annotated[Optional[StrictStr], Field(description="Filter by city name")] = Query(
        None, description="Filter by city name", alias="city"
    ),
) -> List[str]:
    """get operation for /addressbook/{address_key}/people"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_people_get(
        address_key, city
    )


@router.head(
    "/addressbook/{address_key}/people",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_people_head(
    address_key: StrictStr = Path(..., description=""),
) -> None:
    """head operation for /addressbook/{address_key}/people"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_people_head(address_key)


@router.put(
    "/addressbook/{address_key}/people",
    responses={
        200: {"model": List[str], "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_people_put(
    address_key: StrictStr = Path(..., description=""),
    request_body: Annotated[
        List[StrictStr], Field(description="The request body for /addressbook/{address_key}/people")
    ] = Body(None, description="The request body for /addressbook/{address_key}/people"),
) -> List[str]:
    """put operation for /addressbook/{address_key}/people"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_people_put(
        address_key, request_body
    )


@router.delete(
    "/addressbook/{address_key}/person",
    responses={
        200: {"model": Person, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_delete(
    address_key: StrictStr = Path(..., description=""),
    limit: Annotated[
        Optional[StrictInt], Field(description="Limit the number of responses back")
    ] = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: Annotated[
        Optional[StrictInt], Field(description="The offset to start returning resources")
    ] = Query(None, description="The offset to start returning resources", alias="offset"),
) -> Person:
    """delete operation for /addressbook/{address_key}/person"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_delete(
        address_key, limit, offset
    )


@router.get(
    "/addressbook/{address_key}/person",
    responses={
        200: {"model": List[Person], "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_get(
    address_key: StrictStr = Path(..., description=""),
    last_name: Annotated[Optional[StrictStr], Field(description="Filter by last name")] = Query(
        None, description="Filter by last name", alias="last_name"
    ),
    limit: Annotated[
        Optional[StrictInt], Field(description="Limit the number of responses back")
    ] = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: Annotated[
        Optional[StrictInt], Field(description="The offset to start returning resources")
    ] = Query(None, description="The offset to start returning resources", alias="offset"),
) -> List[Person]:
    """get operation for /addressbook/{address_key}/person"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_get(
        address_key, last_name, limit, offset
    )


@router.head(
    "/addressbook/{address_key}/person",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_head(
    address_key: StrictStr = Path(..., description=""),
    limit: Annotated[
        Optional[StrictInt], Field(description="Limit the number of responses back")
    ] = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: Annotated[
        Optional[StrictInt], Field(description="The offset to start returning resources")
    ] = Query(None, description="The offset to start returning resources", alias="offset"),
) -> None:
    """head operation for /addressbook/{address_key}/person"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_head(
        address_key, limit, offset
    )


@router.patch(
    "/addressbook/{address_key}/person",
    responses={
        200: {"model": Person, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_patch(
    address_key: StrictStr = Path(..., description=""),
    limit: Annotated[
        Optional[StrictInt], Field(description="Limit the number of responses back")
    ] = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: Annotated[
        Optional[StrictInt], Field(description="The offset to start returning resources")
    ] = Query(None, description="The offset to start returning resources", alias="offset"),
) -> Person:
    """patch operation for /addressbook/{address_key}/person"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_patch(
        address_key, limit, offset
    )


@router.post(
    "/addressbook/{address_key}/person",
    responses={
        201: {"model": CreatePerson, "description": "Response for CREATED"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_post(
    address_key: StrictStr = Path(..., description=""),
    create_person: Annotated[
        CreatePerson, Field(description="The request body for /addressbook/{address_key}/person")
    ] = Body(None, description="The request body for /addressbook/{address_key}/person"),
    limit: Annotated[
        Optional[StrictInt], Field(description="Limit the number of responses back")
    ] = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: Annotated[
        Optional[StrictInt], Field(description="The offset to start returning resources")
    ] = Query(None, description="The offset to start returning resources", alias="offset"),
) -> CreatePerson:
    """post operation for /addressbook/{address_key}/person"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_post(
        address_key, create_person, limit, offset
    )


@router.put(
    "/addressbook/{address_key}",
    responses={
        200: {"model": UpdateAddressbook, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_put(
    address_key: StrictStr = Path(..., description=""),
    update_addressbook: Annotated[
        UpdateAddressbook, Field(description="The request body for /addressbook/{address_key}")
    ] = Body(None, description="The request body for /addressbook/{address_key}"),
) -> UpdateAddressbook:
    """Update an existing address in this addressbook, with the given address key."""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_put(
        address_key, update_addressbook
    )


@router.delete(
    "/addressbook/{address_key}/state",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_state_delete(
    address_key: StrictStr = Path(..., description=""),
) -> str:
    """delete operation for /addressbook/{address_key}/state"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_state_delete(
        address_key
    )


@router.get(
    "/addressbook/{address_key}/state",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_state_get(
    address_key: StrictStr = Path(..., description=""),
    city: Annotated[Optional[StrictStr], Field(description="Filter by city name")] = Query(
        None, description="Filter by city name", alias="city"
    ),
) -> str:
    """get operation for /addressbook/{address_key}/state"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_state_get(
        address_key, city
    )


@router.head(
    "/addressbook/{address_key}/state",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_state_head(
    address_key: StrictStr = Path(..., description=""),
) -> None:
    """head operation for /addressbook/{address_key}/state"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_state_head(address_key)


@router.put(
    "/addressbook/{address_key}/state",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_state_put(
    address_key: StrictStr = Path(..., description=""),
    body: Annotated[
        StrictStr, Field(description="The request body for /addressbook/{address_key}/state")
    ] = Body(None, description="The request body for /addressbook/{address_key}/state"),
) -> str:
    """put operation for /addressbook/{address_key}/state"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_state_put(
        address_key, body
    )


@router.delete(
    "/addressbook/{address_key}/street",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_street_delete(
    address_key: StrictStr = Path(..., description=""),
) -> str:
    """delete operation for /addressbook/{address_key}/street"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_street_delete(
        address_key
    )


@router.get(
    "/addressbook/{address_key}/street",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_street_get(
    address_key: StrictStr = Path(..., description=""),
    city: Annotated[Optional[StrictStr], Field(description="Filter by city name")] = Query(
        None, description="Filter by city name", alias="city"
    ),
) -> str:
    """get operation for /addressbook/{address_key}/street"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_street_get(
        address_key, city
    )


@router.head(
    "/addressbook/{address_key}/street",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_street_head(
    address_key: StrictStr = Path(..., description=""),
) -> None:
    """head operation for /addressbook/{address_key}/street"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_street_head(address_key)


@router.put(
    "/addressbook/{address_key}/street",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_street_put(
    address_key: StrictStr = Path(..., description=""),
    body: Annotated[
        StrictStr, Field(description="The request body for /addressbook/{address_key}/street")
    ] = Body(None, description="The request body for /addressbook/{address_key}/street"),
) -> str:
    """put operation for /addressbook/{address_key}/street"""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_address_key_street_put(
        address_key, body
    )


@router.get(
    "/addressbook",
    responses={
        200: {"model": List[Addressbook], "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_get(
    city: Annotated[Optional[StrictStr], Field(description="Filter by city name")] = Query(
        None, description="Filter by city name", alias="city"
    ),
    limit: Annotated[
        Optional[StrictInt], Field(description="Limit the number of responses back")
    ] = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: Annotated[
        Optional[StrictInt], Field(description="The offset to start returning resources")
    ] = Query(None, description="The offset to start returning resources", alias="offset"),
) -> List[Addressbook]:
    """List all addresses in this addressbook."""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_get(city, limit, offset)


@router.post(
    "/addressbook",
    responses={
        201: {"model": CreateAddressbook, "description": "Response for CREATED"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_post(
    create_addressbook: Annotated[
        CreateAddressbook, Field(description="The request body for /addressbook")
    ] = Body(None, description="The request body for /addressbook"),
    limit: Annotated[
        Optional[StrictInt], Field(description="Limit the number of responses back")
    ] = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: Annotated[
        Optional[StrictInt], Field(description="The offset to start returning resources")
    ] = Query(None, description="The offset to start returning resources", alias="offset"),
) -> CreateAddressbook:
    """Create a new address in this addressbook, a new address key will be created."""
    if not BaseAddressbookApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAddressbookApi.subclasses[0]().addressbook_post(
        create_addressbook, limit, offset
    )
