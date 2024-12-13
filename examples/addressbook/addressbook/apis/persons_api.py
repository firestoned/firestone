# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from addressbook.apis.persons_api_base import BasePersonsApi
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
from pydantic import Field, StrictInt, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from addressbook.models.create_person import CreatePerson
from addressbook.models.person import Person
from addressbook.models.update_person import UpdatePerson
from addressbook.security_api import get_token_bearer_auth

router = APIRouter()

ns_pkg = addressbook.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/persons",
    responses={
        200: {"model": List[Person], "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_get(
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
    """List all persons in this collection"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_get(last_name, limit, offset)


@router.post(
    "/persons",
    responses={
        201: {"model": CreatePerson, "description": "Response for CREATED"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_post(
    create_person: Annotated[
        CreatePerson, Field(description="The request body for /persons")
    ] = Body(None, description="The request body for /persons"),
    limit: Annotated[
        Optional[StrictInt], Field(description="Limit the number of responses back")
    ] = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: Annotated[
        Optional[StrictInt], Field(description="The offset to start returning resources")
    ] = Query(None, description="The offset to start returning resources", alias="offset"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> CreatePerson:
    """Create a new person in this collection, a new UUID key will be created"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_post(create_person, limit, offset)


@router.delete(
    "/persons/{uuid}/age",
    responses={
        200: {"model": int, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_age_delete(
    uuid: StrictStr = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> int:
    """delete operation for /persons/{uuid}/age"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_age_delete(uuid)


@router.get(
    "/persons/{uuid}/age",
    responses={
        200: {"model": int, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_age_get(
    uuid: StrictStr = Path(..., description=""),
    last_name: Annotated[Optional[StrictStr], Field(description="Filter by last name")] = Query(
        None, description="Filter by last name", alias="last_name"
    ),
) -> int:
    """get operation for /persons/{uuid}/age"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_age_get(uuid, last_name)


@router.head(
    "/persons/{uuid}/age",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_age_head(
    uuid: StrictStr = Path(..., description=""),
) -> None:
    """head operation for /persons/{uuid}/age"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_age_head(uuid)


@router.put(
    "/persons/{uuid}/age",
    responses={
        200: {"model": int, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_age_put(
    uuid: StrictStr = Path(..., description=""),
    body: Annotated[
        StrictInt, Field(description="The request body for /persons/{uuid}/age")
    ] = Body(None, description="The request body for /persons/{uuid}/age"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> int:
    """put operation for /persons/{uuid}/age"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_age_put(uuid, body)


@router.delete(
    "/persons/{uuid}",
    responses={
        200: {"model": Person, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_delete(
    uuid: StrictStr = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> Person:
    """delete operation for /persons/{uuid}"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_delete(uuid)


@router.delete(
    "/persons/{uuid}/first_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_first_name_delete(
    uuid: StrictStr = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """delete operation for /persons/{uuid}/first_name"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_first_name_delete(uuid)


@router.get(
    "/persons/{uuid}/first_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_first_name_get(
    uuid: StrictStr = Path(..., description=""),
    last_name: Annotated[Optional[StrictStr], Field(description="Filter by last name")] = Query(
        None, description="Filter by last name", alias="last_name"
    ),
) -> str:
    """get operation for /persons/{uuid}/first_name"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_first_name_get(uuid, last_name)


@router.head(
    "/persons/{uuid}/first_name",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_first_name_head(
    uuid: StrictStr = Path(..., description=""),
) -> None:
    """head operation for /persons/{uuid}/first_name"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_first_name_head(uuid)


@router.put(
    "/persons/{uuid}/first_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_first_name_put(
    uuid: StrictStr = Path(..., description=""),
    body: Annotated[
        StrictStr, Field(description="The request body for /persons/{uuid}/first_name")
    ] = Body(None, description="The request body for /persons/{uuid}/first_name"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """put operation for /persons/{uuid}/first_name"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_first_name_put(uuid, body)


@router.get(
    "/persons/{uuid}",
    responses={
        200: {"model": Person, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_get(
    uuid: StrictStr = Path(..., description=""),
    last_name: Annotated[Optional[StrictStr], Field(description="Filter by last name")] = Query(
        None, description="Filter by last name", alias="last_name"
    ),
) -> Person:
    """Get a specific person from this collection"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_get(uuid, last_name)


@router.head(
    "/persons/{uuid}",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_head(
    uuid: StrictStr = Path(..., description=""),
) -> None:
    """Determine the existence and size of this person"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_head(uuid)


@router.delete(
    "/persons/{uuid}/hobbies",
    responses={
        200: {"model": List[str], "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_hobbies_delete(
    uuid: StrictStr = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> List[str]:
    """delete operation for /persons/{uuid}/hobbies"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_hobbies_delete(uuid)


@router.get(
    "/persons/{uuid}/hobbies",
    responses={
        200: {"model": List[str], "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_hobbies_get(
    uuid: StrictStr = Path(..., description=""),
    last_name: Annotated[Optional[StrictStr], Field(description="Filter by last name")] = Query(
        None, description="Filter by last name", alias="last_name"
    ),
) -> List[str]:
    """get operation for /persons/{uuid}/hobbies"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_hobbies_get(uuid, last_name)


@router.head(
    "/persons/{uuid}/hobbies",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_hobbies_head(
    uuid: StrictStr = Path(..., description=""),
) -> None:
    """head operation for /persons/{uuid}/hobbies"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_hobbies_head(uuid)


@router.put(
    "/persons/{uuid}/hobbies",
    responses={
        200: {"model": List[str], "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_hobbies_put(
    uuid: StrictStr = Path(..., description=""),
    request_body: Annotated[
        List[StrictStr], Field(description="The request body for /persons/{uuid}/hobbies")
    ] = Body(None, description="The request body for /persons/{uuid}/hobbies"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> List[str]:
    """put operation for /persons/{uuid}/hobbies"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_hobbies_put(uuid, request_body)


@router.delete(
    "/persons/{uuid}/last_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_last_name_delete(
    uuid: StrictStr = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """delete operation for /persons/{uuid}/last_name"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_last_name_delete(uuid)


@router.get(
    "/persons/{uuid}/last_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_last_name_get(
    uuid: StrictStr = Path(..., description=""),
    last_name: Annotated[Optional[StrictStr], Field(description="Filter by last name")] = Query(
        None, description="Filter by last name", alias="last_name"
    ),
) -> str:
    """get operation for /persons/{uuid}/last_name"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_last_name_get(uuid, last_name)


@router.head(
    "/persons/{uuid}/last_name",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_last_name_head(
    uuid: StrictStr = Path(..., description=""),
) -> None:
    """head operation for /persons/{uuid}/last_name"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_last_name_head(uuid)


@router.put(
    "/persons/{uuid}/last_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_last_name_put(
    uuid: StrictStr = Path(..., description=""),
    body: Annotated[
        StrictStr, Field(description="The request body for /persons/{uuid}/last_name")
    ] = Body(None, description="The request body for /persons/{uuid}/last_name"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """put operation for /persons/{uuid}/last_name"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_last_name_put(uuid, body)


@router.put(
    "/persons/{uuid}",
    responses={
        200: {"model": UpdatePerson, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_put(
    uuid: StrictStr = Path(..., description=""),
    update_person: Annotated[
        UpdatePerson, Field(description="The request body for /persons/{uuid}")
    ] = Body(None, description="The request body for /persons/{uuid}"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> UpdatePerson:
    """Put a new person in this collection, with the given UUId key"""
    if not BasePersonsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePersonsApi.subclasses[0]().persons_uuid_put(uuid, update_person)
