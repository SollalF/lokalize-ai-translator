import os

import uvicorn
from dotenv import load_dotenv

from app.core.logging import logger, setup_logging


def main():
    # Load environment variables
    load_dotenv()

    # Get log level from environment variable or default to INFO
    log_level = os.getenv("LOG_LEVEL", "INFO")

    # Setup logging with the configured level
    setup_logging(log_level=log_level)

    logger.info("Starting the application...")

    # Configure uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", "8000")),
        reload=True,
        workers=1,
        log_level=log_level.lower(),
    )


if __name__ == "__main__":
    main()
