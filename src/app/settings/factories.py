from app.main.state import State, Stage
from app.settings.models import SettingsSection


stage_to_settings_section_mapping = {
    Stage.MAIN_SETTINGS.GAME_SETTINGS: models.GameSettings,
    Stage.MAIN_SETTINGS.PLAYER_SETTINGS: models.PlayerSettings,
    Stage.ADVANCED_SETTINGS.DISPLAY: models.DisplaySettings,
    Stage.ADVANCED_SETTINGS.SELECTION: models.SelectionSettings,
    Stage.ADVANCED_SETTINGS.SAMPLING: models.SamplingSettings,
    Stage.ADVANCED_SETTINGS.PLAYBACK_BAR: models.PlaybackBarSettings,
    Stage.ADVANCED_SETTINGS.EVALUATION: models.EvaluationSettings,
}


def settings_factory(state: State) -> SettingsSection:
    stage = state.stage
    settings = state.settings

    stage_to_settings_section_mapping = {
        Stage.MAIN_SETTINGS.GAME_SETTINGS: settings.game,
        Stage.MAIN_SETTINGS.PLAYER_SETTINGS: settings.players,
        Stage.ADVANCED_SETTINGS.DISPLAY: settings.display,
        Stage.ADVANCED_SETTINGS.SELECTION: settings.selection,
        Stage.ADVANCED_SETTINGS.SAMPLING: settings.sampling,
        Stage.ADVANCED_SETTINGS.PLAYBACK_BAR: settings.playback_bar,
        Stage.ADVANCED_SETTINGS.EVALUATION: settings.evaluation,
    }

    return stage_to_settings_section_mapping[stage]

