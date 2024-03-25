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

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self


class UpdatePerson(BaseModel):
    """
    UpdatePerson
    """  # noqa: E501

    age: Optional[Any] = Field(default=None, description="The person's age")
    first_name: Optional[Any] = Field(default=None, description="The person's first name")
    hobbies: Optional[Any] = Field(default=None, description="The person's hobbies")
    last_name: Optional[Any] = Field(default=None, description="The person's last name")
    __properties: ClassVar[List[str]] = ["age", "first_name", "hobbies", "last_name"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of UpdatePerson from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if age (nullable) is None
        # and model_fields_set contains the field
        if self.age is None and "age" in self.model_fields_set:
            _dict["age"] = None

        # set to None if first_name (nullable) is None
        # and model_fields_set contains the field
        if self.first_name is None and "first_name" in self.model_fields_set:
            _dict["first_name"] = None

        # set to None if hobbies (nullable) is None
        # and model_fields_set contains the field
        if self.hobbies is None and "hobbies" in self.model_fields_set:
            _dict["hobbies"] = None

        # set to None if last_name (nullable) is None
        # and model_fields_set contains the field
        if self.last_name is None and "last_name" in self.model_fields_set:
            _dict["last_name"] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UpdatePerson from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "age": obj.get("age"),
                "first_name": obj.get("first_name"),
                "hobbies": obj.get("hobbies"),
                "last_name": obj.get("last_name"),
            }
        )
        return _obj
