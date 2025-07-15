"""Main module for mcpturbo-ai"""

import logging

from mcpturbo_core.logger import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class McpturboAi:
    """Main class for mcpturbo-ai"""

    def __init__(self):
        self.version = "1.0.0"

    async def run(self):

        """Simple execution entry point."""
        message = f"mcpturbo-ai {self.version} running"
        logger.info(message)
        return message
