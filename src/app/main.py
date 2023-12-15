import asyncio
from sys import exit

from app.formatters import separate_line
from app.state import GameState
from app.settings.models import Settings


async def game_loop():
    settings = Settings.load_from_file()
    game = GameState()
    viewer = get_viewer(settings)
    viewer.display(separate_line('Hello, welcome to THE GAME!'))

    while True:
        model = get_model(game_state)

        presenter = Presenter(model, viewer)

        presenter.show()
        presenter.get_input()

        try:
            presenter.validate()
        except Exception:
            viewer.display(separate_line('Invalid input. Please try again.'))
            continue

        presenter.update()


def main():
    try:
        asyncio.run(game_loop())

    except KeyboardInterrupt:
        exit(separate_line("OK, goodbye!"))


if __name__ == '__main__':
    main()
