# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401


class Person(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    Person - a model defined in OpenAPI

        age: The age of this Person [Optional].
        first_name: The first_name of this Person [Optional].
        hobbies: The hobbies of this Person [Optional].
        last_name: The last_name of this Person [Optional].
    """

    age: Optional[int] = Field(alias="age", default=None)
    first_name: Optional[str] = Field(alias="first_name", default=None)
    hobbies: Optional[List[str]] = Field(alias="hobbies", default=None)
    last_name: Optional[str] = Field(alias="last_name", default=None)


Person.update_forward_refs()
