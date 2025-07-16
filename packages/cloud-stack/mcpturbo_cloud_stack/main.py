"""Main module for mcpturbo-cloud-stack"""

import logging

from mcpturbo_core.logger import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class McpturboCloudStack:
    """Main class for mcpturbo-cloud-stack"""

    def __init__(self):
        self.version = "1.0.0"

    async def run(self):

        """Simple execution entry point."""
        message = f"mcpturbo-cloud-stack {self.version} running"
        logger.info(message)
        return message

