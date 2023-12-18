import asyncio
from sys import exit

from app.formatters import separate_line
from app.main.presenters import presenter_factory
from app.main.state import get_state


async def game_loop():
    state = get_state()
    viewer = state.viewers.default_viewer
    viewer.display(separate_line('Hello, welcome to THE GAME!'))

    while True:
        presenter = presenter_factory(state)

        presenter.prepare()

        try:
            presenter.validate()
        except IncorrectInputError as e:
            viewer.display(separate_line('Invalid input. Please try again.'))
            continue
        else:
            presenter.process()


def main():
    try:
        asyncio.run(game_loop())

    except KeyboardInterrupt:
        exit(separate_line("OK, goodbye!"))


if __name__ == '__main__':
    main()
