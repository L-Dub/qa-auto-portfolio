"""
Page Object for Email Recipients.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RecipientPage(BasePage):
    """
    Email Recipients management (Settings → Email Recipients).
    """

    ADD_RECIPIENT_BUTTON = (By.XPATH, "//button[contains(., 'Add Recipient')]")
    #USERNAME_FIELD = (By.ID, "username")
    FIRST_NAME = (By.ID, "addRecipientFullName")
    LAST_NAME = (By.XPATH, "//input[@placeholder='Enter the recipient last name']")
    EMAIL = (By.XPATH, "//input[@placeholder='Enter the recipient email']")
    SAVE_BUTTON = (By.ID, "addRecipientSubmitButton")
    EDIT_ICON = (By.XPATH, "//mat-icon[@mattooltip='Edit this recipient']")
    DELETE_ICON = (By.XPATH, "//span[@mattooltip='Delete this recipient']")
    SEARCH_BAR = (By.XPATH, "//input[@placeholder='Search using Username, First Name, Last Name']")
    RECIPIENT_TABLE = (By.CSS_SELECTOR, "table.mat-mdc-table.mdc-data-table__table")
    CHECKBOX_HEADER = (By.CSS_SELECTOR, "th input[type='checkbox']")
    DELETE_RECIPIENTS_BUTTON = (By.XPATH, "//button[contains(., 'Delete Recipients')]")
    CONFIRM_DELETE = (By.XPATH, "//button[contains(., 'Yes')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/settings/email-recipients"

    def navigate(self):
        self.open(self.url)
        self.assert_element_displayed(self.RECIPIENT_TABLE)

    def add_recipient(self, first, last, email):
        self.click(self.ADD_RECIPIENT_BUTTON)
        #self.type(self.USERNAME_FIELD, username)
        self.type(self.EMAIL, email)
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.click(self.SAVE_BUTTON)
        """self.search_recipient(username)
        self.assert_recipient_in_list(username)
        """

    def search_recipient(self, keyword):
        self.type(self.SEARCH_BAR, keyword)

    def delete_first_recipient(self):
        self.click(self.DELETE_ICON)
        self.click(self.CONFIRM_DELETE)

    def get_recipient_rows(self):
        return self.find_elements((By.CSS_SELECTOR, "tbody tr"))

    def assert_recipient_in_list(self, username):
        rows = self.get_recipient_rows()
        found = any(username in row.text for row in rows)
        assert found, f"Recipient '{username}' not found"
        logger.info(f"Recipient '{username}' found")

    def assert_recipient_not_in_list(self, username):
        rows = self.get_recipient_rows()
        found = any(username in row.text for row in rows)
        assert not found, f"Recipient '{username}' should not be in list"
        logger.info(f"Recipient '{username}' correctly absent")