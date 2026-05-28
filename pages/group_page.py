"""
Page Object for Group Management.
Handles groups (Settings → Groups).
"""

from selenium.webdriver.common.by import By
from time import sleep
from pages.base_page import BasePage
from utils.logger import logger
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class GroupPage(BasePage):
    """
    Groups management page.
    """
    ADD_GROUP_BUTTON = (By.XPATH, "//button[span[text()='Add Group']]")
    GROUP_NAME = (By.ID, "name")
    DESCRIPTION = (By.ID, "description")
    SAVE_BUTTON = (By.ID, "addNetworkSubmitButton")
    EDIT_ICON = (By.CSS_SELECTOR, "[mattooltip='Edit this group']")
    DELETE_ICON = (By.CSS_SELECTOR, "[mattooltip='Delete this group']")
    SEARCH_BAR = (By.XPATH, "//input[@placeholder='Search using ID, Name']")
    GROUP_TABLE = (By.CSS_SELECTOR, "table.mat-mdc-table.mdc-data-table__table")
    CHECKBOX_HEADER = (By.XPATH, "//th[contains(@class, 'cdk-column-checkBox')]//mat-checkbox//div[contains(@class, 'mdc-checkbox')]")
    DELETE_GROUPS_BUTTON = (By.CLASS_NAME, "deleteAllBtn")
    CONFIRM_DELETE = (By.XPATH, "//button[span[text()='Yes']]")
    CHECK_BOX = (By.XPATH, "//input[@type='checkbox' and contains(@class, 'mdc-checkbox__native-control')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/settings/groups"
        
    def navigate(self):
        self.open(self.url)
        #There needs to be at least one group in this page, so we check for the table instead of an empty state message.
        self.assert_element_displayed(self.GROUP_TABLE)

        """Method for adding a group"""
    def add_group(self, name):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ADD_GROUP_BUTTON)
        ).click()
        
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.GROUP_NAME)
        ).click()
        self.type(self.GROUP_NAME, name)
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.SAVE_BUTTON)
        ).click()

        """Method for deleting a group using an icon"""
    def delete_using_icon(self):
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.DELETE_ICON)
        ).click()
    
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.CONFIRM_DELETE)
        ).click()
    
        """Method for searching for a group using the search bar"""
    def search_group(self, keyword):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SEARCH_BAR)
        ).click()
        self.type(self.SEARCH_BAR, keyword)
        
        """Method for deleting a group using the button"""
    def delete_multiple_groups_using_button(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.CHECKBOX_HEADER)
        ).click()
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.DELETE_GROUPS_BUTTON)
        ).click()
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CONFIRM_DELETE)
        )
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
        assert not found, f"Group '{name}' should not be in list but its present"
        logger.info(f"Group '{name}' correctly absent")