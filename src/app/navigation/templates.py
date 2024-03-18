import os

from app.cli.models import MenuStep
from app.state import get_state


def make_main_menu_step():
    state = get_state()

    resume_option = []
    game_pickle_path = state.settings.service_paths.game_pickle_path
    if os.path.exists(game_pickle_path):
        resume_option.append("resume")

    libraries_stats_option = []
    players = state.settings.players
    if any([player.path != "" for player in players]):
        libraries_stats_option.append("libraries_stats")

    return MenuStep(
        name="MainMenu",
        prompt="Select option with number input:",
        options=[
            "play",
            *resume_option,
            "settings",
            *libraries_stats_option,
            "readme",
            "exit",
        ],
    )


SETTINGS_MENU = MenuStep(
    name="SettingsMenu",
    prompt=None,
    options=[
        "main_settings",
        "advanced_settings",
        "show_current_settings",
        "edit_config_file",
        "set_default_settings",
        "back",
    ],
)


def make_libraries_stats_step():
    state = get_state()
    game_pickle_path = state.settings.service_paths.game_pickle_path
    players = state.settings.players

    options = []
    is_prev_game = os.path.exists(game_pickle_path)
    is_next_game = any([player.path != "" for player in players])
    if is_prev_game and is_next_game:
        options = [
            "next_short_stats",
            "next_extended_stats",
            "previous_short_stats",
            "previous_extended_stats",
        ]
    elif is_prev_game:
        options = ["previous_short_stats", "previous_extended_stats"]
    elif is_next_game:
        options = ["short_stats", "extended_stats"]

    return MenuStep(
        name="LibrariesStats",
        prompt=None,
        options=[
            *options,
            "back",
        ],
    )


MAIN_SETTINGS_MENU = MenuStep(
    name="MainSettingsMenu",
    prompt="Select settings menu section:",
    options=[
        "game",
        "players",
        "back",
    ],
)


ADVANCED_SETTINGS_MENU = MenuStep(
    name="AdvancedSettingsMenu",
    prompt="Select settings menu section:",
    options=[
        "display",
        "selection",
        "sampling",
        "playback_bar",
        "evaluation",
        "service_paths",
        "back",
    ],
)


def make_players_menu_step():
    state = get_state()

    pl_number = state.settings.game.players_number
    pl_names = [player.name for player in state.settings.players]
    pl_names.extend(["" for _ in range(pl_number - len(pl_names))])
    pl_options = [f"player {i + 1} ({pl_names[i]})" for i in range(pl_number)]

    return MenuStep(
        name="Players",
        prompt="Choose player:",
        options=[
            *pl_options,
            "back",
        ],
    )
