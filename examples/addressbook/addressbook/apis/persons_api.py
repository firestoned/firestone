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
