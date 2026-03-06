"""
Helper functions for capturing screenshots during test failures.
"""

import os
from datetime import datetime
from config import Config


def take_screenshot(driver, test_name):
    """
    Save a screenshot with a timestamp in the screenshots directory.
    Returns the file path of the saved screenshot.
    """
    os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"{Config.SCREENSHOT_DIR}/{test_name}_{timestamp}.png"
    driver.save_screenshot(screenshot_path)
    return screenshot_path
