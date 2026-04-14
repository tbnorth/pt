"""Code test/dev"""

from pathlib import Path

try:
    from pt_win.plugins.nottl import NoTitle
except ImportError:
    NoTitle = None

try:
    from pt.plugins.credget import CredGet
except ImportError:
    CredGet = None

from pt.core import TextDeskApp
from pt.plugins.clock import Clock
from pt.plugins.tail import Tail

if __name__ == "__main__":
    app = TextDeskApp()
    # app.plugins.append(Clock)
    cbl = "C:\\Users\\tbrown02\\t\\clipboard_logs\\clipboard_log_2026-04-05.md"
    if Path(cbl).exists():
        app.plugins.append((Tail, {"path": cbl}))
    if NoTitle:
        app.plugins.append(NoTitle)
    if CredGet:
        app.plugins.append(CredGet)
    app.run()
