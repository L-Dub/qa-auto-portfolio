"""
Page Object for the Login page.
Encapsulates locators and actions related to login/logout functionality.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config import Config
from utils.logger import logger


class LoginPage(BasePage):
    """
    Represents the login page of the application.
    Provides methods to log in, log out, and verify password visibility.
    """

    # Locators
    USERNAME_INPUT = (By.ID, "loginUsername")
    PASSWORD_INPUT = (By.ID, "loginPassword")
    LOGIN_BUTTON = (By.ID, "loginButton")
    FLASH_MESSAGE = (By.CSS_SELECTOR, ".mat-mdc-snack-bar-label")   # Snackbar for error messages
    DASHBOARD_HEADING = (By.CSS_SELECTOR, "blastweb-heading h1")     # Element that confirms dashboard load
    USER_MENU = (By.CSS_SELECTOR, ".userName-wrapper")               # Clicks to open the user dropdown
    LOGOUT_BUTTON = (By.XPATH, "//span[text()='Logout']")            # Actual logout button inside the menu
    EYE_ICON = (By.ID, "togglePassword")                             # Password visibility toggle
    SETTINGS_BUTTON = (By.XPATH, "//button[contains(text(), 'Settings')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/en/login"

    # ---------- Navigation ----------
    def navigate(self):
        self.open(self.url)
        assert "/en/login" in self.driver.current_url

    # ---------- Core Actions ----------
    def login(self, username=None, password=None):
        if username is None:
            username = Config.ADMIN_USERNAME
        if password is None:
            password = Config.ADMIN_PASSWORD
        logger.info(f"Attempting login with username: {username}")
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def logout(self):
        logger.info("Logging out")
        self.click(self.USER_MENU)          # open user menu
        self.click(self.LOGOUT_BUTTON)      # click logout

    def open_settings(self):
        self.click(self.SETTINGS_BUTTON)

    def reveal_password(self):
        logger.info("Toggling password visibility")
        self.click(self.EYE_ICON)

    # ---------- Wait Conditions ----------
    def wait_for_logged_in(self):
        self.wait.until(EC.url_contains("/dashboard"))
        self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADING))
        logger.info("Login successful – dashboard loaded.")

    def wait_for_error_message(self, expected_substring):
        try:
            self.wait.until(EC.text_to_be_present_in_element(self.FLASH_MESSAGE, expected_substring))
        except:
            self.wait.until(lambda d: expected_substring in d.page_source)
        logger.info(f"Error message '{expected_substring}' appeared.")

    # ---------- Getters ----------
    def get_flash_message(self):
        return self.get_text(self.FLASH_MESSAGE)

    def get_password_field_type(self):
        return self.find_element(self.PASSWORD_INPUT).get_attribute("type")

    # ---------- Assertions ----------
    def assert_login_successful(self):
        self.assert_element_displayed(self.DASHBOARD_HEADING)
        logger.info("Login successful – dashboard heading is present.")

    def assert_login_failed(self, expected_error_substring):
        self.assert_element_contains_text(self.FLASH_MESSAGE, expected_error_substring)
        logger.info(f"Login failed as expected with message containing '{expected_error_substring}'")

    def assert_on_login_page(self):
        self.assert_title_contains("Login")
        self.assert_element_displayed(self.LOGIN_BUTTON)
        self.assert_element_not_displayed(self.LOGOUT_BUTTON)
        