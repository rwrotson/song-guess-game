from enum import StrEnum, auto

from app.abstract.models import BaseModel


class MainMenu(StrEnum):
    PLAY = auto()
    SETTINGS = auto()
    HELP = auto()
    EXIT = auto()


class SettingsMenu(StrEnum):
    MAIN_SETTINGS = auto()
    ADVANCED_SETTINGS = auto()
    SHOW_CURRENT_SETTINGS = auto()
    EDIT_CONFIG_FILE = auto()
    BACK = auto()


class Menu(BaseModel):
    type_: type[MainMenu] | type[SettingsMenu]

    @property
    def type_name(self) -> str:
        return self.type_.__name__

    @property
    def items(self) -> list[str]:
        return [item for item in self.type_]

    @property
    def items_number(self) -> int:
        return len(self.menu_items)

    def get_section_name_by_order_number(self, order_number: int) -> str:
        order_number -= 1

        if 0 <= order_number < self.items_number:
            return self.menu_items[order_number]

        raise ValueError("Invalid order number")
