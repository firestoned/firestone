# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from addressbook.apis.postal_codes_api_base import BasePostalCodesApi
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
from addressbook.models.create_postal_code import CreatePostalCode
from addressbook.models.postal_code import PostalCode
from addressbook.security_api import get_token_bearer_auth

router = APIRouter()

ns_pkg = addressbook.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/postal_codes",
    responses={
        200: {"model": List[PostalCode], "description": "Response for OK"},
    },
    tags=["postal_codes"],
    response_model_by_alias=True,
)
async def postal_codes_get(
    name: Annotated[Optional[StrictStr], Field(description="Filter by name")] = Query(
        None, description="Filter by name", alias="name"
    ),
    limit: Annotated[
        Optional[StrictInt], Field(description="Limit the number of responses back")
    ] = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: Annotated[
        Optional[StrictInt], Field(description="The offset to start returning resources")
    ] = Query(None, description="The offset to start returning resources", alias="offset"),
) -> List[PostalCode]:
    """List all postal codes in this collection"""
    if not BasePostalCodesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePostalCodesApi.subclasses[0]().postal_codes_get(name, limit, offset)


@router.post(
    "/postal_codes",
    responses={
        201: {"model": CreatePostalCode, "description": "Response for CREATED"},
    },
    tags=["postal_codes"],
    response_model_by_alias=True,
)
async def postal_codes_post(
    create_postal_code: Annotated[
        CreatePostalCode, Field(description="The request body for /postal_codes")
    ] = Body(None, description="The request body for /postal_codes"),
    limit: Annotated[
        Optional[StrictInt], Field(description="Limit the number of responses back")
    ] = Query(None, description="Limit the number of responses back", alias="limit"),
    offset: Annotated[
        Optional[StrictInt], Field(description="The offset to start returning resources")
    ] = Query(None, description="The offset to start returning resources", alias="offset"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> CreatePostalCode:
    """Create a new postal code in this collection, a new UUID key will be created"""
    if not BasePostalCodesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePostalCodesApi.subclasses[0]().postal_codes_post(
        create_postal_code, limit, offset
    )


@router.delete(
    "/postal_codes/{uuid}",
    responses={
        200: {"model": PostalCode, "description": "Response for OK"},
    },
    tags=["postal_codes"],
    response_model_by_alias=True,
)
async def postal_codes_uuid_delete(
    uuid: StrictStr = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> PostalCode:
    """delete operation for /postal_codes/{uuid}"""
    if not BasePostalCodesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePostalCodesApi.subclasses[0]().postal_codes_uuid_delete(uuid)


@router.get(
    "/postal_codes/{uuid}",
    responses={
        200: {"model": PostalCode, "description": "Response for OK"},
    },
    tags=["postal_codes"],
    response_model_by_alias=True,
)
async def postal_codes_uuid_get(
    uuid: StrictStr = Path(..., description=""),
    name: Annotated[Optional[StrictStr], Field(description="Filter by name")] = Query(
        None, description="Filter by name", alias="name"
    ),
) -> PostalCode:
    """Get a specific postal code from this collection"""
    if not BasePostalCodesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePostalCodesApi.subclasses[0]().postal_codes_uuid_get(uuid, name)


@router.head(
    "/postal_codes/{uuid}",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["postal_codes"],
    response_model_by_alias=True,
)
async def postal_codes_uuid_head(
    uuid: StrictStr = Path(..., description=""),
) -> None:
    """Determine the existence and size of this postal code"""
    if not BasePostalCodesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePostalCodesApi.subclasses[0]().postal_codes_uuid_head(uuid)


@router.delete(
    "/postal_codes/{uuid}/name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["postal_codes"],
    response_model_by_alias=True,
)
async def postal_codes_uuid_name_delete(
    uuid: StrictStr = Path(..., description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """delete operation for /postal_codes/{uuid}/name"""
    if not BasePostalCodesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePostalCodesApi.subclasses[0]().postal_codes_uuid_name_delete(uuid)


@router.get(
    "/postal_codes/{uuid}/name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["postal_codes"],
    response_model_by_alias=True,
)
async def postal_codes_uuid_name_get(
    uuid: StrictStr = Path(..., description=""),
    name: Annotated[Optional[StrictStr], Field(description="Filter by name")] = Query(
        None, description="Filter by name", alias="name"
    ),
) -> str:
    """get operation for /postal_codes/{uuid}/name"""
    if not BasePostalCodesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePostalCodesApi.subclasses[0]().postal_codes_uuid_name_get(uuid, name)
