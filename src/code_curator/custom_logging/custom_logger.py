from __future__ import annotations
import logging

from .logging_formatter import CustomFormatter

class CustomLogger:
    # FIXME: Possible fix this?
    @classmethod
    def getLogger(cls, name: str) -> CustomLogger:
        logger = logging.getLogger(name)
        logger.propagate = False

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        ch.setFormatter(CustomFormatter())

        logger.addHandler(ch)
        return logger