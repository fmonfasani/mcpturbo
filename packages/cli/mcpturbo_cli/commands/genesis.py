
"""Commands for project initialization using Genesis."""

from argparse import Namespace
from typing import Any

from ..genesis_integration import genesis_init


async def cmd_init(args: Namespace) -> Any:
    """Handle ``genesis init`` command."""
    return await genesis_init(project_name=args.name, app_type=getattr(args, "type", "web"))

__all__ = ["cmd_init"]

