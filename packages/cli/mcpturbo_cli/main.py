
"""Main entry point for ``mcpturbo-cli``."""

from __future__ import annotations

import argparse
from typing import Any, Sequence

from .commands import genesis as genesis_cmd



class McpturboCli:
    """Main class for mcpturbo-cli."""

    def __init__(self) -> None:
        self.version = "1.0.0"


    async def run(self):
        """Simple execution entry point."""
        message = f"mcpturbo-cli {self.version} running"
        print(message)
        return message
