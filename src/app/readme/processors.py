from app.readme.models import ReadmeModel


class ReadmeProcessor:
    def __init__(self):
        self.model = ReadmeModel

    def process(self, input_text: str) -> None:
        order_number = int(input_text)
        return self.model.get_text_by_order_number()

    def process2(self, input_text: str):
        match input_text:
            case "1" | "RULES":
                return self.model.get_text_by_order_number(0)
            case "2" | "SETTINGS":
                return self.model.get_text_by_order_number(1)
            case "3" | "ADVANCED_SETTINGS":
                return self.model.get_text_by_order_number(2)
            case "4" | "AUTHORS":
                return self.model.get_text_by_order_number(3)
            case "5" | "BACK":
                state.stage = Stage.MAIN.MAIN_MENU
