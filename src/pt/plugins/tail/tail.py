
from datetime import UTC, datetime
from pathlib import Path

import pyperclip
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, TextArea
from textual.containers import Horizontal, Vertical

SCREEN_NAME = "tail_screen"

class CopyableButton(Button):
    """A label that can be copied to the clipboard."""
    # FIXME: move to some common shared module?

    def __init__(self, *args, **kwargs):
        kwargs["compact"] = True
        super().__init__(*args, **kwargs)

    def action_press(self) -> None:
        """Handle click events on the label."""
        pyperclip.copy(self.label)

        def reset(self=self, content=self.label):
            self.label = content

        self.label = "Copied"
        self.set_timer(0.33, reset)


class TailScreen(Screen):
    """A simple screen to display the tail of a file."""

    def __init__(self, *args, **kwargs):
        self.path = kwargs.pop("path", None)
        self.lines = Path(self.path).read_text().splitlines()[-10:]
        super().__init__(*args, **kwargs)
        self._btns = []

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        self.last_lines = [Button(">", compact=True) for _ in range(100)]
        for line, btn in enumerate(self.last_lines):
            btn.line = line
        self.text_area = TextArea(Path(self.path).read_text(), read_only=True)
        self.text_area.scroll_end(animate=False)
        yield Horizontal(Vertical(*self.last_lines), self.text_area, classes="leftish")


    # @on(ScreenResume)
    def on_screen_resume(self):
        now = datetime.now()

    def on_button_pressed(self, pressed):
        button = pressed.button
        pyperclip.copy(button.label)

        def reset(button=button, content=button.label):
            button.label = content

        button.label = str(button.line)
        button.label = str(button.parent.size.height)

        self.set_timer(0.33, reset)
        self.set_timer(0.66, self.app.pop_screen)

    def Xon_key(self, key):
        if key.key not in ("tab", "enter"):
            self.app.pop_screen()


class Tail(Button):
    """A simple tail widget."""

    def __init__(self, *args, **kwargs):
        kwargs["compact"] = True
        self.path = kwargs.pop("path", None)
        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        """Start a timer to update the tail every second."""
        self.update_text()
        self.set_interval(1, self.update_text)

    def update_text(self) -> None:
        """Update the tail's label with the latest content."""
        if self.path:
            with open(self.path, "rb") as f:
                f.seek(0, 2)  # Move to the end of the file
                # Then seek backwards until we find a newline, or reach the beginning of
                # the file
                while f.tell() > 0:
                    f.seek(-1, 1)
                    if f.read(1) == b"\n":
                        content = f.read().decode("utf-8")
                        if content.strip():
                            self.label = content.strip()
                            break
                    f.seek(-1, 1)


    def action_press(self) -> None:
        """Handle click events on the tail."""
        if SCREEN_NAME not in self.app.SCREENS:
            ts = TailScreen(path=self.path)
            self.app.SCREENS[SCREEN_NAME] = ts
            self.app.install_screen(ts, name=SCREEN_NAME)

        self.app.push_screen(SCREEN_NAME)

    on_click = action_press
