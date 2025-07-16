"""Main module for mcpturbo-docs"""

import logging

from mcpturbo_core.logger import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class McpturboDocs:
    """Main class for mcpturbo-docs"""

    def __init__(self):
        self.version = "1.0.0"

    async def run(self):

        """Simple execution entry point."""
        message = f"mcpturbo-docs {self.version} running"
        logger.info(message)
        return message

