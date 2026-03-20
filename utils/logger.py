"""
Logging configuration for the framework.
Logs are written to both console and a file in the logs directory.
"""

import logging
import os
from config import Config


# Create logs directory if it doesn't exist
os.makedirs(Config.LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(f"{Config.LOG_DIR}/test_run.log"),
        logging.StreamHandler()
    ]
)

# Create a logger instance for the whole framework
logger = logging.getLogger(__name__)