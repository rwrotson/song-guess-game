from app.cli.core.models import MenuModel, MenuType
from app.cli.mods.representers import MenuRepresenter
from app.cli.mods.receivers import InputReceiver
from app.cli.mods.manglers import InputMangler
from app.cli.utils import StepCounter


class HomogenicMenu:
    """
    Menu in which steps are processed the same way.
    """

    __slots__ = ("_model", "_representer", "_receiver", "_mangler", "_counter", "_current_input")

    def __init__(
        self,
        *,
        model: MenuModel,
        representer: MenuRepresenter,
        receiver: InputReceiver,
        mangler: InputMangler,
    ):
        self._model = model
        self._representer = representer
        self._receiver = receiver
        self._mangler = mangler

        self._counter = StepCounter(steps_number=self._model.steps_number)
        self._current_input: str | None = None

    def _validate_coherance(self):
        if self._model.menu_type == MenuType.MIXED:
            raise ValueError("Menu model type must be HOMOGENIC.")

    def represent(self) -> str:
        current_step = self._counter.current_step
        menu_step = self._model.steps[current_step]
        return self._representer.represent(menu_step)

    def receive(self) -> str:
        return self._receiver.await_input()

    def mangle(self, input_text: str) -> str:
        mangle_kwargs = {}
        if self._model.menu_type == MenuType.OPTIONS:
            option_name = self._model.steps[self._counter.current_step].name
            mangle_kwargs["option_name"] = option_name
        elif self._model.menu_type == MenuType.TEXT_INPUT:
            field_name = self._model.steps[self._counter.current_step].name
            mangle_kwargs["field_name"] = field_name
        return self._mangler.mangle(input_text, **mangle_kwargs)


class HeterogenicMenu:
    """
    Menu in which each step can be processed differently.
    """
    __slots__ = ("_model", "_representer", "_receiver", "_mangler", "_counter", "_current_input")

    def __init__(
        self,
        *,
        model: MenuModel,
        representer: list[MenuRepresenter],
        receiver: list[InputReceiver],
        mangler: list[InputMangler],
    ):
        self._model = model
        self._representer = representer
        self._receiver = receiver
        self._mangler = mangler

        self._validate_coherance()

        self._counter = StepCounter(steps_number=self._model.steps_number)

    def _validate_coherance(self) -> None:
        steps = self._model.steps_number
        mods = self._representer, self._receiver, self._mangler
        repr_n, recv_n, mang_n = [len(mod) for mod in mods]
        if {steps, repr_n, recv_n, mang_n} != 1:
            raise ValueError(
                "The number of steps in the menu model and "
                "the number of menu components must be equal."
            )
        if self._model.menu_type != MenuType.MIXED:
            raise ValueError("Menu model is homogenic, use HomogenicMenu.")

    def represent(self) -> str:
        menu_step = self._model.steps[self._counter.current_step]
        representer = self._representer[self._counter.current_step]
        return representer.represent(menu_step)

    def receive(self) -> str:
        current_step = self._counter.current_step
        receiver = self._receiver[current_step]
        return receiver.await_input()

    def mangle(self, input_text: str) -> str:
        mangler = self._mangler[self._counter.current_step]
        menu_step = self._model.steps[self._counter.current_step]
        return mangler.mangle(input_text)
