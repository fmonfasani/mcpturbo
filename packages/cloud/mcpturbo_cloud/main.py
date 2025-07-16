"""Main module for mcpturbo-cloud"""

import logging

from mcpturbo_core.logger import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

class McpturboCloud:
    """Main class for mcpturbo-cloud"""
    
    def __init__(self):
        self.version = "1.0.0"

    async def run(self):

        """Simple execution entry point."""
        message = f"mcpturbo-cloud {self.version} running"
        logger.info(message)
        return message

