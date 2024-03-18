from sys import exit

from app.cli.exceptions import InvalidInputError
from app.navigation.factories import menu_factory
from app.state import get_state, Stage


def game_loop():
    state = get_state()
    menu = menu_factory(state)

    step_number = 0
    while step_number < menu.steps_number:
        menu_text = menu.represent(step_number=step_number)
        state.viewer.display(menu_text)

        input_text = menu.receive()

        try:
            validated_input = menu.validate(
                input_text,
                step_number=step_number,
            )

        except InvalidInputError as e:
            msg = f"{e}. Try again."
            state.viewer.display(msg + "\n")
            continue

        else:
            option_name = None
            menu_step_options = menu[step_number].options
            if menu_step_options and isinstance(validated_input, int):
                option_name = menu_step_options[validated_input - 1]

            mangled_text = menu.mangle(
                str(validated_input),
                option_name=option_name,
                step_number=step_number,
            )
            state.viewer.print(mangled_text)

            menu.process(
                raw=input_text,
                validated=validated_input,
                option_name=option_name,
                step_number=step_number,
            )

            step_number += 1


def main():
    try:
        while True:
            game_loop()

    except KeyboardInterrupt:
        state = get_state()
        if state.stage in Stage.MAIN_SETTINGS.value:
            state.stage = Stage.SETTINGS.value.MAIN_SETTINGS
            main()
        elif state.stage in Stage.ADVANCED_SETTINGS.value:
            state.stage = Stage.SETTINGS.value.ADVANCED_SETTINGS
            main()
        else:
            exit("\nOK, goodbye!\n")


def entrypoint():
    state = get_state()
    state.viewer.display("Hello, welcome to THE GAME!\n\n")

    main()


if __name__ == "__main__":
    entrypoint()
