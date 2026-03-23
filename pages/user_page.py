"""
Page Object for User Management pages.
Handles viewing, adding, editing, deleting, and searching users.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils import logger


class UserPage(BasePage):
    """
    Represents the user management section (Settings → Users).
    """

    # Locators
    ADD_USER_BUTTON = (By.XPATH, "//span[contains(text(),'Add User')]")
    EDIT_ICON = (By.CSS_SELECTOR, "[mattooltip='Edit this user']")
    DELETE_ICON = (By.CSS_SELECTOR, "[mattooltip='Delete this user']")
    RESET_PASSWORD_ICON = (By.CSS_SELECTOR, "[mattooltip='Reset this user's password']")
    SEARCH_BAR = (By.CSS_SELECTOR, "input[placeholder='Search using Username, First Name, Surname']")
    USER_TABLE = (By.CSS_SELECTOR, "//table[role='table']")
    CHECKBOX_HEADER = (By.CSS_SELECTOR, "th input[type='checkbox']")
    CHECKBOX_ROW = (By.CSS_SELECTOR, "td input[type='checkbox']")
    DELETE_USERS_BUTTON = (By.XPATH, "//span[contains(text(),'Delete Users')]")
    CONFIRM_DELETE = (By.CSS_SELECTOR, "button.yesBtn")   # Confirmation popup button

    # Form fields (for add/edit)
    USERNAME_FIELD = (By.ID, "addUserUsername")
    FIRST_NAME_FIELD = (By.ID, "addUserFirstName")
    LAST_NAME_FIELD = (By.ID, "addUserSurname")
    EMAIL_FIELD = (By.ID, "addUserEmail")
    ROLE_DROPDOWN = (By.XPATH, "//div[contains(@class, 'mat-mdc-select') and .//span[text()='Role']]")
    ROLE_SELECT = (By.XPATH, "//span[contains(text(), 'detnet engineer')]")  # Example role option; adjust as needed
    ADD_USER_BUTTON = (By.XPATH, "//span[contains(text(), 'Add User')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/settings/users"

    # ---------- Navigation ----------
    def navigate(self):
        """Go to the users page."""
        self.open(self.url)
        self.assert_element_displayed(self.USER_TABLE)  # Ensure page loaded

    # ---------- Actions ----------
    def click_add_user(self):
        """Click the 'Add User' button."""
        self.click(self.ADD_USER_BUTTON)
        
    def reset_user_password(self, index=1):
        """Click the reset password icon for the user at the given row index."""
        icons = self.find_elements(self.RESET_PASSWORD_ICON)
        assert len(icons) > index, f"No reset password icon at index {index}"
        icons[index].click()
        
    def click_edit_user(self, index=1):
        """Click the edit icon for the user at the given row index."""
        icons = self.find_elements(self.EDIT_ICON)
        assert len(icons) > index, f"No edit icon at index {index}"
        icons[index].click()
        
    def search_user(self, keyword):
        """Type a search keyword into the search bar."""
        self.type(self.SEARCH_BAR, keyword)

    def select_user_checkbox(self, index=0):
        """Select the checkbox of the user at the given row index."""
        checkboxes = self.find_elements(self.CHECKBOX_ROW)
        assert len(checkboxes) > index, f"No checkbox at index {index}"
        checkboxes[index].click()

    def select_all_checkbox(self):
        """Click the header checkbox to select all users."""
        self.click(self.CHECKBOX_HEADER)

    def click_delete_selected(self):
        """Click the 'Delete Users' button for multiple deletion."""
        self.click(self.DELETE_USERS_BUTTON)
        self.click(self.CONFIRM_DELETE)   # Confirm the popup

    def delete_first_user(self):
        """Delete the first user in the table using the row delete icon."""
        self.click(self.DELETE_ICON)
        self.click(self.CONFIRM_DELETE)

    def fill_user_form(self, username, first_name, last_name, email):
        """Fill the add/edit user form (assumes form is already open)."""
        self.type(self.USERNAME_FIELD, username)
        self.type(self.FIRST_NAME_FIELD, first_name)
        self.type(self.LAST_NAME_FIELD, last_name)
        self.type(self.EMAIL_FIELD, email)
        self.click(self.ROLE_DROPDOWN) # Click the role dropdown to open it
        self.click(self.ROLE_SELECT)  # Select the role from dropdown
        self.click(self.ADD_USER_BUTTON)

    # ---------- Getters ----------
    def get_user_rows(self):
        """Return all rows of the user table."""
        return self.find_elements((By.CSS_SELECTOR, "tbody tr"))

    def get_user_cell_text(self, row_index, column_index):
        """Get text from a specific cell (e.g., for verification)."""
        rows = self.get_user_rows()
        assert row_index < len(rows), f"Row {row_index} out of range"
        cells = rows[row_index].find_elements(By.TAG_NAME, "td")
        assert column_index < len(cells), f"Column {column_index} out of range"
        return cells[column_index].text

    # ---------- Assertions ----------
    def assert_user_in_list(self, username):
        """Assert that a user with the given username appears in the table."""
        self.search_user(username)
        rows = self.get_user_rows()
        # After search, there should be at least one row containing the username
        found = any(username in row.text for row in rows)
        assert found, f"User '{username}' not found in user list"
        logger.info(f"User '{username}' found in list")

    def assert_user_not_in_list(self, username):
        """Assert that a user with the given username does NOT appear after search."""
        self.search_user(username)
        rows = self.get_user_rows()
        # Either table is empty or none of the rows contain the username
        found = any(username in row.text for row in rows)
        assert not found, f"User '{username}' should not be in list but was found"
        logger.info(f"User '{username}' correctly absent from list")