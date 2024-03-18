from typing import Any

from app.cli.mods.processors import Input
from app.state import get_state
from app.settings.models import SettingsSection


class SettingsSectionProcessor:
    def __init__(self, settings_section: SettingsSection):
        self._model = settings_section

    def _field_name_by_order_number(self, order_number: int, /) -> str:
        return list(self._model.model_fields)[order_number]

    def _set_field(self, field_name: str, value: Any) -> None:
        field = self._model.__annotations__[field_name]
        setattr(self._model, field_name, field(value))

    def process(self, input_: Input, step_number: int = 0) -> None:
        field_name = self._field_name_by_order_number(step_number)
        self._set_field(field_name, input_.validated)

        if step_number == self._model.fields_number - 1:
            state = get_state()
            state.stage = state.previous_stage

            state.settings.save_to_file()
