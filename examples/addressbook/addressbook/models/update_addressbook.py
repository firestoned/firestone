# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401
from addressbook.models.person import Person


class UpdateAddressbook(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    UpdateAddressbook - a model defined in OpenAPI

        addrtype: The addrtype of this UpdateAddressbook [Optional].
        city: The city of this UpdateAddressbook [Optional].
        country: The country of this UpdateAddressbook [Optional].
        people: The people of this UpdateAddressbook [Optional].
        person: The person of this UpdateAddressbook [Optional].
        state: The state of this UpdateAddressbook [Optional].
        street: The street of this UpdateAddressbook [Optional].
    """

    addrtype: Optional[str] = Field(alias="addrtype", default=None)
    city: Optional[str] = Field(alias="city", default=None)
    country: Optional[str] = Field(alias="country", default=None)
    people: Optional[List[str]] = Field(alias="people", default=None)
    person: Optional[Person] = Field(alias="person", default=None)
    state: Optional[str] = Field(alias="state", default=None)
    street: Optional[str] = Field(alias="street", default=None)


UpdateAddressbook.update_forward_refs()
