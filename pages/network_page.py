"""
Page Object for Network Management.
Handles CRUD operations on networks.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import logger


class NetworkPage(BasePage):
    """
    Represents the networks management page (Settings → Networks).
    """

    # Locators
    ADD_NETWORK_BUTTON = (By.XPATH, "//span[contains(text(), 'Add Network')]")
    NETWORK_NAME = (By.ID, "addNetworkResourceName")
    REPORT_DETONATORS_CHECK = (By.ID, "mat-mdc-checkbox-450-input")
    IN_USE_CHECK = (By.ID, "mat-mdc-checkbox-451-input")
    SAVE_BUTTON = (By.ID, "addNetworkSubmitButton")
    EDIT_ICON = (By.CSS_SELECTOR, "[mattooltip='Edit this network']")
    DELETE_ICON = (By.XPATH, "//span[text()='Delete Networks']")
    SEARCH_BAR = (By.CSS_SELECTOR, "input[placeholder='Search using ID, Name']")
    NETWORK_TABLE = (By.CSS_SELECTOR, "table.mat-mdc-table")
    CHECKBOX_HEADER = (By.CSS_SELECTOR, "th input[type='checkbox']")
    DELETE_NETWORKS_BUTTON = (By.XPATH, "//span[contains(text(), 'Delete Networks')]")
    CONFIRM_DELETE = (By.CSS_SELECTOR, "button.yesBtn")

#----------------------- Actions ----------------------
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/settings/networks"

    def navigate(self):
        """Go to networks page."""
        self.open(self.url)
        self.assert_element_displayed(self.NETWORK_TABLE)

    def add_network(self, name, report_detonators=True, in_use=True):
        """
        Add a new network with the given details.
        Steps from test plan: supply information, check boxes, click Add.
        """
        self.click(self.ADD_NETWORK_BUTTON)
        self.type(self.NETWORK_NAME, name)
        
        self.click(self.REPORT_DETONATORS_CHECK)
        if not in_use:
            self.click(self.IN_USE_CHECK)
        self.click(self.SAVE_BUTTON)
        # Wait for the network to appear in the table (implicitly via search)
        self.search_network(name)
        self.assert_network_in_list(name)

    def search_network(self, keyword):
        """Search for a network by ID or name."""
        self.type(self.SEARCH_BAR, keyword)

    def delete_first_network(self):
        """Delete the first network in the list using the delete icon."""
        self.click(self.DELETE_ICON)
        self.click(self.CONFIRM_DELETE)

    def get_network_rows(self):
        """Return all rows in the network table."""
        return self.find_elements((By.CSS_SELECTOR, "tbody tr"))

    def assert_network_in_list(self, name):
        """Assert that a network with the given name appears in the table."""
        rows = self.get_network_rows()
        found = any(name in row.text for row in rows)
        assert found, f"Network '{name}' not found in list"
        logger.info(f"Network '{name}' found in list")

    def assert_network_not_in_list(self, name):
        """Assert that a network with the given name does NOT appear."""
        rows = self.get_network_rows()
        found = any(name in row.text for row in rows)
        assert not found, f"Network '{name}' should not be in list but was found"
        logger.info(f"Network '{name}' correctly absent")