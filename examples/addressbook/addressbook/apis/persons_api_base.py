# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictInt, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from addressbook.models.create_person import CreatePerson
from addressbook.models.person import Person
from addressbook.models.update_person import UpdatePerson
from addressbook.security_api import get_token_bearer_auth


class BasePersonsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BasePersonsApi.subclasses = BasePersonsApi.subclasses + (cls,)

    async def persons_get(
        self,
        last_name: Annotated[Optional[StrictStr], Field(description="Filter by last name")],
        limit: Annotated[
            Optional[StrictInt], Field(description="Limit the number of responses back")
        ],
        offset: Annotated[
            Optional[StrictInt], Field(description="The offset to start returning resources")
        ],
    ) -> List[Person]:
        """List all persons in this collection"""
        ...

    async def persons_post(
        self,
        create_person: Annotated[CreatePerson, Field(description="The request body for /persons")],
        limit: Annotated[
            Optional[StrictInt], Field(description="Limit the number of responses back")
        ],
        offset: Annotated[
            Optional[StrictInt], Field(description="The offset to start returning resources")
        ],
    ) -> CreatePerson:
        """Create a new person in this collection, a new UUID key will be created"""
        ...

    async def persons_uuid_delete(
        self,
        uuid: StrictStr,
    ) -> Person:
        """delete operation for /persons/{uuid}"""
        ...

    async def persons_uuid_get(
        self,
        uuid: StrictStr,
        last_name: Annotated[Optional[StrictStr], Field(description="Filter by last name")],
    ) -> Person:
        """Get a specific person from this collection"""
        ...

    async def persons_uuid_head(
        self,
        uuid: StrictStr,
    ) -> None:
        """Determine the existence and size of this person"""
        ...

    async def persons_uuid_put(
        self,
        uuid: StrictStr,
        update_person: Annotated[
            UpdatePerson, Field(description="The request body for /persons/{uuid}")
        ],
    ) -> UpdatePerson:
        """Put a new person in this collection, with the given UUId key"""
        ...
