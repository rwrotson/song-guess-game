from pydantic import ValidationError

from app.formatters import bold
from app.settings.models import SettingsSection, FieldData
from app.views import Viewer


class SettingsPresenter:
    def __init__(self, model: SettingsSection, viewer: Viewer) -> None:
        self._model = model
        self._viewer = viewer

        self._current_step: int = 1
        self._field: FieldData = self._model.get_field_by_order_number(self._current_step)

        self._input: str | None = None

    def _show(self, text: str) -> None:
        self._viewer.display(f"\n{text}\n")

    def show_current_state(self) -> None:
        field = self._field.value
        description = bold(field.description)
        default = f"Leave empty for default value ({field.default})." if field.default else ""

        self._show(f"{description} {default}")

    def validate(self) -> None:
        if (self._input != "" and self._field.value.default) or (self._input == "" and not self._field.value.default):
            self._model.validate_field(field_name=self._field.name, value=self._input)
        else:
            self._input = self._field.value.default

    def run(self) -> SettingsSection:
        for self._current_step in range(1, len(self._model.model_fields) + 1):
            self._field = self._model.get_field_by_order_number(self._current_step)
            self.show_current_state()
            while True:
                self._input = input()
                try:
                    self.validate()
                except ValidationError as e:
                    msg = f"{e.errors()[0]['msg']}. {bold('Try again.')}"
                    self._show(msg)
                else:
                    self._model.set_field(self._field.name, self._input)
                    break
        return self._model
