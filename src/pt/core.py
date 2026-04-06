"""Contract for a plugin, main app."""

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from pt.flexbox import FlexBoxContainer


class Plugin:
    """Contract for a plugin."""

    def __init__(
        self,
        name: str,  # plugin name
        every: float = 0.0,  # execution interval in seconds
    ):
        self.name = name
        self.every = every

class TextDeskLayout(FlexBoxContainer):
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        for widget in self.app.plugins:
            yield widget()

class TextDeskApp(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugins = []

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield TextDeskLayout()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = TextDeskApp()
    app.run()
