# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401
from addressbook.models.person import Person


class CreateAddressbook(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    CreateAddressbook - a model defined in OpenAPI

        addrtype: The addrtype of this CreateAddressbook.
        city: The city of this CreateAddressbook.
        country: The country of this CreateAddressbook.
        people: The people of this CreateAddressbook [Optional].
        person: The person of this CreateAddressbook [Optional].
        state: The state of this CreateAddressbook.
        street: The street of this CreateAddressbook.
    """

    addrtype: str = Field(alias="addrtype")
    city: str = Field(alias="city")
    country: str = Field(alias="country")
    people: Optional[List[str]] = Field(alias="people", default=None)
    person: Optional[Person] = Field(alias="person", default=None)
    state: str = Field(alias="state")
    street: str = Field(alias="street")


CreateAddressbook.update_forward_refs()
