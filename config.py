"""
Configuration management for the test framework.
Loads settings from environment variables (via .env file) and provides defaults.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()


class Config:
    """Central configuration class."""

    # Application URL
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")

    # Browser settings
    BROWSER = os.getenv("BROWSER")
    HEADLESS = os.getenv("HEADLESS").lower() == "true"
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "30"))

    # Credentials
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    CBO_USERNAME = os.getenv("CBO_USERNAME")
    CBO_PASSWORD = os.getenv("CBO_PASSWORD")
    ENGINEER_USERNAME= os.getenv("ENGINEER_USERNAME")
    ENGINEER_PASSWORD= os.getenv("ENGINEER_PASSWORD")
    SUPERVISOR_USERNAME= os.getenv("SUPERVISOR_USERNAME")
    SUPERVISOR_PASSWORD= os.getenv("SUPERVISOR_PASSWORD")
    
    #Firmware file path
    FIRMWARE_FILE_PATH = os.getenv("FIRMWARE_FILE_PATH")

    # API
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080/api")

    # Paths
    SCREENSHOT_DIR = "reports/screenshots"
    LOG_DIR = "logs"

    # Hardware mock flag
    MOCK_HARDWARE = os.getenv("MOCK_HARDWARE").lower() == "true"
