# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from addressbook.models.create_postal_code import CreatePostalCode
from addressbook.models.postal_code import PostalCode
from addressbook.security_api import get_token_bearer_auth


class BasePostalCodesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BasePostalCodesApi.subclasses = BasePostalCodesApi.subclasses + (cls,)

    def postal_codes_get(
        self,
        name: str,
        limit: int,
        offset: int,
    ) -> List[PostalCode]:
        """List all postal codes in this collection"""
        ...

    def postal_codes_post(
        self,
        create_postal_code: CreatePostalCode,
        limit: int,
        offset: int,
    ) -> CreatePostalCode:
        """Create a new postal code in this collection, a new UUID key will be created"""
        ...

    def postal_codes_uuid_delete(
        self,
        uuid: str,
    ) -> PostalCode:
        """delete operation for /postal_codes/{uuid}"""
        ...

    def postal_codes_uuid_get(
        self,
        uuid: str,
        name: str,
    ) -> PostalCode:
        """Get a specific postal code from this collection"""
        ...

    def postal_codes_uuid_head(
        self,
        uuid: str,
    ) -> None:
        """Determine the existence and size of this postal code"""
        ...

    def postal_codes_uuid_name_delete(
        self,
        uuid: str,
    ) -> str:
        """delete operation for /postal_codes/{uuid}/name"""
        ...

    def postal_codes_uuid_name_get(
        self,
        uuid: str,
        name: str,
    ) -> str:
        """get operation for /postal_codes/{uuid}/name"""
        ...
