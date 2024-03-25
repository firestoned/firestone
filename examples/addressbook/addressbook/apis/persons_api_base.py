# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from addressbook.models.create_person import CreatePerson
from addressbook.models.person import Person
from addressbook.models.update_person import UpdatePerson
from addressbook.security_api import get_token_bearer_auth


class BasePersonsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BasePersonsApi.subclasses = BasePersonsApi.subclasses + (cls,)

    def persons_get(
        self,
        last_name: str,
        limit: int,
        offset: int,
    ) -> List[Person]:
        """List all persons in this collection"""
        ...

    def persons_post(
        self,
        create_person: CreatePerson,
        limit: int,
        offset: int,
    ) -> CreatePerson:
        """Create a new person in this collection, a new UUID key will be created"""
        ...

    def persons_uuid_age_delete(
        self,
        uuid: str,
    ) -> int:
        """delete operation for /persons/{uuid}/age"""
        ...

    def persons_uuid_age_get(
        self,
        uuid: str,
        last_name: str,
    ) -> int:
        """get operation for /persons/{uuid}/age"""
        ...

    def persons_uuid_age_head(
        self,
        uuid: str,
    ) -> None:
        """head operation for /persons/{uuid}/age"""
        ...

    def persons_uuid_age_put(
        self,
        uuid: str,
        body: int,
    ) -> int:
        """put operation for /persons/{uuid}/age"""
        ...

    def persons_uuid_delete(
        self,
        uuid: str,
    ) -> Person:
        """delete operation for /persons/{uuid}"""
        ...

    def persons_uuid_first_name_delete(
        self,
        uuid: str,
    ) -> str:
        """delete operation for /persons/{uuid}/first_name"""
        ...

    def persons_uuid_first_name_get(
        self,
        uuid: str,
        last_name: str,
    ) -> str:
        """get operation for /persons/{uuid}/first_name"""
        ...

    def persons_uuid_first_name_head(
        self,
        uuid: str,
    ) -> None:
        """head operation for /persons/{uuid}/first_name"""
        ...

    def persons_uuid_first_name_put(
        self,
        uuid: str,
        body: str,
    ) -> str:
        """put operation for /persons/{uuid}/first_name"""
        ...

    def persons_uuid_get(
        self,
        uuid: str,
        last_name: str,
    ) -> Person:
        """Get a specific person from this collection"""
        ...

    def persons_uuid_head(
        self,
        uuid: str,
    ) -> None:
        """Determine the existence and size of this person"""
        ...

    def persons_uuid_hobbies_delete(
        self,
        uuid: str,
    ) -> List[str]:
        """delete operation for /persons/{uuid}/hobbies"""
        ...

    def persons_uuid_hobbies_get(
        self,
        uuid: str,
        last_name: str,
    ) -> List[str]:
        """get operation for /persons/{uuid}/hobbies"""
        ...

    def persons_uuid_hobbies_head(
        self,
        uuid: str,
    ) -> None:
        """head operation for /persons/{uuid}/hobbies"""
        ...

    def persons_uuid_hobbies_put(
        self,
        uuid: str,
        request_body: List[str],
    ) -> List[str]:
        """put operation for /persons/{uuid}/hobbies"""
        ...

    def persons_uuid_last_name_delete(
        self,
        uuid: str,
    ) -> str:
        """delete operation for /persons/{uuid}/last_name"""
        ...

    def persons_uuid_last_name_get(
        self,
        uuid: str,
        last_name: str,
    ) -> str:
        """get operation for /persons/{uuid}/last_name"""
        ...

    def persons_uuid_last_name_head(
        self,
        uuid: str,
    ) -> None:
        """head operation for /persons/{uuid}/last_name"""
        ...

    def persons_uuid_last_name_put(
        self,
        uuid: str,
        body: str,
    ) -> str:
        """put operation for /persons/{uuid}/last_name"""
        ...

    def persons_uuid_put(
        self,
        uuid: str,
        update_person: UpdatePerson,
    ) -> UpdatePerson:
        """Put a new person in this collection, with the given UUId key"""
        ...
