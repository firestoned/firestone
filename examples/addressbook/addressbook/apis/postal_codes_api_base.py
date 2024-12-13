# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictInt, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from addressbook.models.create_postal_code import CreatePostalCode
from addressbook.models.postal_code import PostalCode
from addressbook.security_api import get_token_bearer_auth


class BasePostalCodesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BasePostalCodesApi.subclasses = BasePostalCodesApi.subclasses + (cls,)

    async def postal_codes_get(
        self,
        name: Annotated[Optional[StrictStr], Field(description="Filter by name")],
        limit: Annotated[
            Optional[StrictInt], Field(description="Limit the number of responses back")
        ],
        offset: Annotated[
            Optional[StrictInt], Field(description="The offset to start returning resources")
        ],
    ) -> List[PostalCode]:
        """List all postal codes in this collection"""
        ...

    async def postal_codes_post(
        self,
        create_postal_code: Annotated[
            CreatePostalCode, Field(description="The request body for /postal_codes")
        ],
        limit: Annotated[
            Optional[StrictInt], Field(description="Limit the number of responses back")
        ],
        offset: Annotated[
            Optional[StrictInt], Field(description="The offset to start returning resources")
        ],
    ) -> CreatePostalCode:
        """Create a new postal code in this collection, a new UUID key will be created"""
        ...

    async def postal_codes_uuid_delete(
        self,
        uuid: StrictStr,
    ) -> PostalCode:
        """delete operation for /postal_codes/{uuid}"""
        ...

    async def postal_codes_uuid_get(
        self,
        uuid: StrictStr,
        name: Annotated[Optional[StrictStr], Field(description="Filter by name")],
    ) -> PostalCode:
        """Get a specific postal code from this collection"""
        ...

    async def postal_codes_uuid_head(
        self,
        uuid: StrictStr,
    ) -> None:
        """Determine the existence and size of this postal code"""
        ...

    async def postal_codes_uuid_name_delete(
        self,
        uuid: StrictStr,
    ) -> str:
        """delete operation for /postal_codes/{uuid}/name"""
        ...

    async def postal_codes_uuid_name_get(
        self,
        uuid: StrictStr,
        name: Annotated[Optional[StrictStr], Field(description="Filter by name")],
    ) -> str:
        """get operation for /postal_codes/{uuid}/name"""
        ...
