from app.cli.models import MenuStep


README_MENU = MenuStep(
    name="readme",
    prompt="Enter the number of INFO you want to get:",
    options=[
        "rules",
        "settings",
        "advanced_options",
        "authors",
        "back",
    ],
)
