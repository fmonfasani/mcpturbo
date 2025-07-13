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

    async def _run_async(self, args: argparse.Namespace) -> None:
        if hasattr(args, "func"):
            await args.func(args)
        else:
            raise SystemExit("No command specified")

    def run(self, argv: Optional[list[str]] = None) -> None:
        """Parse arguments and execute the chosen command."""
        parser = argparse.ArgumentParser(prog="mcpturbo")
        subparsers = parser.add_subparsers(dest="command")

        # Register command groups
        genesis.build_parser(subparsers)

        args = parser.parse_args(argv)
        asyncio.run(self._run_async(args))


if __name__ == "__main__":
    McpturboCli().run()
