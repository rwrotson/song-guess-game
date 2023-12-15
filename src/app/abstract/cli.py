from typing import Protocol


class MenuRepresenter(Protocol):
    @staticmethod
    def represent(step_model: MenuStep) -> str:
        ...