import logging
import logging.handlers
from static.paths import LOGS_DIR

import os


def logger():
    """Returns an instance for a logger"""

    log_file = LOGS_DIR / "bot_logs.log"

    if not LOGS_DIR.exists():
        os.makedirs(LOGS_DIR, exist_ok=True)

    if not log_file.exists():
        with open(log_file, "w") as _:
            pass

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    logger_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=2000000, backupCount=5
    )
    logger_handler.setLevel(logging.DEBUG)

    logger_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    )
    logger_handler.setFormatter(logger_format)

    logger.addHandler(logger_handler)

    logger.info("logger initialised")

    return logger

