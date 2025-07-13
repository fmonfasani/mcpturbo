"""Genesis command implementations."""

import argparse
from typing import Any

from ..genesis_integration import genesis_init, genesis_setup

async def cmd_init(args: argparse.Namespace) -> Any:
    """Handle `genesis init` command."""
    return await genesis_init(args.project_name, app_type=args.type)

async def cmd_setup(args: argparse.Namespace) -> Any:
    """Handle `genesis setup` command."""
    return await genesis_setup()


def build_parser(subparsers: argparse._SubParsersAction) -> None:
    """Register genesis commands with the main parser."""
    parser = subparsers.add_parser("genesis", help="Project scaffolding commands")
    g_sub = parser.add_subparsers(dest="genesis_command")

    init_parser = g_sub.add_parser("init", help="Initialize new project")
    init_parser.add_argument("project_name", help="Name of the project")
    init_parser.add_argument("--type", default="web", help="Project type template")
    init_parser.set_defaults(func=cmd_init)

    setup_parser = g_sub.add_parser("setup", help="Setup orchestrator and agents")
    setup_parser.set_defaults(func=cmd_setup)
