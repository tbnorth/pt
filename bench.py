"""Code test/dev"""

from pt_win.plugins.nottl import NoTitle

from pt.core import TextDeskApp
from pt.plugins.clock import Clock

if __name__ == "__main__":
    app = TextDeskApp()
    app.plugins.append(Clock)
    app.plugins.append(NoTitle)
    app.run()
