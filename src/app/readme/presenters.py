from app.abstract.presenters import Presenter
from app.abstract.views import Viewer, TypingDisabledViewer
from app.readme.models import Readme
from app.validators import ChoiceInputValidator


class ReadmePresenter(Presenter):
    def __init__(self, model: Readme, viewer: Viewer) -> None:
        super().__init__(model, viewer)

        self.options_number = model.sections_number + 1

    def _show_input_request(self):
        request_text = "Enter the number of INFO you want to get:"
        for i in range(1, self.options_number + 1):
            request_text += f"\n\t{i}. {self._model.get_section_name_by_order_number(i).upper()}"

        self._display(text=request_text)

    def _validate_input(self):
        validator = ChoiceInputValidator(max_number=self.options_number)
        validator.validate(self._current_input)

    def _await_input_to_return(self):
        self._display(text="Press ENTER to continue...")
        input()

    def run(self) -> None:
        self._show_input_request()
        self._receive_input()

        self._display(
            text=self._model.get_text_by_order_number(int(self._current_input))
        )

        self._await_input_to_return()


r0 = Readme()
v = TypingDisabledViewer()
r = ReadmePresenter(r0, v)

r.run()
