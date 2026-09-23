from datetime import datetime

import psutil
import pyperclip
from rich.text import Text
from textual.app import ComposeResult
from textual.color import Color, Gradient
from textual.screen import Screen
from textual.widgets import Button, Label, RichLog, Static

SCREEN_NAME = "cpu_screen"


BAR = "▁▂▃▄▅▆▇█"


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


class CPUScreen(Screen):
    """A simple screen to display CPU usage."""

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        steps = 40
        grad = Gradient.from_colors(
            Color.parse("red"), Color.parse("green"), quality=steps
        )
        for bg in (
            lambda x: Color.parse("white"),
            lambda x: Color.parse("black"),
            lambda x: grad.get_color(x / steps),
        ):
            text = []
            for i in range(steps):
                color = grad.get_color(i / steps)
                roloc = grad.get_color((steps - i) / steps)
                # text.append(f"[{roloc.hex} on {bg(i).hex}]*[/]")
                text.append(f"[{roloc.hex}][on {bg(i).hex}]*[/][/]")
                # text.append(f"[{roloc.hex} on #ffffff]*[/]")
            yield Label("qcpu" + "".join(text))

        for bg in (
            lambda x: Color.parse("white"),
            lambda x: Color.parse("black"),
            lambda x: grad.get_color(x / steps),
        ):
            text = Text()
            for i in range(steps):
                color = grad.get_color(i / steps)
                roloc = grad.get_color((steps - i) / steps)
                # text.append(f"[{roloc.hex} on {bg(i).hex}]*[/]")
                text.append("*", style=f"{roloc.hex} on {bg(i).hex}")
                # text.append(f"[{roloc.hex} on #ffffff]*[/]")
            log = RichLog()
            log.write(text)
            yield log

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


class CPU(Button):
    """A simple tail widget."""

    def __init__(self, *args, **kwargs):
        kwargs["compact"] = True
        self.path = kwargs.pop("path", None)
        super().__init__(*args, **kwargs)
        self.history = []
        self.history_limit = 10

    def on_mount(self) -> None:
        """Start a timer to update the tail every second."""
        self.update_text()
        self.set_interval(5, self.update_text)

    def update_text(self) -> None:
        """Update the tail's label with the latest content."""
        steps = 40
        grad = Gradient.from_colors(
            Color.parse("green"), Color.parse("red"), quality=steps
        )
        self.history.append(psutil.cpu_percent())
        if len(self.history) > self.history_limit:
            self.history.pop(0)
        x = int(self.history[-1])
        pct = "󰘣" if x > 99 else f"{x:02d}"[0]
        text = Text(f" {pct}")
        for x in self.history:
            color = grad.get_color(x / 100)
            text.append(BAR[int((x / 100) * (len(BAR) - 1))], style=f"{color.hex}")
        self.label = text

    def action_press(self) -> None:
        """Handle click events on the tail."""
        if SCREEN_NAME not in self.app.SCREENS:
            ts = CPUScreen()
            self.app.SCREENS[SCREEN_NAME] = ts
            self.app.install_screen(ts, name=SCREEN_NAME)

        self.app.push_screen(SCREEN_NAME)

    on_click = action_press
