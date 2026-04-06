
from datetime import UTC, datetime

import pyperclip
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button


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


class TimeScreen(Screen):
    """A simple screen to display the time."""

    fmts = [
        "%Y%m%d%H%M%S",  # 20260404155120
        "%Y%m%d",  # 20260404
        "%c",  # Sat Apr  4 15:51:20 2026
        "%a %b %d %I:%M %p %Y",  # Sat Apr 04 04:00 PM 2026
        "%Y-%m-%d %H:%M:%S",  # 2026-04-04 15:51:20
        "EPOCH",  # 1775335880.720142
        "ISO",  # 2026-04-04T15:51:20.720142-05:00
        "ISOUTC",  # 2026-04-04T20:51:20.720142+00:00
        "%A, %B %d, %Y",  # Saturday, April 04, 2026
        "%a, %b %d, %Y",  # Sat, Apr 04, 2026
        "%B %d, %Y",  # April 04, 2026
        "%b %d, %Y",  # Apr 04, 2026
        "%d %B %Y",  # 04 April 2026
        "%x",  # 04/04/26
        "%H:%M:%S",  # 15:51:20
        "%I:%M %p",  # 03:51 PM
        "%H%M%S",  # 155120
        "Day %j",  # Day 094
        "Week starting Monday: %U",  # Week starting Monday: 13
        "Week starting Sunday: %W",  # Week starting Sunday: 13
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._btns = []

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        for fmt in self.fmts:
            btn = Button(fmt, compact=True)
            self._btns.append(btn)
            yield btn

    def on_click(self) -> None:
        """Handle click events on the screen."""
        # self.app.pop_screen()
        self.set_timer(0.66, self.app.pop_screen)

    # @on(ScreenResume)
    def on_screen_resume(self):
        now = datetime.now()
        for fmt, btn in zip(self.fmts, self._btns, strict=True):
            match fmt:
                case "EPOCH":
                    txt = str(now.timestamp())
                case "ISO":
                    txt = now.astimezone().isoformat()
                case "ISOUTC":
                    txt = now.astimezone(UTC).isoformat()
                case _:
                    txt = now.strftime(fmt)
            btn.label = now.strftime(txt)

    def on_button_pressed(self, pressed):
        button = pressed.button
        pyperclip.copy(button.label)

        def reset(button=button, content=button.label):
            button.label = content

        button.label = "Copied"
        self.set_timer(0.33, reset)
        self.set_timer(0.66, self.app.pop_screen)

    def on_key(self, key):
        if key.key not in ("tab", "enter"):
            self.app.pop_screen()


class Clock(Button):
    """A simple clock widget."""

    def __init__(self, *args, **kwargs):
        kwargs["compact"] = True
        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        """Start a timer to update the clock every second."""
        self.update_time()
        self.set_interval(1, self.update_time)

    def update_time(self) -> None:
        """Update the clock's label with the current time."""
        now = datetime.now().strftime("%H:%M:%S")
        self.label = now

    def action_press(self) -> None:
        """Handle click events on the clock."""
        if "time_screen" not in self.app.SCREENS:
            ts = TimeScreen()
            self.app.SCREENS["time_screen"] = ts
            self.app.install_screen(ts, name="time_screen")

        self.app.push_screen("time_screen")
