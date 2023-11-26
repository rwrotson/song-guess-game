from app.formatters import bold
from app.abstract.models import BaseModel, FieldData
from app.abstract.presenters import Presenter
from app.abstract.views import Viewer
from app.validators import TextInputValidator


class SettingsPresenter(Presenter):
    pass


class SettingsSectionPresenter(Presenter):
    def __init__(self, model: BaseModel, viewer: Viewer) -> None:
        super().__init__(model, viewer)

        self._current_step: int = 1
        self._current_field: FieldData = self._update_current_field()

    def _show_input_request(self) -> None:
        field = self._current_field.value
        description = bold(field.description)
        default = f"Leave empty for default value ({field.default})." if field.default else ""

        self._display(f"{description} {default}")

    def _validate_input(self) -> None:
        validator = TextInputValidator(model=self._model, field_name=self._current_field.name)
        if self._current_input != "" or (self._current_input == "" and not self._current_field.value.default):
            validator.validate(input_text=self._current_input)
        else:
            self._current_input = self._current_field.value.default

    def _mangle_input(self) -> None:
        print("\033[F\033[F")
        new_text = f"{bold(self._current_field.name)}: {self._current_input}"
        self._display(text=f"{new_text}\r")

    def _proceed_input(self) -> None:
        self._model.set_field(self._current_field.name, self._current_input)
        self._current_field = self._update_current_field()

    def _update_current_field(self) -> FieldData:
        return self._model.get_field_by_order_number(self._current_step)

    def run(self) -> None:
        for self._current_step in range(1, len(self._model.model_fields) + 1):
            super().run()
