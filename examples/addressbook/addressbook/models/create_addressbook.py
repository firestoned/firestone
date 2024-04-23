# coding: utf-8

"""
    Example person and addressbook API

    Example person and addressbook API

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from addressbook.models.person import Person

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class CreateAddressbook(BaseModel):
    """
    CreateAddressbook
    """  # noqa: E501

    addrtype: StrictStr = Field(description="The address type, e.g. work or home")
    city: StrictStr = Field(description="The city of this address")
    country: StrictStr = Field(description="The country of this address")
    people: Optional[List[Any]] = Field(
        default=None, description="A list of people's names living there"
    )
    person: Optional[Person] = None
    state: StrictStr = Field(description="The state of this address")
    street: StrictStr = Field(description="The street and civic number of this address")
    __properties: ClassVar[List[str]] = [
        "addrtype",
        "city",
        "country",
        "people",
        "person",
        "state",
        "street",
    ]

    @field_validator("addrtype")
    def addrtype_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ("work", "home"):
            raise ValueError("must be one of enum values ('work', 'home')")
        return value

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of CreateAddressbook from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={},
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of person
        if self.person:
            _dict["person"] = self.person.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of CreateAddressbook from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "addrtype": obj.get("addrtype"),
                "city": obj.get("city"),
                "country": obj.get("country"),
                "people": obj.get("people"),
                "person": (
                    Person.from_dict(obj.get("person")) if obj.get("person") is not None else None
                ),
                "state": obj.get("state"),
                "street": obj.get("street"),
            }
        )
        return _obj
