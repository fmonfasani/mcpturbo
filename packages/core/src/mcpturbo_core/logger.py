import logging


def configure_logging(level=logging.INFO):
    """Configure basic logging for the mcpturbo packages."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


__all__ = ["configure_logging"]
