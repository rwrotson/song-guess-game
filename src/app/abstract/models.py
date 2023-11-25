from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel as PydanticBaseModel
from pydantic.fields import FieldInfo


@dataclass(frozen=True, slots=True)
class FieldData:
    """
    Class for storing information about a pydantic field.
    """

    name: str
    value: FieldInfo


class BaseModel(PydanticBaseModel):
    """
    Base class for pydantic models in app, with useful helpers.
    """

    def get_field_by_order_number(self, order_number: int) -> FieldData:
        field_name = list(self.model_fields)[order_number - 1]
        return FieldData(
            name=field_name,
            value=self.model_fields[field_name],
        )

    def validate_field(self, field_name: str, value: Any) -> None:
        self.__pydantic_validator__.validate_assignment(
            self.model_construct(),
            field_name=field_name,
            field_value=value,
        )

    def set_field(self, field_name: str, value: Any) -> None:
        setattr(self, field_name, self.__annotations__[field_name](value))
