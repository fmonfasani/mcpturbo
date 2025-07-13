"""Main module for mcpturbo-cli."""

from __future__ import annotations

import argparse
import asyncio
from typing import Optional

from .commands import genesis


class McpturboCli:
    """Main entrypoint for the mcpturbo command line interface."""

    def __init__(self):
        self.version = "1.0.0"

        
    async def run(self):
        """Run the CLI entry point"""
        return f"{self.__class__.__name__} running (v{self.version})"

