from pydantic import BaseModel

from app.settings.views import Viewer


class SettingsPresenter:
    def __init__(self, viewer: Viewer):
        self.viewer = viewer

    def format_setting(self, settings_section: BaseModel):
        return f"User:\nID: {user.id}\nUsername: {user.username}\nEmail: {user.email}"

    def display_user(self, user: User):
        formatted_data = self.format_user(user)
        self.viewer.display(formatted_data)