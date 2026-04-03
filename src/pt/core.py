"""Contract for a plugin."""


class Plugin:
    """Contract for a plugin."""

    def __init__(
        self,
        name: str,  # plugin name
        every: float = 0.0,  # execution interval in seconds
    ):
        self.name = name
        self.every = every
