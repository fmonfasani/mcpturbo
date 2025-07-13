"""Main entry point for ``mcpturbo-cli``."""

from __future__ import annotations

import argparse
from typing import Any, Sequence

from .commands import genesis as genesis_cmd


class McpturboCli:
    """Main class for mcpturbo-cli."""

    def __init__(self) -> None:
        self.version = "1.0.0"

    async def run(self, argv: Sequence[str] | None = None) -> Any:
        """Parse arguments and execute the chosen command."""
        parser = argparse.ArgumentParser(prog="mcpturbo")
        subparsers = parser.add_subparsers(dest="command")

        # ``genesis`` command group
        genesis_parser = subparsers.add_parser(
            "genesis", help="Project initialization commands"
        )
        genesis_sub = genesis_parser.add_subparsers(dest="subcommand")

        init_parser = genesis_sub.add_parser(
            "init", help="Initialize a new project via Genesis"
        )
        init_parser.add_argument("name", help="Project name")
        init_parser.add_argument(
            "--type",
            dest="type",
            default="web",
            help="Project type (default: web)",
        )

        args = parser.parse_args(list(argv) if argv is not None else None)

        if args.command == "genesis" and args.subcommand == "init":
            return await genesis_cmd.cmd_init(args)

        parser.print_help()
        return None

