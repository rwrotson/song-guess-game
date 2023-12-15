from pydantic import BaseModel

from app.abstract.menus import Menu
from app.cli.core import structs
from app.cli.menus import HomogenicMenu, HeterogenicMenu
from app.cli.mods.manglers import InputMangler, ManglingTemplate
from app.cli.core.models import MenuModel, MenuStepType, MenuType
from app.cli.mods.representers import TextInputRepresenter, OptionsRepresenter, MenuRepresenter
from app.cli.mods.receivers import InputReceiver


def model_factory(menu_info: type[structs.MenuInfo] | BaseModel) -> MenuModel:
    if isinstance(menu_info, BaseModel):
        return MenuModel.from_model(menu_info)
    return MenuModel.from_menu_info(menu_info)


def parse_menu_step_type(step_type: MenuStepType) -> tuple[MenuRepresenter, InputReceiver, InputMangler]:
    mapping = {
        MenuStepType.OPTIONS: {
            "representer": OptionsRepresenter,
            "mangling_template": ManglingTemplate.OPTIONS_MENU,
        },
        MenuStepType.TEXT_INPUT: {
            "representer": TextInputRepresenter,
            "mangling_template": ManglingTemplate.SETTINGS_SECTION,
        },
    }

    representer = mapping[step_type]["representer"]
    mangling_template = mapping[step_type]["mangling_template"]
    input_mangler = InputMangler(template=mangling_template)
    input_receiver = InputReceiver()

    return representer, input_receiver, input_mangler


def homogenic_menu_factory(menu_info: type[structs.MenuInfo] | BaseModel) -> HomogenicMenu:
    model = model_factory(menu_info)
    menu_type = model.menu_type

    if menu_type == MenuType.MIXED:
        raise ValueError("Menu model type must be HOMOGENIC.")

    menu_type_to_step_type = {
        MenuType.OPTIONS: MenuStepType.OPTIONS,
        MenuType.TEXT_INPUT: MenuStepType.TEXT_INPUT,
    }
    step_type = menu_type_to_step_type[menu_type]
    representer, input_receiver, input_mangler = parse_menu_step_type(step_type)

    return HomogenicMenu(
        model=model,
        representer=representer,
        receiver=input_receiver,
        mangler=input_mangler,
    )


def heterogenic_menu_factory(menu_info: type[structs.MenuInfo] | BaseModel) -> HeterogenicMenu:
    model = model_factory(menu_info)
    menu_type = model.menu_type

    if menu_type != MenuType.MIXED:
        raise ValueError("Menu model type must be HETEROGENIC.")

    representers = []
    receivers = []
    manglers = []
    for step in model.steps:
        step_type = step.step_type
        representer, input_receiver, input_mangler = parse_menu_step_type(step_type)

        representers.append(representer)
        receivers.append(input_receiver)
        manglers.append(input_mangler)

    return HeterogenicMenu(
        model=model,
        representer=representers,
        receiver=receivers,
        mangler=manglers,
    )


def menu_factory(menu_info: type[structs.MenuInfo] | BaseModel) -> Menu:
    model = model_factory(menu_info)
    if model.menu_type == MenuType.MIXED:
        return heterogenic_menu_factory(menu_info)
    return homogenic_menu_factory(menu_info)
