from app.settings.models import SettingsSection


class SettingsSectionProcessor:
    # cli-level validation
    def __init__(self, settings_section: SettingsSection, number) -> None:
        self.settings_section = settings_section

    def process(self, input_text: str, /) -> None:
        pass
