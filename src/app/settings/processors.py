from app.main.processors import Processor


class SettingsSectionProcessor(Processor):
    def __init__(self):
        super().__init__()

        self._model = self._state.settings

    def _set_field(self, field_name: str, value: Any) -> None:
        field = self._model.__annotations__[field_name]
        setattr(self._model, field_name, field(value))

    def process(self, input_text: str, /) -> None:
        pass
