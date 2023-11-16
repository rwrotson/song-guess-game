from typing import Any, Protocol


class GamePresenter(Protocol):
    def __init__(self, menu: "Game") -> None:
        ...

    def show(self) -> None:
        ...

    def show_current_state(self) -> None:
        ...

    def show_results(self) -> None:
        ...


class SettingsPresenter(Protocol):
    step: int = 1

    def __init__(self, menu: "Settings") -> None:
        ...

    def show(self) -> None:
        ...

    def show_current_state(self) -> None:
        ...

    def show_results(self) -> None:
        ...


class SettingPresenter(Protocol):
    def __init__(self, menu: "Setting") -> None:
        ...

    def show(self) -> None:
        ...

    def show_current_state(self) -> None:
        ...

    def show_results(self) -> None:
        ...


# Game: 1) question 2) answer 3) evaluation
# Settings: 1) first_field, 2) 2nd_field, 3) 3rd_field


class Presenter(Protocol):
    input: Any | None = None
    next_state: "Presenter | None" = None

    def __init__(self, model: "Model", viewer: "Viewer") -> None:
        ...

    def show(self) -> None:
        ...

    def get_input(self) -> None:
        ...

    def validate(self) -> None:
        ...

    def update_state(self) -> None:
        ...
