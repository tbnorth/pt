"""Code test/dev"""

from pt_win.plugins.nottl import NoTitle

from pt.core import TextDeskApp
from pt.plugins.clock import Clock
from pt.plugins.tail import Tail

if __name__ == "__main__":
    app = TextDeskApp()
    app.plugins.append(Clock)
    app.plugins.append((Tail, {"path": "C:\\Users\\tbrown02\\t\\clipboard_logs\\clipboard_log_2026-04-05.md"}))
    app.plugins.append(NoTitle)
    app.run()
