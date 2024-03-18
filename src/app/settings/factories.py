from app.cli.factories import ParsedModel
from app.cli.models import Menu
from app.cli.mods import manglers, representers, validators
from app.state import Stage, get_state
from app.settings.models import SettingsSection
from app.settings.processors import SettingsSectionProcessor


def _settings_sections_mapping(stage: Stage) -> SettingsSection:
    state = get_state()
    settings = state.settings

    if stage == Stage.MAIN_SETTINGS.value.PLAYER:
        if (player_number := state.data.get("player_number")) is None:
            raise ValueError("")

        return settings.players[player_number - 1]

    others_mapping = {
        Stage.MAIN_SETTINGS.value.GAME: settings.game,
        Stage.ADVANCED_SETTINGS.value.DISPLAY: settings.display,
        Stage.ADVANCED_SETTINGS.value.SELECTION: settings.selection,
        Stage.ADVANCED_SETTINGS.value.SAMPLING: settings.sampling,
        Stage.ADVANCED_SETTINGS.value.PLAYBACK_BAR: settings.playback_bar,
        Stage.ADVANCED_SETTINGS.value.EVALUATION: settings.evaluation,
        Stage.ADVANCED_SETTINGS.value.SERVICE_PATHS: settings.service_paths,
    }

    return others_mapping[stage]


def settings_menu_factory(stage: Stage) -> Menu | None:
    settings_section = _settings_sections_mapping(stage)

    if not (settings_model := ParsedModel.from_any_origin(settings_section)):
        return None

    return Menu(
        *settings_model.steps,
        name=settings_model.name,
        representer=representers.Representer(
            representers.RepresenterTemplate(
                prompt_template=representers.PromptTemplate.PROMPT_WITH_NAME,
                default_template=representers.DefaultTemplate.DEFAULT,
                options_template=representers.OptionsTemplate.WITH_NUMBER_AND_TAB,
            )
        ),
        validator=validators.ModelValidator(
            model=settings_section,
            accept_null_for_defaults=True,
        ),
        mangler=manglers.Mangler(
            manglers.ManglingTemplate.SETTINGS_SECTION,
        ),
        processor=SettingsSectionProcessor(
            settings_section=settings_section,
        ),
    )
