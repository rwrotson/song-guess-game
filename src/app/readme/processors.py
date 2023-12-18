from app.main.state import State, Stage
from app.readme.models import ReadmeModel


class ReadmeProcessor:
    def __init__(self, state: State) -> None:
        self._model = ReadmeModel
        self._state = state

    def process(self, input_text: str) -> None:
        match input_text:
            case "1" | "RULES":
                return self._model.get_text_by_order_number(0)
            case "2" | "SETTINGS":
                return self._model.get_text_by_order_number(1)
            case "3" | "ADVANCED_SETTINGS":
                return self._model.get_text_by_order_number(2)
            case "4" | "AUTHORS":
                return self._model.get_text_by_order_number(3)
            case "5" | "BACK":
                self._state.stage = Stage.MAIN.MAIN_MENU
