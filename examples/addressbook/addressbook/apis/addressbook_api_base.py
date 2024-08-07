# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from addressbook.models.addressbook import Addressbook
from addressbook.models.create_addressbook import CreateAddressbook
from addressbook.models.create_person import CreatePerson
from addressbook.models.person import Person
from addressbook.models.update_addressbook import UpdateAddressbook
from addressbook.models.update_person import UpdatePerson
from addressbook.security_api import get_token_bearer_auth


class BaseAddressbookApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAddressbookApi.subclasses = BaseAddressbookApi.subclasses + (cls,)

    def addressbook_address_key_addrtype_delete(
        self,
        address_key: str,
    ) -> str:
        """delete operation for /addressbook/{address_key}/addrtype"""
        ...

    def addressbook_address_key_addrtype_get(
        self,
        address_key: str,
        city: str,
    ) -> str:
        """get operation for /addressbook/{address_key}/addrtype"""
        ...

    def addressbook_address_key_addrtype_head(
        self,
        address_key: str,
    ) -> None:
        """head operation for /addressbook/{address_key}/addrtype"""
        ...

    def addressbook_address_key_addrtype_put(
        self,
        address_key: str,
        body: str,
    ) -> str:
        """put operation for /addressbook/{address_key}/addrtype"""
        ...

    def addressbook_address_key_city_delete(
        self,
        address_key: str,
    ) -> str:
        """delete operation for /addressbook/{address_key}/city"""
        ...

    def addressbook_address_key_city_get(
        self,
        address_key: str,
        city: str,
    ) -> str:
        """get operation for /addressbook/{address_key}/city"""
        ...

    def addressbook_address_key_city_head(
        self,
        address_key: str,
    ) -> None:
        """head operation for /addressbook/{address_key}/city"""
        ...

    def addressbook_address_key_city_put(
        self,
        address_key: str,
        body: str,
    ) -> str:
        """put operation for /addressbook/{address_key}/city"""
        ...

    def addressbook_address_key_country_delete(
        self,
        address_key: str,
    ) -> str:
        """delete operation for /addressbook/{address_key}/country"""
        ...

    def addressbook_address_key_country_get(
        self,
        address_key: str,
        city: str,
    ) -> str:
        """get operation for /addressbook/{address_key}/country"""
        ...

    def addressbook_address_key_country_head(
        self,
        address_key: str,
    ) -> None:
        """head operation for /addressbook/{address_key}/country"""
        ...

    def addressbook_address_key_country_put(
        self,
        address_key: str,
        body: str,
    ) -> str:
        """put operation for /addressbook/{address_key}/country"""
        ...

    def addressbook_address_key_delete(
        self,
        address_key: str,
    ) -> Addressbook:
        """Delete an address from this addressbook."""
        ...

    def addressbook_address_key_get(
        self,
        address_key: str,
        city: str,
    ) -> Addressbook:
        """Get a specific address from this addressbook."""
        ...

    def addressbook_address_key_head(
        self,
        address_key: str,
    ) -> None:
        """Determine the existence and size of this address."""
        ...

    def addressbook_address_key_is_valid_delete(
        self,
        address_key: str,
    ) -> bool:
        """delete operation for /addressbook/{address_key}/is_valid"""
        ...

    def addressbook_address_key_is_valid_get(
        self,
        address_key: str,
        city: str,
    ) -> bool:
        """get operation for /addressbook/{address_key}/is_valid"""
        ...

    def addressbook_address_key_is_valid_head(
        self,
        address_key: str,
    ) -> None:
        """head operation for /addressbook/{address_key}/is_valid"""
        ...

    def addressbook_address_key_is_valid_put(
        self,
        address_key: str,
        body: bool,
    ) -> bool:
        """put operation for /addressbook/{address_key}/is_valid"""
        ...

    def addressbook_address_key_people_delete(
        self,
        address_key: str,
    ) -> List[str]:
        """delete operation for /addressbook/{address_key}/people"""
        ...

    def addressbook_address_key_people_get(
        self,
        address_key: str,
        city: str,
    ) -> List[str]:
        """get operation for /addressbook/{address_key}/people"""
        ...

    def addressbook_address_key_people_head(
        self,
        address_key: str,
    ) -> None:
        """head operation for /addressbook/{address_key}/people"""
        ...

    def addressbook_address_key_people_put(
        self,
        address_key: str,
        request_body: List[str],
    ) -> List[str]:
        """put operation for /addressbook/{address_key}/people"""
        ...

    def addressbook_address_key_person_delete(
        self,
        address_key: str,
        limit: int,
        offset: int,
    ) -> Person:
        """delete operation for /addressbook/{address_key}/person"""
        ...

    def addressbook_address_key_person_get(
        self,
        address_key: str,
        last_name: str,
        limit: int,
        offset: int,
    ) -> List[Person]:
        """get operation for /addressbook/{address_key}/person"""
        ...

    def addressbook_address_key_person_head(
        self,
        address_key: str,
        limit: int,
        offset: int,
    ) -> None:
        """head operation for /addressbook/{address_key}/person"""
        ...

    def addressbook_address_key_person_patch(
        self,
        address_key: str,
        limit: int,
        offset: int,
    ) -> Person:
        """patch operation for /addressbook/{address_key}/person"""
        ...

    def addressbook_address_key_person_post(
        self,
        address_key: str,
        create_person: CreatePerson,
        limit: int,
        offset: int,
    ) -> CreatePerson:
        """post operation for /addressbook/{address_key}/person"""
        ...

    def addressbook_address_key_person_uuid_age_delete(
        self,
        address_key: str,
        uuid: str,
    ) -> int:
        """delete operation for /addressbook/{address_key}/person/{uuid}/age"""
        ...

    def addressbook_address_key_person_uuid_age_get(
        self,
        address_key: str,
        uuid: str,
        last_name: str,
    ) -> int:
        """get operation for /addressbook/{address_key}/person/{uuid}/age"""
        ...

    def addressbook_address_key_person_uuid_age_head(
        self,
        address_key: str,
        uuid: str,
    ) -> None:
        """head operation for /addressbook/{address_key}/person/{uuid}/age"""
        ...

    def addressbook_address_key_person_uuid_age_put(
        self,
        address_key: str,
        uuid: str,
        body: int,
    ) -> int:
        """put operation for /addressbook/{address_key}/person/{uuid}/age"""
        ...

    def addressbook_address_key_person_uuid_delete(
        self,
        address_key: str,
        uuid: str,
    ) -> Person:
        """delete operation for /addressbook/{address_key}/person/{uuid}"""
        ...

    def addressbook_address_key_person_uuid_first_name_delete(
        self,
        address_key: str,
        uuid: str,
    ) -> str:
        """delete operation for /addressbook/{address_key}/person/{uuid}/first_name"""
        ...

    def addressbook_address_key_person_uuid_first_name_get(
        self,
        address_key: str,
        uuid: str,
        last_name: str,
    ) -> str:
        """get operation for /addressbook/{address_key}/person/{uuid}/first_name"""
        ...

    def addressbook_address_key_person_uuid_first_name_head(
        self,
        address_key: str,
        uuid: str,
    ) -> None:
        """head operation for /addressbook/{address_key}/person/{uuid}/first_name"""
        ...

    def addressbook_address_key_person_uuid_first_name_put(
        self,
        address_key: str,
        uuid: str,
        body: str,
    ) -> str:
        """put operation for /addressbook/{address_key}/person/{uuid}/first_name"""
        ...

    def addressbook_address_key_person_uuid_get(
        self,
        address_key: str,
        uuid: str,
        last_name: str,
    ) -> Person:
        """get operation for /addressbook/{address_key}/person/{uuid}"""
        ...

    def addressbook_address_key_person_uuid_head(
        self,
        address_key: str,
        uuid: str,
    ) -> None:
        """head operation for /addressbook/{address_key}/person/{uuid}"""
        ...

    def addressbook_address_key_person_uuid_hobbies_delete(
        self,
        address_key: str,
        uuid: str,
    ) -> List[str]:
        """delete operation for /addressbook/{address_key}/person/{uuid}/hobbies"""
        ...

    def addressbook_address_key_person_uuid_hobbies_get(
        self,
        address_key: str,
        uuid: str,
        last_name: str,
    ) -> List[str]:
        """get operation for /addressbook/{address_key}/person/{uuid}/hobbies"""
        ...

    def addressbook_address_key_person_uuid_hobbies_head(
        self,
        address_key: str,
        uuid: str,
    ) -> None:
        """head operation for /addressbook/{address_key}/person/{uuid}/hobbies"""
        ...

    def addressbook_address_key_person_uuid_hobbies_put(
        self,
        address_key: str,
        uuid: str,
        request_body: List[str],
    ) -> List[str]:
        """put operation for /addressbook/{address_key}/person/{uuid}/hobbies"""
        ...

    def addressbook_address_key_person_uuid_last_name_delete(
        self,
        address_key: str,
        uuid: str,
    ) -> str:
        """delete operation for /addressbook/{address_key}/person/{uuid}/last_name"""
        ...

    def addressbook_address_key_person_uuid_last_name_get(
        self,
        address_key: str,
        uuid: str,
        last_name: str,
    ) -> str:
        """get operation for /addressbook/{address_key}/person/{uuid}/last_name"""
        ...

    def addressbook_address_key_person_uuid_last_name_head(
        self,
        address_key: str,
        uuid: str,
    ) -> None:
        """head operation for /addressbook/{address_key}/person/{uuid}/last_name"""
        ...

    def addressbook_address_key_person_uuid_last_name_put(
        self,
        address_key: str,
        uuid: str,
        body: str,
    ) -> str:
        """put operation for /addressbook/{address_key}/person/{uuid}/last_name"""
        ...

    def addressbook_address_key_person_uuid_patch(
        self,
        address_key: str,
        uuid: str,
    ) -> Person:
        """patch operation for /addressbook/{address_key}/person/{uuid}"""
        ...

    def addressbook_address_key_person_uuid_put(
        self,
        address_key: str,
        uuid: str,
        update_person: UpdatePerson,
    ) -> UpdatePerson:
        """put operation for /addressbook/{address_key}/person/{uuid}"""
        ...

    def addressbook_address_key_put(
        self,
        address_key: str,
        update_addressbook: UpdateAddressbook,
    ) -> UpdateAddressbook:
        """Update an existing address in this addressbook, with the given address key."""
        ...

    def addressbook_address_key_state_delete(
        self,
        address_key: str,
    ) -> str:
        """delete operation for /addressbook/{address_key}/state"""
        ...

    def addressbook_address_key_state_get(
        self,
        address_key: str,
        city: str,
    ) -> str:
        """get operation for /addressbook/{address_key}/state"""
        ...

    def addressbook_address_key_state_head(
        self,
        address_key: str,
    ) -> None:
        """head operation for /addressbook/{address_key}/state"""
        ...

    def addressbook_address_key_state_put(
        self,
        address_key: str,
        body: str,
    ) -> str:
        """put operation for /addressbook/{address_key}/state"""
        ...

    def addressbook_address_key_street_delete(
        self,
        address_key: str,
    ) -> str:
        """delete operation for /addressbook/{address_key}/street"""
        ...

    def addressbook_address_key_street_get(
        self,
        address_key: str,
        city: str,
    ) -> str:
        """get operation for /addressbook/{address_key}/street"""
        ...

    def addressbook_address_key_street_head(
        self,
        address_key: str,
    ) -> None:
        """head operation for /addressbook/{address_key}/street"""
        ...

    def addressbook_address_key_street_put(
        self,
        address_key: str,
        body: str,
    ) -> str:
        """put operation for /addressbook/{address_key}/street"""
        ...

    def addressbook_get(
        self,
        city: str,
        limit: int,
        offset: int,
    ) -> List[Addressbook]:
        """List all addresses in this addressbook."""
        ...

    def addressbook_post(
        self,
        create_addressbook: CreateAddressbook,
        limit: int,
        offset: int,
    ) -> CreateAddressbook:
        """Create a new address in this addressbook, a new address key will be created."""
        ...
