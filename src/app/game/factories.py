from app.cli.factories import ParsedModel
from app.cli.models import Menu, MenuStep
from app.cli.mods import manglers, representers, validators
from app.game import templates, processors
from app.state import Stage


GAME_TEMPLATES_MAPPING = {
    Stage.GAME.value.QUESTION: templates.make_question_menu,
    Stage.GAME.value.ANSWER: templates.ANSWER_MENU,
    Stage.GAME.value.EVALUATION_: templates.make_evaluation_menu,
    Stage.GAME.value.ENDGAME: templates.ENDGAME_MENU,
}


GAME_PROCESSORS_MAPPING = {
    Stage.GAME.value.QUESTION: processors.QuestionProcessor(),
    Stage.GAME.value.ANSWER: processors.AnswerProcessor(),
    Stage.GAME.value.EVALUATION_: processors.EvaluationProcessor(),
    Stage.GAME.value.ENDGAME: processors.EndgameProcessor(),
}


def _game_text_menu_factory(stage: Stage, parsed_model: ParsedModel) -> Menu:
    return Menu(
        *parsed_model.steps,
        name=parsed_model.name,
        representer=representers.Representer(
            representers.RepresenterTemplate(
                prompt_template=representers.PromptTemplate.ONLY_PROMPT,
                options_template=representers.OptionsTemplate.NO_OPTIONS,
            )
        ),
        validator=validators.NoValidator(default_input="no answer"),
        mangler=manglers.Mangler(
            manglers.ManglingTemplate.NO_MANGLING,
        ),
        processor=GAME_PROCESSORS_MAPPING[stage],
    )


def _game_options_menu_factory(
    stage: Stage, parsed_model: ParsedModel, menu_template: MenuStep
) -> Menu:
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
        processor=GAME_PROCESSORS_MAPPING[stage],
    )


def game_menu_factory(stage: Stage) -> Menu:
    menu_template = GAME_TEMPLATES_MAPPING[stage]

    if callable(menu_template):
        menu_template: MenuStep = menu_template()

    parsed_model = ParsedModel.from_any_origin(menu_template)

    if stage in (Stage.GAME.value.ANSWER, Stage.GAME.value.ENDGAME):
        return _game_text_menu_factory(stage, parsed_model)

    return _game_options_menu_factory(stage, parsed_model, menu_template)
