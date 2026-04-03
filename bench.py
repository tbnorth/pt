"""Code test/dev"""

import asyncio
from datetime import datetime

import pyperclip
import win32con
import win32gui
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Label

from pt.flexbox import FlexBoxContainer


class CopyableLabel(Label):
    """A label that can be copied to the clipboard."""

    def on_click(self) -> None:
        """Handle click events on the label."""
        pyperclip.copy(self.content)
        content = self.content
        self.update("Copied")
        self.set_timer(0.33, lambda: self.update(content))


class TimeScreen(Screen):
    """A simple screen to display the time."""

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        now = datetime.now()
        epoch = str(now.timestamp())
        for fmt in [
            "%A, %B %d, %Y",
            "%H:%M:%S",
            "%I:%M %p",
            "%Y-%m-%d %H:%M:%S",
            "%Y%m%d%H%M%S",
            "%Y%m%d",
            "%H%M%S",
            "%a, %b %d, %Y",
            "%B %d, %Y",
            "%b %d, %Y",
            "%d %B %Y",
            "%c",
            "%X",
            "%x",
            epoch,
        ]:
            yield CopyableLabel(now.strftime(fmt))

    def on_click(self) -> None:
        """Handle click events on the screen."""
        # self.app.pop_screen()
        self.set_timer(0.66, self.app.pop_screen)


class NoTitle(Label):
    async def on_click(self) -> None:

        colors = ["red", "white"]
        for i in range(15):
            self.styles.color = colors[i % 2]
            self.app.refresh()
            await asyncio.sleep(0.2)
        self.styles.color = "white"
        hwnd = win32gui.GetForegroundWindow()   
        current_style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        new_style = current_style ^ win32con.WS_CAPTION
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, new_style)
        win32gui.SetWindowPos(
            hwnd,
            0,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE
            | win32con.SWP_NOSIZE
            | win32con.SWP_NOZORDER
            | win32con.SWP_FRAMECHANGED,
        )


class Clock(Label):
    """A simple clock widget."""

    def on_mount(self) -> None:
        """Start a timer to update the clock every second."""
        self.update_time()
        self.set_interval(1, self.update_time)

    def update_time(self) -> None:
        """Update the clock's label with the current time."""

        now = datetime.now().strftime("%H:%M:%S")
        self.update(now)

    def on_click(self) -> None:
        """Handle click events on the clock."""
        if "time_screen" not in self.app.SCREENS:
            ts = TimeScreen()
            self.app.SCREENS["time_screen"] = ts
            self.app.install_screen(ts, name="time_screen")

        self.app.push_screen("time_screen")


class PTLayout(FlexBoxContainer):
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield NoTitle("<no title>")
        yield Clock()


class StopwatchApp(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "bench.tcss"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield PTLayout()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = StopwatchApp()
    app.run()
