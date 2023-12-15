from typing import Protocol


class InputReceiver(Protocol):
    def await_input(self, *, input_request_text: str | None = None) -> str:
        pass


class DefaultInputReceiver:
    @staticmethod
    def await_input(*, input_request_text: str | None = None) -> str:
        return input(input_request_text)

