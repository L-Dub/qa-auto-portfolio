"""
Page Object for Group Management.
Handles groups (Settings → Groups).
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import logger

class GroupPage(BasePage):
    """
    Groups management page.
    """

    ADD_GROUP_BUTTON = (By.XPATH, "//button[.//span[text()='Add Group']]")
    GROUP_NAME = (By.ID, "name")
    # DESCRIPTION = (By.ID, "description")
    SAVE_BUTTON = (By.ID, "addNetworkSubmitButton")
    EDIT_ICON = (By.CSS_SELECTOR, "[mattooltip='Edit this group']")
    DELETE_ICON = (By.XPATH, "//span[@mattooltip='Delete this group']")
    SEARCH_BAR = (By.XPATH, "//input[@placeholder='Search using ID, Name']")
    GROUP_TABLE = (By.CSS_SELECTOR, "table.mat-mdc-table.mdc-data-table__table")
    CHECKBOX_HEADER = (By.XPATH, "//th[contains(@class, 'cdk-column-checkBox')]//input[@type='checkbox']")
    DELETE_GROUPS_BUTTON = (By.CLASS_NAME, "deleteAllBtn")
    CONFIRM_DELETE = (By.CLASS_NAME, "yesBtn")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/settings/groups"

    def navigate(self):
        self.open(self.url)
        self.assert_element_displayed(self.GROUP_TABLE)

    def add_group(self, name, description=""):
        self.click(self.ADD_GROUP_BUTTON)
        self.type(self.GROUP_NAME, name)
        '''if description:
            self.type(self.DESCRIPTION, description)
        '''
        self.click(self.SAVE_BUTTON)
        self.search_group(name)
        self.assert_group_in_list(name)

    def search_group(self, keyword):
        self.type(self.SEARCH_BAR, keyword)

    def delete_first_group(self):
        self.click(self.DELETE_ICON)
        self.click(self.CONFIRM_DELETE)

    def get_group_rows(self):
        return self.find_elements((By.CSS_SELECTOR, "tbody tr"))

    def assert_group_in_list(self, name):
        rows = self.get_group_rows()
        found = any(name in row.text for row in rows)
        assert found, f"Group '{name}' not found"
        logger.info(f"Group '{name}' found")

    def assert_group_not_in_list(self, name):
        rows = self.get_group_rows()
        found = any(name in row.text for row in rows)
        assert not found, f"Group '{name}' should not be in list"
        logger.info(f"Group '{name}' correctly absent")