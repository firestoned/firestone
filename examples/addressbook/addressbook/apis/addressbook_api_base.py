# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Any, List, Optional
from typing_extensions import Annotated
from addressbook.models.addressbook import Addressbook
from addressbook.models.create_addressbook import CreateAddressbook
from addressbook.models.create_person import CreatePerson
from addressbook.models.person import Person
from addressbook.models.update_addressbook import UpdateAddressbook


class BaseAddressbookApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAddressbookApi.subclasses = BaseAddressbookApi.subclasses + (cls,)

    async def addressbook_address_key_addrtype_delete(
        self,
        address_key: StrictStr,
    ) -> str:
        """delete operation for /addressbook/{address_key}/addrtype"""
        ...

    async def addressbook_address_key_addrtype_get(
        self,
        address_key: StrictStr,
        city: Annotated[Optional[StrictStr], Field(description="Filter by city name")],
    ) -> str:
        """get operation for /addressbook/{address_key}/addrtype"""
        ...

    async def addressbook_address_key_addrtype_head(
        self,
        address_key: StrictStr,
    ) -> None:
        """head operation for /addressbook/{address_key}/addrtype"""
        ...

    async def addressbook_address_key_addrtype_put(
        self,
        address_key: StrictStr,
        body: Annotated[
            StrictStr, Field(description="The request body for /addressbook/{address_key}/addrtype")
        ],
    ) -> str:
        """put operation for /addressbook/{address_key}/addrtype"""
        ...

    async def addressbook_address_key_city_delete(
        self,
        address_key: StrictStr,
    ) -> str:
        """delete operation for /addressbook/{address_key}/city"""
        ...

    async def addressbook_address_key_city_get(
        self,
        address_key: StrictStr,
        city: Annotated[Optional[StrictStr], Field(description="Filter by city name")],
    ) -> str:
        """get operation for /addressbook/{address_key}/city"""
        ...

    async def addressbook_address_key_city_head(
        self,
        address_key: StrictStr,
    ) -> None:
        """head operation for /addressbook/{address_key}/city"""
        ...

    async def addressbook_address_key_city_put(
        self,
        address_key: StrictStr,
        body: Annotated[
            StrictStr, Field(description="The request body for /addressbook/{address_key}/city")
        ],
    ) -> str:
        """put operation for /addressbook/{address_key}/city"""
        ...

    async def addressbook_address_key_country_delete(
        self,
        address_key: StrictStr,
    ) -> str:
        """delete operation for /addressbook/{address_key}/country"""
        ...

    async def addressbook_address_key_country_get(
        self,
        address_key: StrictStr,
        city: Annotated[Optional[StrictStr], Field(description="Filter by city name")],
    ) -> str:
        """get operation for /addressbook/{address_key}/country"""
        ...

    async def addressbook_address_key_country_head(
        self,
        address_key: StrictStr,
    ) -> None:
        """head operation for /addressbook/{address_key}/country"""
        ...

    async def addressbook_address_key_country_put(
        self,
        address_key: StrictStr,
        body: Annotated[
            StrictStr, Field(description="The request body for /addressbook/{address_key}/country")
        ],
    ) -> str:
        """put operation for /addressbook/{address_key}/country"""
        ...

    async def addressbook_address_key_delete(
        self,
        address_key: StrictStr,
    ) -> Addressbook:
        """Delete an address from this addressbook."""
        ...

    async def addressbook_address_key_get(
        self,
        address_key: StrictStr,
        city: Annotated[Optional[StrictStr], Field(description="Filter by city name")],
    ) -> Addressbook:
        """Get a specific address from this addressbook."""
        ...

    async def addressbook_address_key_head(
        self,
        address_key: StrictStr,
    ) -> None:
        """Determine the existence and size of this address."""
        ...

    async def addressbook_address_key_is_valid_delete(
        self,
        address_key: StrictStr,
    ) -> bool:
        """delete operation for /addressbook/{address_key}/is_valid"""
        ...

    async def addressbook_address_key_is_valid_get(
        self,
        address_key: StrictStr,
        city: Annotated[Optional[StrictStr], Field(description="Filter by city name")],
    ) -> bool:
        """get operation for /addressbook/{address_key}/is_valid"""
        ...

    async def addressbook_address_key_is_valid_head(
        self,
        address_key: StrictStr,
    ) -> None:
        """head operation for /addressbook/{address_key}/is_valid"""
        ...

    async def addressbook_address_key_is_valid_put(
        self,
        address_key: StrictStr,
        body: Annotated[
            StrictBool,
            Field(description="The request body for /addressbook/{address_key}/is_valid"),
        ],
    ) -> bool:
        """put operation for /addressbook/{address_key}/is_valid"""
        ...

    async def addressbook_address_key_people_delete(
        self,
        address_key: StrictStr,
    ) -> List[str]:
        """delete operation for /addressbook/{address_key}/people"""
        ...

    async def addressbook_address_key_people_get(
        self,
        address_key: StrictStr,
        city: Annotated[Optional[StrictStr], Field(description="Filter by city name")],
    ) -> List[str]:
        """get operation for /addressbook/{address_key}/people"""
        ...

    async def addressbook_address_key_people_head(
        self,
        address_key: StrictStr,
    ) -> None:
        """head operation for /addressbook/{address_key}/people"""
        ...

    async def addressbook_address_key_people_put(
        self,
        address_key: StrictStr,
        request_body: Annotated[
            List[StrictStr],
            Field(description="The request body for /addressbook/{address_key}/people"),
        ],
    ) -> List[str]:
        """put operation for /addressbook/{address_key}/people"""
        ...

    async def addressbook_address_key_person_delete(
        self,
        address_key: StrictStr,
        limit: Annotated[
            Optional[StrictInt], Field(description="Limit the number of responses back")
        ],
        offset: Annotated[
            Optional[StrictInt], Field(description="The offset to start returning resources")
        ],
    ) -> Person:
        """delete operation for /addressbook/{address_key}/person"""
        ...

    async def addressbook_address_key_person_get(
        self,
        address_key: StrictStr,
        last_name: Annotated[Optional[StrictStr], Field(description="Filter by last name")],
        limit: Annotated[
            Optional[StrictInt], Field(description="Limit the number of responses back")
        ],
        offset: Annotated[
            Optional[StrictInt], Field(description="The offset to start returning resources")
        ],
    ) -> List[Person]:
        """get operation for /addressbook/{address_key}/person"""
        ...

    async def addressbook_address_key_person_head(
        self,
        address_key: StrictStr,
        limit: Annotated[
            Optional[StrictInt], Field(description="Limit the number of responses back")
        ],
        offset: Annotated[
            Optional[StrictInt], Field(description="The offset to start returning resources")
        ],
    ) -> None:
        """head operation for /addressbook/{address_key}/person"""
        ...

    async def addressbook_address_key_person_patch(
        self,
        address_key: StrictStr,
        limit: Annotated[
            Optional[StrictInt], Field(description="Limit the number of responses back")
        ],
        offset: Annotated[
            Optional[StrictInt], Field(description="The offset to start returning resources")
        ],
    ) -> Person:
        """patch operation for /addressbook/{address_key}/person"""
        ...

    async def addressbook_address_key_person_post(
        self,
        address_key: StrictStr,
        create_person: Annotated[
            CreatePerson,
            Field(description="The request body for /addressbook/{address_key}/person"),
        ],
        limit: Annotated[
            Optional[StrictInt], Field(description="Limit the number of responses back")
        ],
        offset: Annotated[
            Optional[StrictInt], Field(description="The offset to start returning resources")
        ],
    ) -> CreatePerson:
        """post operation for /addressbook/{address_key}/person"""
        ...

    async def addressbook_address_key_put(
        self,
        address_key: StrictStr,
        update_addressbook: Annotated[
            UpdateAddressbook, Field(description="The request body for /addressbook/{address_key}")
        ],
    ) -> UpdateAddressbook:
        """Update an existing address in this addressbook, with the given address key."""
        ...

    async def addressbook_address_key_state_delete(
        self,
        address_key: StrictStr,
    ) -> str:
        """delete operation for /addressbook/{address_key}/state"""
        ...

    async def addressbook_address_key_state_get(
        self,
        address_key: StrictStr,
        city: Annotated[Optional[StrictStr], Field(description="Filter by city name")],
    ) -> str:
        """get operation for /addressbook/{address_key}/state"""
        ...

    async def addressbook_address_key_state_head(
        self,
        address_key: StrictStr,
    ) -> None:
        """head operation for /addressbook/{address_key}/state"""
        ...

    async def addressbook_address_key_state_put(
        self,
        address_key: StrictStr,
        body: Annotated[
            StrictStr, Field(description="The request body for /addressbook/{address_key}/state")
        ],
    ) -> str:
        """put operation for /addressbook/{address_key}/state"""
        ...

    async def addressbook_address_key_street_delete(
        self,
        address_key: StrictStr,
    ) -> str:
        """delete operation for /addressbook/{address_key}/street"""
        ...

    async def addressbook_address_key_street_get(
        self,
        address_key: StrictStr,
        city: Annotated[Optional[StrictStr], Field(description="Filter by city name")],
    ) -> str:
        """get operation for /addressbook/{address_key}/street"""
        ...

    async def addressbook_address_key_street_head(
        self,
        address_key: StrictStr,
    ) -> None:
        """head operation for /addressbook/{address_key}/street"""
        ...

    async def addressbook_address_key_street_put(
        self,
        address_key: StrictStr,
        body: Annotated[
            StrictStr, Field(description="The request body for /addressbook/{address_key}/street")
        ],
    ) -> str:
        """put operation for /addressbook/{address_key}/street"""
        ...

    async def addressbook_get(
        self,
        city: Annotated[Optional[StrictStr], Field(description="Filter by city name")],
        limit: Annotated[
            Optional[StrictInt], Field(description="Limit the number of responses back")
        ],
        offset: Annotated[
            Optional[StrictInt], Field(description="The offset to start returning resources")
        ],
    ) -> List[Addressbook]:
        """List all addresses in this addressbook."""
        ...

    async def addressbook_post(
        self,
        create_addressbook: Annotated[
            CreateAddressbook, Field(description="The request body for /addressbook")
        ],
        limit: Annotated[
            Optional[StrictInt], Field(description="Limit the number of responses back")
        ],
        offset: Annotated[
            Optional[StrictInt], Field(description="The offset to start returning resources")
        ],
    ) -> CreateAddressbook:
        """Create a new address in this addressbook, a new address key will be created."""
        ...
