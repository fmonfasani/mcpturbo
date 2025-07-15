"""Main module for mcpturbo-web"""

import logging

from mcpturbo_core.logger import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class McpturboWeb:
    """Main class for mcpturbo-web"""

    def __init__(self):
        self.version = "1.0.0"

    async def run(self):

        """Simple execution entry point."""
        message = f"mcpturbo-web {self.version} running"
        logger.info(message)
        return message

