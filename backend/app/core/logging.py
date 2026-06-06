"""Unified logging configuration for the application."""
import logging
import os
from logging.handlers import RotatingFileHandler


def setupLogging() -> logging.Logger:
    """Configure root logger with file rotation and console output."""
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    # Console handler — WARNING and above only
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    console.setFormatter(logging.Formatter("%(levelname)s - %(name)s - %(message)s"))

    # File handler — all levels, with rotation
    logDir = "logs"
    os.makedirs(logDir, exist_ok=True)
    file = RotatingFileHandler(
        f"{logDir}/app.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file.setLevel(logging.INFO)
    file.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))

    logger.addHandler(console)
    logger.addHandler(file)
    logger.info("Logging system initialized")
    return logger