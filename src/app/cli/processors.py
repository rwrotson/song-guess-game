from app.state import get_state, Stage
from app.settings import models
from app.settings.models import SettingsSection
from app.settings.presenters import SettingsSectionPresenter


state = get_state()


class MainMenuProcessor:
    def process(self, input_text: str) -> None:
        match input_text:
            case "1" | "PLAY":
                state.game.reset_game()
            case "2" | "SETTINGS":
                state.stage = Stage.MAIN.SETTINGS
            case "3" | "README":
                state.stage = Stage.MAIN.README
            case "4" | "EXIT":
                state.exit()
            case _:
                raise ValueError("Invalid input")


class SettingsMenuProcessor:
    @staticmethod
    def process(input_text: str) -> None:
        match input_text:
            case "1" | "MAIN_SETTINGS":
                state.stage = Stage.SETTINGS.MAIN_SETTINGS
            case "2" | "ADVANCED_SETTINGS":
                state.stage = Stage.SETTINGS.ADVANCED_SETTINGS
            case "3" | "SHOW_CURRENT_SETTINGS":
                ...
            case "4" | "EDIT_CONFIG_FILE":
                ...
            case "5" | "BACK":
                state.stage = Stage.MAIN.MAIN_MENU
            case _:
                raise ValueError("Invalid input")


def run_settings_configurator(settings_section: type[SettingsSection]) -> None:
    model = settings_section
    viewer = state.get_viewer()
    presenter = SettingsSectionPresenter(model=settings_section, viewer=viewer)
    presenter.run()


class MainSettingsProcessor:
    @staticmethod
    def process(input_text: str) -> None:
        match input_text:
            case "1" | "GAME_SETTINGS":
                ...
            case "2" | "PLAYER_SETTINGS":
                ...
            case "3" | "BACK":
                state.stage = Stage.MAIN.SETTINGS
            case _:
                raise ValueError("Invalid input")


class AdvancedSettingsProcessor:
    def process(self, input_text: str) -> None:
        match input_text:
            case "1" | "DISPLAY":
                self.run_settings_configurator(models.DisplaySettings)
            case "2" | "SELECTION":
                self.run_settings_configurator(models.SelectionSettings)
            case "3" | "SAMPLING":
                self.run_settings_configurator(models.SamplingSettings)
            case "4" | "PLAYBACK_BAR":
                self.run_settings_configurator(models.PlaybackBarSettings)
            case "5" | "EVALUATION":
                self.run_settings_configurator(models.EvaluationSettings)
            case "6" | "BACK":
                state.stage = Stage.MAIN.SETTINGS_MENU
            case _:
                raise ValueError("Invalid input")
