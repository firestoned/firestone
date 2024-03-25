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
    Path,
    Query,
    Response,
    Security,
    status,
)

from addressbook.models.extra_models import TokenModel  # noqa: F401
from addressbook.models.addressbook import Addressbook
from addressbook.models.create_addressbook import CreateAddressbook
from addressbook.models.create_person import CreatePerson
from addressbook.models.person import Person
from addressbook.models.update_addressbook import UpdateAddressbook
from addressbook.models.update_person import UpdatePerson
from addressbook.security_api import get_token_bearer_auth

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
    address_key: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """delete operation for /addressbook/{address_key}/addrtype"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_addrtype_delete(address_key)


@router.get(
    "/addressbook/{address_key}/addrtype",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_addrtype_get(
    address_key: str = Path(..., description=""),
    city: str = Query(None, description="Filter by city name", alias="city"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """get operation for /addressbook/{address_key}/addrtype"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_addrtype_get(
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
    address_key: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /addressbook/{address_key}/addrtype"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_addrtype_head(address_key)


@router.put(
    "/addressbook/{address_key}/addrtype",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_addrtype_put(
    address_key: str = Path(..., description=""),
    body: str = Body(None, description="The request body for /addressbook/{address_key}/addrtype"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """put operation for /addressbook/{address_key}/addrtype"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_addrtype_put(
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
    address_key: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """delete operation for /addressbook/{address_key}/city"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_city_delete(address_key)


@router.get(
    "/addressbook/{address_key}/city",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_city_get(
    address_key: str = Path(..., description=""),
    city: str = Query(None, description="Filter by city name", alias="city"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """get operation for /addressbook/{address_key}/city"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_city_get(address_key, city)


@router.head(
    "/addressbook/{address_key}/city",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_city_head(
    address_key: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /addressbook/{address_key}/city"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_city_head(address_key)


@router.put(
    "/addressbook/{address_key}/city",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_city_put(
    address_key: str = Path(..., description=""),
    body: str = Body(None, description="The request body for /addressbook/{address_key}/city"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """put operation for /addressbook/{address_key}/city"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_city_put(address_key, body)


@router.delete(
    "/addressbook/{address_key}/country",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_country_delete(
    address_key: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """delete operation for /addressbook/{address_key}/country"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_country_delete(address_key)


@router.get(
    "/addressbook/{address_key}/country",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_country_get(
    address_key: str = Path(..., description=""),
    city: str = Query(None, description="Filter by city name", alias="city"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """get operation for /addressbook/{address_key}/country"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_country_get(address_key, city)


@router.head(
    "/addressbook/{address_key}/country",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_country_head(
    address_key: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /addressbook/{address_key}/country"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_country_head(address_key)


@router.put(
    "/addressbook/{address_key}/country",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_country_put(
    address_key: str = Path(..., description=""),
    body: str = Body(None, description="The request body for /addressbook/{address_key}/country"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """put operation for /addressbook/{address_key}/country"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_country_put(address_key, body)


@router.delete(
    "/addressbook/{address_key}",
    responses={
        200: {"model": Addressbook, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_delete(
    address_key: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> Addressbook:
    """Delete an address from this addressbook."""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_delete(address_key)


@router.get(
    "/addressbook/{address_key}",
    responses={
        200: {"model": Addressbook, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_get(
    address_key: str = Path(..., description=""),
    city: str = Query(None, description="Filter by city name", alias="city"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> Addressbook:
    """Get a specific address from this addressbook."""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_get(address_key, city)


@router.head(
    "/addressbook/{address_key}",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_head(
    address_key: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """Determine the existence and size of this address."""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_head(address_key)


@router.delete(
    "/addressbook/{address_key}/people",
    responses={
        200: {"model": List[str], "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_people_delete(
    address_key: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> List[str]:
    """delete operation for /addressbook/{address_key}/people"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_people_delete(address_key)


@router.get(
    "/addressbook/{address_key}/people",
    responses={
        200: {"model": List[str], "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_people_get(
    address_key: str = Path(..., description=""),
    city: str = Query(None, description="Filter by city name", alias="city"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> List[str]:
    """get operation for /addressbook/{address_key}/people"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_people_get(address_key, city)


@router.head(
    "/addressbook/{address_key}/people",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_people_head(
    address_key: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /addressbook/{address_key}/people"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_people_head(address_key)


@router.put(
    "/addressbook/{address_key}/people",
    responses={
        200: {"model": List[str], "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_people_put(
    address_key: str = Path(..., description=""),
    request_body: List[str] = Body(
        None, description="The request body for /addressbook/{address_key}/people"
    ),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> List[str]:
    """put operation for /addressbook/{address_key}/people"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_people_put(
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
    address_key: str = Path(..., description=""),
    limit: int = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: int = Query(
        None, description="The offset to start returning resources", alias="offset"
    ),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> Person:
    """delete operation for /addressbook/{address_key}/person"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_delete(
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
    address_key: str = Path(..., description=""),
    last_name: str = Query(None, description="Filter by last name", alias="last_name"),
    limit: int = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: int = Query(
        None, description="The offset to start returning resources", alias="offset"
    ),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> List[Person]:
    """get operation for /addressbook/{address_key}/person"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_get(
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
    address_key: str = Path(..., description=""),
    limit: int = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: int = Query(
        None, description="The offset to start returning resources", alias="offset"
    ),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /addressbook/{address_key}/person"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_head(
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
    address_key: str = Path(..., description=""),
    limit: int = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: int = Query(
        None, description="The offset to start returning resources", alias="offset"
    ),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> Person:
    """patch operation for /addressbook/{address_key}/person"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_patch(
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
    address_key: str = Path(..., description=""),
    create_person: CreatePerson = Body(
        None, description="The request body for /addressbook/{address_key}/person"
    ),
    limit: int = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: int = Query(
        None, description="The offset to start returning resources", alias="offset"
    ),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> CreatePerson:
    """post operation for /addressbook/{address_key}/person"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_post(
        address_key, create_person, limit, offset
    )


@router.delete(
    "/addressbook/{address_key}/person/{uuid}/age",
    responses={
        200: {"model": int, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_age_delete(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> int:
    """delete operation for /addressbook/{address_key}/person/{uuid}/age"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_age_delete(
        address_key, uuid
    )


@router.get(
    "/addressbook/{address_key}/person/{uuid}/age",
    responses={
        200: {"model": int, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_age_get(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    last_name: str = Query(None, description="Filter by last name", alias="last_name"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> int:
    """get operation for /addressbook/{address_key}/person/{uuid}/age"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_age_get(
        address_key, uuid, last_name
    )


@router.head(
    "/addressbook/{address_key}/person/{uuid}/age",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_age_head(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /addressbook/{address_key}/person/{uuid}/age"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_age_head(
        address_key, uuid
    )


@router.put(
    "/addressbook/{address_key}/person/{uuid}/age",
    responses={
        200: {"model": int, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_age_put(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    body: int = Body(
        None, description="The request body for /addressbook/{address_key}/person/{uuid}/age"
    ),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> int:
    """put operation for /addressbook/{address_key}/person/{uuid}/age"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_age_put(
        address_key, uuid, body
    )


@router.delete(
    "/addressbook/{address_key}/person/{uuid}",
    responses={
        200: {"model": Person, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_delete(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> Person:
    """delete operation for /addressbook/{address_key}/person/{uuid}"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_delete(
        address_key, uuid
    )


@router.delete(
    "/addressbook/{address_key}/person/{uuid}/first_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_first_name_delete(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """delete operation for /addressbook/{address_key}/person/{uuid}/first_name"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_first_name_delete(
        address_key, uuid
    )


@router.get(
    "/addressbook/{address_key}/person/{uuid}/first_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_first_name_get(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    last_name: str = Query(None, description="Filter by last name", alias="last_name"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """get operation for /addressbook/{address_key}/person/{uuid}/first_name"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_first_name_get(
        address_key, uuid, last_name
    )


@router.head(
    "/addressbook/{address_key}/person/{uuid}/first_name",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_first_name_head(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /addressbook/{address_key}/person/{uuid}/first_name"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_first_name_head(
        address_key, uuid
    )


@router.put(
    "/addressbook/{address_key}/person/{uuid}/first_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_first_name_put(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    body: str = Body(
        None, description="The request body for /addressbook/{address_key}/person/{uuid}/first_name"
    ),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """put operation for /addressbook/{address_key}/person/{uuid}/first_name"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_first_name_put(
        address_key, uuid, body
    )


@router.get(
    "/addressbook/{address_key}/person/{uuid}",
    responses={
        200: {"model": Person, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_get(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    last_name: str = Query(None, description="Filter by last name", alias="last_name"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> Person:
    """get operation for /addressbook/{address_key}/person/{uuid}"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_get(
        address_key, uuid, last_name
    )


@router.head(
    "/addressbook/{address_key}/person/{uuid}",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_head(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /addressbook/{address_key}/person/{uuid}"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_head(
        address_key, uuid
    )


@router.delete(
    "/addressbook/{address_key}/person/{uuid}/hobbies",
    responses={
        200: {"model": List[str], "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_hobbies_delete(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> List[str]:
    """delete operation for /addressbook/{address_key}/person/{uuid}/hobbies"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_hobbies_delete(
        address_key, uuid
    )


@router.get(
    "/addressbook/{address_key}/person/{uuid}/hobbies",
    responses={
        200: {"model": List[str], "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_hobbies_get(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    last_name: str = Query(None, description="Filter by last name", alias="last_name"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> List[str]:
    """get operation for /addressbook/{address_key}/person/{uuid}/hobbies"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_hobbies_get(
        address_key, uuid, last_name
    )


@router.head(
    "/addressbook/{address_key}/person/{uuid}/hobbies",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_hobbies_head(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /addressbook/{address_key}/person/{uuid}/hobbies"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_hobbies_head(
        address_key, uuid
    )


@router.put(
    "/addressbook/{address_key}/person/{uuid}/hobbies",
    responses={
        200: {"model": List[str], "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_hobbies_put(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    request_body: List[str] = Body(
        None, description="The request body for /addressbook/{address_key}/person/{uuid}/hobbies"
    ),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> List[str]:
    """put operation for /addressbook/{address_key}/person/{uuid}/hobbies"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_hobbies_put(
        address_key, uuid, request_body
    )


@router.delete(
    "/addressbook/{address_key}/person/{uuid}/last_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_last_name_delete(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """delete operation for /addressbook/{address_key}/person/{uuid}/last_name"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_last_name_delete(
        address_key, uuid
    )


@router.get(
    "/addressbook/{address_key}/person/{uuid}/last_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_last_name_get(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    last_name: str = Query(None, description="Filter by last name", alias="last_name"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """get operation for /addressbook/{address_key}/person/{uuid}/last_name"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_last_name_get(
        address_key, uuid, last_name
    )


@router.head(
    "/addressbook/{address_key}/person/{uuid}/last_name",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_last_name_head(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /addressbook/{address_key}/person/{uuid}/last_name"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_last_name_head(
        address_key, uuid
    )


@router.put(
    "/addressbook/{address_key}/person/{uuid}/last_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_last_name_put(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    body: str = Body(
        None, description="The request body for /addressbook/{address_key}/person/{uuid}/last_name"
    ),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """put operation for /addressbook/{address_key}/person/{uuid}/last_name"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_last_name_put(
        address_key, uuid, body
    )


@router.patch(
    "/addressbook/{address_key}/person/{uuid}",
    responses={
        200: {"model": Person, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_patch(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> Person:
    """patch operation for /addressbook/{address_key}/person/{uuid}"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_patch(
        address_key, uuid
    )


@router.put(
    "/addressbook/{address_key}/person/{uuid}",
    responses={
        200: {"model": UpdatePerson, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_person_uuid_put(
    address_key: str = Path(..., description=""),
    uuid: str = Path(..., description=""),
    update_person: UpdatePerson = Body(
        None, description="The request body for /addressbook/{address_key}/person/{uuid}"
    ),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> UpdatePerson:
    """put operation for /addressbook/{address_key}/person/{uuid}"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_person_uuid_put(
        address_key, uuid, update_person
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
    address_key: str = Path(..., description=""),
    update_addressbook: UpdateAddressbook = Body(
        None, description="The request body for /addressbook/{address_key}"
    ),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> UpdateAddressbook:
    """Update an existing address in this addressbook, with the given address key."""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_put(
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
    address_key: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """delete operation for /addressbook/{address_key}/state"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_state_delete(address_key)


@router.get(
    "/addressbook/{address_key}/state",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_state_get(
    address_key: str = Path(..., description=""),
    city: str = Query(None, description="Filter by city name", alias="city"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """get operation for /addressbook/{address_key}/state"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_state_get(address_key, city)


@router.head(
    "/addressbook/{address_key}/state",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_state_head(
    address_key: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /addressbook/{address_key}/state"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_state_head(address_key)


@router.put(
    "/addressbook/{address_key}/state",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_state_put(
    address_key: str = Path(..., description=""),
    body: str = Body(None, description="The request body for /addressbook/{address_key}/state"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """put operation for /addressbook/{address_key}/state"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_state_put(address_key, body)


@router.delete(
    "/addressbook/{address_key}/street",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_street_delete(
    address_key: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """delete operation for /addressbook/{address_key}/street"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_street_delete(address_key)


@router.get(
    "/addressbook/{address_key}/street",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_street_get(
    address_key: str = Path(..., description=""),
    city: str = Query(None, description="Filter by city name", alias="city"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """get operation for /addressbook/{address_key}/street"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_street_get(address_key, city)


@router.head(
    "/addressbook/{address_key}/street",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_street_head(
    address_key: str = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /addressbook/{address_key}/street"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_street_head(address_key)


@router.put(
    "/addressbook/{address_key}/street",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_address_key_street_put(
    address_key: str = Path(..., description=""),
    body: str = Body(None, description="The request body for /addressbook/{address_key}/street"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """put operation for /addressbook/{address_key}/street"""
    return BaseAddressbookApi.subclasses[0]().addressbook_address_key_street_put(address_key, body)


@router.get(
    "/addressbook",
    responses={
        200: {"model": List[Addressbook], "description": "Response for OK"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_get(
    city: str = Query(None, description="Filter by city name", alias="city"),
    limit: int = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: int = Query(
        None, description="The offset to start returning resources", alias="offset"
    ),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> List[Addressbook]:
    """List all addresses in this addressbook."""
    return BaseAddressbookApi.subclasses[0]().addressbook_get(city, limit, offset)


@router.post(
    "/addressbook",
    responses={
        201: {"model": CreateAddressbook, "description": "Response for CREATED"},
    },
    tags=["addressbook"],
    response_model_by_alias=True,
)
async def addressbook_post(
    create_addressbook: CreateAddressbook = Body(
        None, description="The request body for /addressbook"
    ),
    limit: int = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: int = Query(
        None, description="The offset to start returning resources", alias="offset"
    ),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> CreateAddressbook:
    """Create a new address in this addressbook, a new address key will be created."""
    return BaseAddressbookApi.subclasses[0]().addressbook_post(create_addressbook, limit, offset)
