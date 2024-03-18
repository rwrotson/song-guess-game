from app.cli.factories import ParsedModel
from app.cli.models import Menu
from app.cli.mods import manglers, representers, validators
from app.readme.models import README_MODEL
from app.readme.processors import ReadmeProcessor
from app.readme.templates import README_MENU


def readme_menu_factory() -> Menu:
    menu_model = ParsedModel.from_any_origin(README_MENU)

    return Menu(
        *menu_model.steps,
        name=menu_model.name,
        representer=representers.Representer(
            representers.RepresenterTemplate(
                prompt_template=representers.PromptTemplate.BOLD_PROMPT,
                options_template=representers.OptionsTemplate.WITH_NUMBER_AND_TAB,
            )
        ),
        validator=validators.MaxNumberValidator(
            README_MODEL.sections_number + 1,
        ),
        mangler=manglers.Mangler(
            manglers.ManglingTemplate.OPTIONS_MENU,
        ),
        processor=ReadmeProcessor(),
    )
