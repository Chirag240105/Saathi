"""Structured (key=value) logging helpers."""
import logging
import sys
from typing import Any


def setup_logging(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s level=%(levelname)s logger=%(name)s %(message)s")
    )
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(level)


def log_event(logger: logging.Logger, event: str, **fields: Any) -> None:
    """Log `event` with key=value fields, e.g. log_event(log, "tool_call", tool="x", ms=12)."""
    parts = " ".join(f"{k}={v!r}" for k, v in fields.items())
    logger.info("event=%s %s", event, parts)
