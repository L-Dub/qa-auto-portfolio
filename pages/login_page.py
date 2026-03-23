"""
Page Object for the Login page.
Encapsulates locators and actions related to login/logout functionality.
"""

from venv import logger

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config import Config


class LoginPage(BasePage):
    """
    Represents the login page of the application.
    Provides methods to log in, log out, and verify password visibility.
    """

    # Locators - defined as tuples for easy maintenance
    USERNAME_INPUT = (By.ID, "loginUsername")
    PASSWORD_INPUT = (By.ID, "loginPassword")
    LOGIN_BUTTON = (By.ID, "loginButton")
    FLASH_MESSAGE = (By.CSS_SELECTOR, "[matsnackbarlabrl]")          # Area that shows success/error messages
    LOGOUT_BUTTON = (By.XPATH, "//span[text()='Logout']")
    EYE_ICON = (By.ID, "togglePassword")  # Adjust selector to match your app's HTML
    SETTINGS_BUTTON = (By.XPATH, "//button[contains(text(), 'Settings')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/en/login"  # Relative to base URL

    # ---------- Navigation ----------
    def navigate(self):
        """Open the login page and verify we are on the correct page."""
        self.open(self.url)
        assert "/en/login" in self.driver.current_url  # Quick sanity check
        
    def open_settings(self):
        self.click(self.SETTINGS_BUTTON)

    # ---------- Actions ----------
    def login(self):
        """
        Fill in credentials and click the login button.
        Does not assert success – that's left to the test.
        """
        logger.info(f"Attempting login with username: {Config.ADMIN_USERNAME}")
        self.type(self.USERNAME_INPUT, Config.ADMIN_USERNAME)
        self.type(self.PASSWORD_INPUT, Config.ADMIN_PASSWORD)
        self.click(self.LOGIN_BUTTON)

    def logout(self):
        """Click the logout button. Assumes the user is already logged in."""
        logger.info("Logging out")
        self.click(self.LOGOUT_BUTTON)

    def reveal_password(self):
        """Click the eye icon to toggle password visibility."""
        logger.info("Toggling password visibility")
        self.click(self.EYE_ICON)

    # ---------- Getters ----------
    def get_flash_message(self):
        """Return the text of the flash message area."""
        return self.get_text(self.FLASH_MESSAGE)

    def get_password_field_type(self):
        """Return the 'type' attribute of the password field (text or password)."""
        return self.find_element(self.PASSWORD_INPUT).get_attribute("type")

    # ---------- Specific Assertions ----------
    def assert_login_successful(self):
        """Assert that login succeeded by checking presence of logout button."""
        self.assert_element_displayed(self.LOGOUT_BUTTON)
        logger.info("Login successful – logout button is present.")

    def assert_login_failed(self, expected_error_substring):
        """Assert that login failed and an error message containing the expected text is shown."""
        self.assert_element_contains_text(self.FLASH_MESSAGE, expected_error_substring)
        logger.info(f"Login failed as expected with message containing '{expected_error_substring}'")

    def assert_on_login_page(self):
        """Assert that we are back on the login page (e.g., after logout)."""
        self.assert_title_contains("Login")
        self.assert_element_displayed(self.LOGIN_BUTTON)
        self.assert_element_not_displayed(self.LOGOUT_BUTTON)
