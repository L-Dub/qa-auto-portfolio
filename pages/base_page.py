"""
Base page class that all page objects inherit from.
Provides common methods for interacting with elements and making assertions.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import Config
from utils.logger import logger


class BasePage:
    """Encapsulates common web page interactions and assertion helpers."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.IMPLICIT_WAIT)

    # ---------- Navigation ----------
    def open(self, url):
        """
        Navigate to a fully qualified URL (or append to base if relative).
        Logs the navigation for debugging.
        """
        full_url = url if url.startswith("http") else Config.BASE_URL + url
        logger.info(f"Navigating to: {full_url}")
        self.driver.get(full_url)

    # ---------- Element Finding ----------
    def find_element(self, locator):
        """Wait for and return a single element. Logs the locator for traceability."""
        logger.debug(f"Waiting for element: {locator}")
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Wait for and return all matching elements."""
        logger.debug(f"Waiting for elements: {locator}")
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    # ---------- Basic Actions ----------
    def click(self, locator):
        """Click on an element after ensuring it is clickable."""
        logger.debug(f"Clicking element: {locator}")
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type(self, locator, text):
        """Clear an input field and type text."""
        logger.debug(f"Typing '{text}' into element: {locator}")
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Get text content of an element."""
        text = self.find_element(locator).text
        logger.debug(f"Text from {locator}: '{text}'")
        return text

    def is_displayed(self, locator):
        """
        Check if an element is displayed (without throwing exception).
        Returns True if displayed, False otherwise.
        """
        try:
            displayed = self.find_element(locator).is_displayed()
            logger.debug(f"Element {locator} displayed: {displayed}")
            return displayed
        except (TimeoutException, NoSuchElementException):
            logger.debug(f"Element {locator} not displayed")
            return False

    # ---------- Assertion Helpers ----------
    def assert_element_text(self, locator, expected_text, case_sensitive=False):
        """
        Assert that the text of an element matches the expected text.
        Raises AssertionError with a descriptive message on failure.
        """
        actual = self.get_text(locator)
        if not case_sensitive:
            actual = actual.lower()
            expected_text = expected_text.lower()
        assert actual == expected_text, \
            f"Text mismatch. Expected: '{expected_text}', Actual: '{actual}'"
        logger.info(f"Assertion passed: element text matches '{expected_text}'")

    def assert_element_contains_text(self, locator, expected_substring, case_sensitive=False):
        """Assert that the element's text contains the expected substring."""
        actual = self.get_text(locator)
        if not case_sensitive:
            actual = actual.lower()
            expected_substring = expected_substring.lower()
        assert expected_substring in actual, \
            f"Substring '{expected_substring}' not found in element text: '{actual}'"
        logger.info(f"Assertion passed: element text contains '{expected_substring}'")

    def assert_element_displayed(self, locator):
        """Assert that an element is displayed."""
        assert self.is_displayed(locator), f"Element {locator} should be displayed but is not."
        logger.info(f"Assertion passed: element {locator} is displayed")

    def assert_element_not_displayed(self, locator):
        """Assert that an element is NOT displayed."""
        assert not self.is_displayed(locator), f"Element {locator} should NOT be displayed but it is."
        logger.info(f"Assertion passed: element {locator} is not displayed")

    def assert_url_contains(self, expected_part):
        """Assert that the current URL contains a specific string."""
        current_url = self.driver.current_url
        assert expected_part in current_url, \
            f"URL does not contain '{expected_part}'. Actual URL: {current_url}"
        logger.info(f"Assertion passed: URL contains '{expected_part}'")

    def assert_title_contains(self, expected_part):
        """Assert that the page title contains a specific string."""
        actual_title = self.driver.title
        assert expected_part in actual_title, \
            f"Page title does not contain '{expected_part}'. Actual title: '{actual_title}'"
        logger.info(f"Assertion passed: title contains '{expected_part}'")

    def assert_title_is(self, expected_title):
        """Assert that the page title exactly matches the expected title."""
        actual_title = self.driver.title
        assert actual_title == expected_title, \
            f"Page title mismatch. Expected: '{expected_title}', Actual: '{actual_title}'"
        logger.info(f"Assertion passed: title is '{expected_title}'")