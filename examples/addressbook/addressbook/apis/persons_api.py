# coding: utf-8

from typing import Dict, List  # noqa: F401

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
from addressbook.models.create_person import CreatePerson
from addressbook.models.person import Person
from addressbook.models.update_person import UpdatePerson
from addressbook.security_api import get_token_bearer_auth

router = APIRouter()


@router.get(
    "/persons",
    responses={
        200: {"model": List[Person], "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_get(
    last_name: str = Query(None, description="Filter by last name"),
    limit: int = Query(None, description="Limit the number of responses back"),
    offset: int = Query(None, description="The offset to start returning resources"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> List[Person]:
    """List all persons in this collection"""
    ...


@router.post(
    "/persons",
    responses={
        201: {"model": CreatePerson, "description": "Response for CREATED"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_post(
    create_person: CreatePerson = Body(None, description="The request body for /persons"),
    limit: int = Query(None, description="Limit the number of responses back"),
    offset: int = Query(None, description="The offset to start returning resources"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> CreatePerson:
    """Create a new person in this collection, a new UUID key will be created"""
    ...


@router.delete(
    "/persons/{uuid}/age",
    responses={
        200: {"model": int, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_age_delete(
    uuid: str = Path(None, description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> int:
    """delete operation for /persons/{uuid}/age"""
    ...


@router.get(
    "/persons/{uuid}/age",
    responses={
        200: {"model": int, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_age_get(
    uuid: str = Path(None, description=""),
    last_name: str = Query(None, description="Filter by last name"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> int:
    """get operation for /persons/{uuid}/age"""
    ...


@router.head(
    "/persons/{uuid}/age",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_age_head(
    uuid: str = Path(None, description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /persons/{uuid}/age"""
    ...


@router.put(
    "/persons/{uuid}/age",
    responses={
        200: {"model": int, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_age_put(
    uuid: str = Path(None, description=""),
    body: int = Body(None, description="The request body for /persons/{uuid}/age"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> int:
    """put operation for /persons/{uuid}/age"""
    ...


@router.delete(
    "/persons/{uuid}",
    responses={
        200: {"model": Person, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_delete(
    uuid: str = Path(None, description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> Person:
    """delete operation for /persons/{uuid}"""
    ...


@router.delete(
    "/persons/{uuid}/first_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_first_name_delete(
    uuid: str = Path(None, description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """delete operation for /persons/{uuid}/first_name"""
    ...


@router.get(
    "/persons/{uuid}/first_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_first_name_get(
    uuid: str = Path(None, description=""),
    last_name: str = Query(None, description="Filter by last name"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """get operation for /persons/{uuid}/first_name"""
    ...


@router.head(
    "/persons/{uuid}/first_name",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_first_name_head(
    uuid: str = Path(None, description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /persons/{uuid}/first_name"""
    ...


@router.put(
    "/persons/{uuid}/first_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_first_name_put(
    uuid: str = Path(None, description=""),
    body: str = Body(None, description="The request body for /persons/{uuid}/first_name"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """put operation for /persons/{uuid}/first_name"""
    ...


@router.get(
    "/persons/{uuid}",
    responses={
        200: {"model": Person, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_get(
    uuid: str = Path(None, description=""),
    last_name: str = Query(None, description="Filter by last name"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> Person:
    """Get a specific person from this collection"""
    ...


@router.head(
    "/persons/{uuid}",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_head(
    uuid: str = Path(None, description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """Determine the existence and size of this person"""
    ...


@router.delete(
    "/persons/{uuid}/hobbies",
    responses={
        200: {"model": List[str], "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_hobbies_delete(
    uuid: str = Path(None, description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> List[str]:
    """delete operation for /persons/{uuid}/hobbies"""
    ...


@router.get(
    "/persons/{uuid}/hobbies",
    responses={
        200: {"model": List[str], "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_hobbies_get(
    uuid: str = Path(None, description=""),
    last_name: str = Query(None, description="Filter by last name"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> List[str]:
    """get operation for /persons/{uuid}/hobbies"""
    ...


@router.head(
    "/persons/{uuid}/hobbies",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_hobbies_head(
    uuid: str = Path(None, description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /persons/{uuid}/hobbies"""
    ...


@router.put(
    "/persons/{uuid}/hobbies",
    responses={
        200: {"model": List[str], "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_hobbies_put(
    uuid: str = Path(None, description=""),
    request_body: List[str] = Body(
        None, description="The request body for /persons/{uuid}/hobbies"
    ),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> List[str]:
    """put operation for /persons/{uuid}/hobbies"""
    ...


@router.delete(
    "/persons/{uuid}/last_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_last_name_delete(
    uuid: str = Path(None, description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """delete operation for /persons/{uuid}/last_name"""
    ...


@router.get(
    "/persons/{uuid}/last_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_last_name_get(
    uuid: str = Path(None, description=""),
    last_name: str = Query(None, description="Filter by last name"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """get operation for /persons/{uuid}/last_name"""
    ...


@router.head(
    "/persons/{uuid}/last_name",
    responses={
        200: {"description": "Default HEAD response"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_last_name_head(
    uuid: str = Path(None, description=""),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> None:
    """head operation for /persons/{uuid}/last_name"""
    ...


@router.put(
    "/persons/{uuid}/last_name",
    responses={
        200: {"model": str, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_last_name_put(
    uuid: str = Path(None, description=""),
    body: str = Body(None, description="The request body for /persons/{uuid}/last_name"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> str:
    """put operation for /persons/{uuid}/last_name"""
    ...


@router.put(
    "/persons/{uuid}",
    responses={
        200: {"model": UpdatePerson, "description": "Response for OK"},
    },
    tags=["persons"],
    response_model_by_alias=True,
)
async def persons_uuid_put(
    uuid: str = Path(None, description=""),
    update_person: UpdatePerson = Body(None, description="The request body for /persons/{uuid}"),
    token_bearer_auth: TokenModel = Security(get_token_bearer_auth),
) -> UpdatePerson:
    """Put a new person in this collection, with the given UUId key"""
    ...
