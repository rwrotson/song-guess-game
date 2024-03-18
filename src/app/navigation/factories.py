from app.cli.models import Menu
from app.cli.mods import manglers, representers, validators
from app.cli.factories import ParsedModel
from app.game.factories import game_menu_factory
from app.navigation import templates, processors
from app.state import State, Stage
from app.readme.factories import readme_menu_factory
from app.settings.factories import settings_menu_factory


MAIN_TEMPLATES_MAPPING = {
    Stage.MAIN_MENU: templates.make_main_menu_step,
    Stage.LIBRARIES_STATS: templates.make_libraries_stats_step,
    Stage.SETTINGS.value.ALL_SETTINGS: templates.SETTINGS_MENU,
    Stage.SETTINGS.value.MAIN_SETTINGS: templates.MAIN_SETTINGS_MENU,
    Stage.SETTINGS.value.ADVANCED_SETTINGS: templates.ADVANCED_SETTINGS_MENU,
    Stage.SETTINGS.value.PLAYERS: templates.make_players_menu_step,
}


MAIN_PROCESSORS_MAPPING = {
    Stage.MAIN_MENU: processors.MainMenuProcessor(),
    Stage.LIBRARIES_STATS: processors.LibrariesStatsProcessor(),
    Stage.SETTINGS.value.ALL_SETTINGS: processors.SettingsProcessor(),
    Stage.SETTINGS.value.MAIN_SETTINGS: processors.MainSettingsProcessor(),
    Stage.SETTINGS.value.ADVANCED_SETTINGS: processors.AdvancedSettingsProcessor(),
    Stage.SETTINGS.value.PLAYERS: processors.PlayersSettingsProcessor(),
}


def main_menu_factory(stage: Stage) -> Menu:
    menu_template = MAIN_TEMPLATES_MAPPING[stage]
    if callable(menu_template):
        menu_template = menu_template()

    parsed_model = ParsedModel.from_any_origin(menu_template)

    return Menu(
        *parsed_model.steps,
        name=parsed_model.name,
        representer=representers.Representer(
            representers.RepresenterTemplate(
                prompt_template=representers.PromptTemplate.BOLD_PROMPT,
                options_template=representers.OptionsTemplate.WITH_NUMBER_AND_TAB,
            )
        ),
        validator=validators.MaxNumberValidator(
            menu_template.options_number,
        ),
        mangler=manglers.Mangler(
            manglers.ManglingTemplate.OPTIONS_MENU,
        ),
        processor=MAIN_PROCESSORS_MAPPING[stage],
    )


def menu_factory(state: State) -> Menu:
    stage = state.stage

    main_stages = (Stage.MAIN_MENU, Stage.LIBRARIES_STATS)
    if (stage in main_stages) or (stage in Stage.SETTINGS.value):
        return main_menu_factory(stage)

    if (stage in Stage.MAIN_SETTINGS.value) or (stage in Stage.ADVANCED_SETTINGS.value):
        return settings_menu_factory(stage)

    if stage in Stage.GAME.value:
        return game_menu_factory(stage)

    if stage == Stage.README:
        return readme_menu_factory()

    raise ValueError(f"Unsupported stage: {state.stage}")
