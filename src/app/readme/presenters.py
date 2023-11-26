from app.abstract.presenters import Presenter
from app.abstract.views import Viewer, TypingDisabledViewer, TypingEnabledViewer
from app.formatters import bold
from app.readme.models import Readme
from app.validators import ChoiceInputValidator


class ReadmePresenter(Presenter):
    def __init__(self, model: Readme, viewer: Viewer) -> None:
        super().__init__(model, viewer)

        self.options_number = model.sections_number + 1

    def _show_input_request(self):
        request_text = "Enter the number of INFO you want to get:"
        for i in range(1, self.options_number + 1):
            section_name = self._model.get_section_name_by_order_number(i)
            request_text += f"\n\t{i}. {bold(section_name.upper())}"

        self._display(text=request_text)

    def _validate_input(self):
        validator = ChoiceInputValidator(max_number=self.options_number)
        validator.validate(self._current_input)

    def _mangle_input(self) -> None:
        print("\033[F\033[F")  # delete last two lines

        chosen_option = int(self._current_input)
        new_text = self._model.get_section_name_by_order_number(chosen_option)

        self._display(text=f"{bold(new_text.upper())}:\r")

    def _proceed_input(self) -> None:
        if (option_n := int(self._current_input)) <= self._model.sections_number:
            self._display(text=self._model.get_text_by_order_number(option_n))

    def _await_input_to_return(self):
        self._display(text="Press ENTER to continue...")
        input()

    def run(self) -> None:
        super().run()

        if not int(self._current_input) == self.options_number:
            self._await_input_to_return()
