from app.cli.mods.processors import Input
from app.state import Stage, get_state
from app.readme.models import README_MODEL


class ReadmeProcessor:
    def process(self, input_: Input, step_number: int = 0) -> None:
        assert isinstance(input_.validated, int), "Invalid input."

        state = get_state()
        viewer = state.viewer

        match (input_.validated, input_.option_name):
            case (1, "RULES"):
                viewer.display(README_MODEL.get_text_by_order_number(0))
            case (2, "SETTINGS"):
                viewer.display(README_MODEL.get_text_by_order_number(1))
            case (3, "ADVANCED_OPTIONS"):
                viewer.display(README_MODEL.get_text_by_order_number(2))
            case (4, "AUTHORS"):
                viewer.display(README_MODEL.get_text_by_order_number(3))
            case (5, "BACK"):
                state.stage = Stage.MAIN_MENU
            case _:
                raise ValueError("Invalid input.")
