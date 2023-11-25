from functools import cached_property

from app.abstract.models import BaseModel
from app.readme.texts import README_TEXTS


class Readme(BaseModel):
    def __init__(self) -> None:
        super().__init__()
        self._texts = README_TEXTS

    @cached_property
    def sections_number(self) -> int:
        return len(self._texts)

    def get_section_name_by_order_number(self, order_number: int) -> str:
        order_number -= 1

        if 0 <= order_number < self.sections_number:
            return tuple(self._texts.keys())[order_number]
        elif order_number == self.sections_number:
            return "BACK"

        raise ValueError("Invalid order number")

    def get_text_by_order_number(self, order_number: int) -> str:
        order_number -= 1

        if 0 <= order_number < self.sections_number:
            return tuple(self._texts.values())[order_number]

        raise ValueError("Invalid order number")
