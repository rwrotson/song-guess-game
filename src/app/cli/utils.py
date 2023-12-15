class StepCounter:
    """
    A class that keeps track of the current step number in the menu.
    """

    __slots__ = ("_current_step", "_steps_number")

    def __init__(self, steps_number: int):
        self._current_step = 0
        self._steps_number = steps_number

    @property
    def current_step(self) -> int:
        return self._current_step

    @property
    def steps_number(self) -> int:
        return self._steps_number

    def increment(self) -> None:
        self._current_step += 1
        if self._current_step == self._steps_number:
            raise ValueError(f"Upper limit of steps is {self._steps_number}.")

    def decrement(self) -> None:
        self._current_step -= 1
        if self._current_step < 0:
            raise ValueError(f"Lower limit of steps is 0.")

    def reset(self) -> None:
        self._current_step = 0
