import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import cast

# Create logs directory if it doesn't exist
logs_dir = Path(__file__).parent.parent.parent / "logs"
logs_dir.mkdir(exist_ok=True)


def setup_logging(
    log_level: str = "INFO",
    log_file: str | None = "app.log",
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Set up logging configuration for the application.

    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Name of the log file
        max_bytes: Maximum size of each log file before rotation
        backup_count: Number of backup log files to keep

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("app")
    logger.setLevel(cast(int, getattr(logging, log_level.upper())))

    # Create formatters
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # File handler
    if log_file:
        file_handler = RotatingFileHandler(
            logs_dir / log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


# Create default logger instance
logger = setup_logging()
