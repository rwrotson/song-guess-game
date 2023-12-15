from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel
from pydantic.fields import FieldInfo


@dataclass(frozen=True, slots=True)
class _FieldData:
    name: str
    value: FieldInfo


class OrderedModel(BaseModel):
    """
    Mixin for pydantic models that allows to get field by its order number.
    Counting starts from 0.
    """
    def field_name_by_order_number(self, order_number: int, /) -> str:
        return list(self.model_fields)[order_number]

    def field_by_order_number(self, order_number: int, /) -> _FieldData:
        field_name = self.field_name_by_order_number(order_number)
        return _FieldData(
            name=field_name,
            value=self.model_fields[field_name],
        )

    def order_number_by_field_name(self, field_name: str, /) -> int:
        return list(self.model_fields).index(field_name)


class FieldValidator:
    """
    Class that validates input for a field.
    """
    def __init__(self, model: BaseModel) -> None:
        self._model = model

    def validate_field(self, field_name: str, value: Any) -> None:
        self._model.__pydantic_validator__.validate_assignment(
            self._model.model_construct(),
            field_name=field_name,
            field_value=value,
        )

    def set_field(self, field_name: str, value: Any) -> None:
        field = self._model.__annotations__[field_name]
        setattr(self._model, field_name, field(value))
