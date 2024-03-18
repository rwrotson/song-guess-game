from typing import Literal

SETTINGS_DICT = {
    "MAIN_SETTINGS": {
        "players_number": {
            "info": "number of players in the game",
            "constrains": ">=1",
            "default": "2",
        },
        "sample_duration": {
            "info": "duration of a sample from a song in seconds",
            "constrains": ">=0.1",
            "default": "1.0",
        },
        "infinite_repeats": {
            "info": "if True, player can repeat the sample infinite times",
            "default": "False",
        },
        "repeats_number": {
            "info": "number of allowed repeats in one round",
            "constrains": ">=1",
            "default": "5",
        },
        "clues_number": {
            "info": "number of clue samples",
            "constrains": ">=0",
            "default": "10",
        },
        "clues_strategy": {
            "info": "method of how next clue sample for the same song will be chosen",
            "constrains": "random_next|new_next",
            "default": "new_next",
        },
        "rounds_number": {
            "info": "number of songs each player tries to guess, number of rounds of the game",
            "comment": "can't be less than the number of songs in the smallest player's library",
            "constrains": ">=1",
            "default": "10",
        },
    },
    "PLAYERS_SETTINGS": {
        "name": {
            "info": "nickname of player",
        },
        "path": {
            "info": "path to library directory with all the audiofiles of a player",
        },
    },
    "DISPLAY_SETTINGS": {
        "color_enabled": {
            "info": "are color tags for text enabled in terminal",
            "default": "True",
        },
        "typing_enabled": {
            "info": "is text being typed letter by letter (True), or is is being typed instantly (False)",
            "default": "True",
        },
        "min_delay": {
            "info": "minimum delay between two letters being typed in seconds, if typing is enabled",
            "constrains": ">=0.0, <=0.5",
            "default": "0.001",
        },
        "max_delay": {
            "info": "maximum delay between two letters being typed in seconds, if typing is enabled",
            "constrains": ">=0.0, <=0.5",
            "default": "0.05",
        },
    },
    "SELECTION_SETTINGS": {
        "strategy": {
            "info": "how the songs are being chosen from player library",
            "options": {
                "naive": "select songs randomely from all audiofiles",
                "normalized_by_folder": "select songs evenly from each folder inside players library",
                "normalized_by_album": "select songs evenly from each album inside players library",
            },
        },
    },
    "SAMPLING_SETTINGS": {
        "from_": {
            "info": "from what second of the song the sample will be taken",
            "constrains": ">=0.0",
            "default": "0.0",
        },
        "to_finish": {
            "info": "from what second till the end of the song the sample will be taken",
            "constrains": ">=0.0",
            "default": "3.0",
        },
        "distance": {
            "info": "minimal distance between two samples from the same song in seconds",
            "constrains": ">=1.0",
            "default": "5.0",
        },
        "clues_quantity": {
            "info": "number of clue samples for the song",
            "constrains": ">=1, <=10",
            "default": "3",
        },
        "strategy": {
            "info": "method of how next clue sample for the same song will be chosen",
            "options": {
                "naive": "select next clue randomely from all clue samples",
                "normalized": "select next clue from all clue samples sequentially",
            },
            "default": "normalized",
        },
    },
    "PLAYBACK_BAR_SETTINGS": {
        "empty_char": {
            "info": "character that represents empty space in playback bar",
            "default": "░",
        },
        "full_char": {
            "info": "character that represents filled space in playback bar",
            "default": "█",
        },
        "space_char": {
            "info": "character that represents space between playback bar and time display",
            "default": "" "",
        },
        "bar_lenght": {
            "info": "length of playback bar in characters",
            "constrains": ">=20, <=100",
            "default": "50",
        },
        "update_frequency": {
            "info": "frequency of playback bar update in seconds",
            "constrains": ">=0.5, <=1.0",
            "default": "0.1",
        },
        "enable_flashing": {
            "info": "if True, playback bar will flash and blink",
            "default": "False",
        },
        "enable_question_mark": {
            "info": "show question sample mark in the progress bar",
            "default": "True",
        },
        "enable_clue_marks": {
            "info": "show clue samples marks in the progress bar",
            "default": "True",
        },
    },
    "EVALUATION_SETTINGS": {
        "full_answer": {
            "info": "points for full correct answer",
            "constrains": ">=0.0",
            "default": "1.0",
        },
        "half_answer": {
            "info": "points for half correct answer",
            "constrains": ">=0.0",
            "default": "0.5",
        },
        "no_answer": {
            "info": "points for no answer",
            "constrains": ">=0.0",
            "default": "0.0",
        },
        "wrong_answer": {
            "info": "points for wrong answer",
            "constrains": ">=0.0",
            "default": "0.0",
        },
        "clue_discount": {
            "info": "discount for points for each clue use",
            "constrains": ">=0.0, <=1.0",
            "default": "0.1",
        },
    },
    "SERVICE_PATHS_SETTINGS": {
        "config_path": {
            "info": "path to config file, where set settings are stored",
            "default": "config.yaml",
        },
        "game_pickle_path": {
            "info": "path to pickle file, where unfinished game state is stored",
            "default": "game.pickle",
        },
        "history_log_path": {
            "info": "path to history log file",
            "default": "history.log",
        },
    },
}


type SettingFieldDict = dict[str, str]
type SettingDict = dict[str, SettingFieldDict]

type SettingDictSection = Literal[
    "MAIN_SETTINGS",
    "PLAYERS_SETTINGS",
    "DISPLAY_SETTINGS",
    "SELECTION_SETTINGS",
    "SAMPLING_SETTINGS",
    "PLAYBACK_BAR_SETTINGS",
    "EVALUATION_SETTINGS",
    "SERVICE_PATHS_SETTINGS",
]


def represent_setting(section_name: SettingDict) -> str:
    result = "${b}" + section_name + ":${r}\n"
    for setting_field_name, setting_field in SETTINGS_DICT[section_name].items():
        fmt_setting_field_name = "\t" + "-- " + "${b}" + setting_field_name + "${r}"
        result += fmt_setting_field_name

        pad_n = 33
        spaces_number = pad_n - len(fmt_setting_field_name) - 1
        result += " " * spaces_number + ": " + setting_field["info"] + "\n"
        if "comment" in setting_field:
            result += " " * pad_n + "(${i}" + setting_field["comment"] + "${r})\n"
        if "options" in setting_field:
            for option_name, option in setting_field["options"].items():
                result += " " * pad_n + "-${i}" + option_name + "${r}: " + option + "\n"

        tech_info = ""
        if "constrains" in setting_field:
            tech_info += "(" + "${b}" + setting_field["constrains"] + "${r}"
        if "default" in setting_field:
            if not tech_info:
                tech_info += "("
            else:
                tech_info += ", "
            tech_info += "default" + ": ${b}" + setting_field["default"] + "${r})"
        if tech_info:
            result += " " * pad_n + tech_info + "\n"

    return result
