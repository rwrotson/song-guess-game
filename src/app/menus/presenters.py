import sys
from typing import Callable

from app.abstract.presenters import Presenter
from app.abstract.views import Viewer
from app.formatters import bold
from app.menus.models import Menu
from app.settings.models import get_settings
from app.state import get_state, Stage
from app.validators import ChoiceInputValidator


class MenuPresenter(Presenter):
    def __init__(self, model: Menu, viewer: Viewer) -> None:
        super().__init__(model, viewer)

    def _show_input_request(self):
        request_text = "Enter the number of OPTION you want to choose:"
        for i in range(1, self._model.items_number + 1):
            section_name = self._model.get_section_name_by_order_number(i)
            request_text += f"\n\t{i}. {bold(section_name.upper())}"

        self._display(text=request_text)

    def _validate_input(self):
        validator = ChoiceInputValidator(self._model.items_number + 1)
        validator.validate(self._current_input)

    def _mangle_input(self) -> None:
        print("\033[F\033[F")  # delete last two lines

        chosen_option = int(self._current_input)
        new_text = self._model.get_section_name_by_order_number(chosen_option)

        self._display(text=f"{bold(new_text.upper())}:\r")

    def _proceed_input(self) -> None:
        def get_input_processor(type_: Menu) -> Callable[[str, Viewer], None]:
            input_processor_factory = {
                Menu.MAIN_MENU: proceed_main_menu_input,
                Menu.SETTINGS_MENU: proceed_settings_menu_input,
            }
            return input_processor_factory[type_]

        processor_func = get_input_processor(self._model.type_)
        processor_func(self._current_input, self._viewer)


def proceed_main_menu_input(input_: str, viewer: Viewer) -> None:
    state = get_state()

    match input_:
        case "1":
            state.stage = Stage.READY_TO_PLAY
        case "2":
            state.stage = Stage.SETTINGS_MENU
        case "3":
            state.stage = Stage.README
        case "4":
            viewer.display(text="Goodbye! Hope to see you again!")
            sys.exit()
        case _:
            raise ValueError("Invalid input")


def proceed_settings_menu_input(input_: str, viewer: Viewer) -> None:
    state = get_state()

    match input_:
        case "1":
            state.stage = Stage.MAIN_SETTINGS
        case "2":
            state.stage = Stage.ADVANCED_SETTINGS
        case "3":
            settings = get_settings()
            viewer.display(text=settings.config_file_as_str)
        case "4":
            settings = get_settings()
            settings.edit_config_file()
        case "5":
            state.stage = Stage.MAIN_MENU
        case _:
            raise ValueError("Invalid input")
