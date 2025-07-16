
"""Main entry point for ``mcpturbo-cli``."""

from __future__ import annotations

import argparse
import logging
from typing import Any, Sequence

from mcpturbo_core.logger import configure_logging
from .commands import genesis as genesis_cmd

configure_logging()
logger = logging.getLogger(__name__)



class McpturboCli:
    """Main class for mcpturbo-cli."""

    def __init__(self) -> None:
        self.version = "1.0.0"


    async def run(self):
        """Simple execution entry point."""
        message = f"mcpturbo-cli {self.version} running"
        logger.info(message)
        return message
