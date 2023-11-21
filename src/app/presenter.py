from typing import Any, Protocol

from pydantic import BaseModel

from app.views import Viewer


class Presenter(Protocol):
    # Game: 1) question 2) answer 3) evaluation
    # Settings: 1) 1st_field, 2) 2nd_field, 3) 3rd_field

    input: Any | None = None
    next_state: "Presenter | None" = None

    def __init__(self, model: BaseModel, viewer: Viewer) -> None:
        ...

    def show(self) -> None:
        ...

    def get_input(self) -> None:
        ...

    def validate(self) -> None:
        ...

    def update_state(self) -> None:
        ...


class GamePresenter(Protocol):
    def __init__(self, menu: "Game") -> None:
        ...

    def show(self) -> None:
        ...

    def show_current_state(self) -> None:
        ...

    def show_results(self) -> None:
        ...


class ReadmePresenter(Protocol):
    def __init__(self, menu: "Readme") -> None:
        ...

    def show(self) -> None:
        ...

    def show_current_state(self) -> None:
        ...

    def show_results(self) -> None:
        ...
