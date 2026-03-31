"""
Page Object for Network Management (Settings → Networks).
"""

from unicodedata import name

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import logger
import time


class NetworkPage(BasePage):
    # Locators
    ADD_NETWORK_BUTTON = (By.XPATH, "//span[contains(text(), 'Add Network')]")
    NETWORK_NAME_INPUT = (By.ID, "addNetworkResourceName")
    NETWORK_EDIT_NAME_INPUT = (By.ID, "networkResourceName")
    REPORT_DETONATORS_CHECK = (By.XPATH, "//mat-checkbox[@formcontrolname='reportDets']")
    IN_USE_CHECK = (By.XPATH, "//mat-checkbox[@formcontrolname='inUse']")
    SAVE_BUTTON = (By.ID, "addNetworkSubmitButton")
    SAVE_EDIT_BUTTON = (By.XPATH, "//button[.//mat-icon[text()='save'] and contains(., 'Save')]")
    SEARCH_BAR = (By.CSS_SELECTOR, "input[placeholder='Search using ID, Name']")
    NETWORK_TABLE = (By.CSS_SELECTOR, "table.mat-mdc-table")
    CHECKBOX = (By.CSS_SELECTOR, "input.mdc-checkbox__native-control[type='checkbox']")
    
    # Button locators that require dynamic row context
    DELETE_ICON = (By.XPATH, "//span[@mattooltip='Delete this network']")
    DELETE_BTN = (By.XPATH, "//span[contains(text(),'delete')]")
    CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[@class='yesBtn']")
    EDIT_ICON = (By.XPATH, "//mat-icon[@mattooltip='Edit this network']")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/settings/networks"

    def navigate(self):
        
        self.open(self.url)
        self.wait_for_table_to_load()
        logger.info("Navigated to Networks management page")

    def wait_for_table_to_load(self, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.NETWORK_TABLE)
        )

    def wait_for_network_to_appear(self, name: str, timeout: int = 12):
        def network_in_table(_):
            rows = self.get_network_rows()
            return any(name in (row.text or "") for row in rows)
        WebDriverWait(self.driver, timeout).until(network_in_table)

    def wait_for_network_to_disappear(self, name: str, timeout: int = 12):
        def network_not_in_table(_):
            rows = self.get_network_rows()
            return not any(name in (row.text or "") for row in rows)
        WebDriverWait(self.driver, timeout).until(network_not_in_table)

    def _click_material_checkbox(self, locator):
        try:
            checkbox = WebDriverWait(self.driver, 8).until(
                EC.element_to_be_clickable(locator)
            )
            checkbox.click()
        except Exception:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].click();", element)

    # ====================== Main Actions ======================
    
    #================== Add a new network ======================.
    def add_network(self, name: str, report_detonators: bool = True, in_use: bool = True):
        
        logger.info(f"Adding network: {name}")

        self.click(self.ADD_NETWORK_BUTTON)
        self.type(self.NETWORK_NAME_INPUT, name)

        if report_detonators:
            self._click_material_checkbox(self.REPORT_DETONATORS_CHECK)
        if in_use:
            self._click_material_checkbox(self.IN_USE_CHECK)

        self.click(self.SAVE_BUTTON)

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.SAVE_BUTTON)
        )

        self.search_network(name)
        self.wait_for_network_to_appear(name)
        self.assert_network_in_list(name)

    #================== Search for network in the list ======================
    def search_network(self, keyword: str):
        self.type(self.SEARCH_BAR, keyword)
        self.wait_for_table_to_load(timeout=8)
        
    #================== Delete a network in the list using the delete icon ======================
    def delete_network_using_icon(self, name: str):
        """Delete network - No broad try/except. Let failures raise naturally."""
        logger.info(f"Deleting network: {name}")

        self.search_network(name)

        # Find delete icon inside the specific row
        row_xpath = f"//tbody/tr[contains(., '{name}')]"
        delete_in_row = (By.XPATH, f"{row_xpath}{self.DELETE_ICON[1]}")

        # These lines will now properly fail the test if something goes wrong
        delete_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(delete_in_row)
        )
        delete_btn.click()

        self.click(self.CONFIRM_DELETE_BUTTON)
        self.wait_for_network_to_disappear(name)

        #================== Edit a network ======================
    def edit_network(self, new_name, old_name):
        
        logger.info(f"Editing network from '{old_name}' to '{new_name}'")

        self.search_network(old_name)

        # Clear and type new name
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.EDIT_ICON)
        ).click()  # Click the edit icon to open the form
        
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.NETWORK_EDIT_NAME_INPUT)
        ).clear()  # Clear existing name
        
        self.type(self.NETWORK_EDIT_NAME_INPUT, new_name)
        
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SAVE_EDIT_BUTTON)
        ).click()  # Click save and wait for form to close
        
        self.search_network(new_name)
        
    def delete_network_using_btn(self, name):
        logger.info(f"Deleting network {name} using the delete button")
        
        # Find the row containing the network name and click its checkbox
        checkbox_locator = (By.XPATH, f"//tr[contains(., '{name}')]//mat-checkbox")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(checkbox_locator)
        ).click()
        
        logger.info("Checkbox checked, now clicking delete button")
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.DELETE_BTN)
        ).click()
        
        self.click(self.CONFIRM_DELETE_BUTTON)
        self.wait_for_network_to_disappear(name)
        
    def get_network_rows(self):
            self.wait_for_table_to_load()
            return self.find_elements((By.CSS_SELECTOR, "tbody tr"))

    """Assertions for network in the list"""
    def assert_network_in_list(self, name: str):
        rows = self.get_network_rows()
        found = any(name in (row.text or "") for row in rows)
        assert found, f"Network '{name}' not found in the list"
        logger.info(f"Network '{name}' found in list")

    """Assertions for network not in the list"""
    def assert_network_not_in_list(self, name: str):
        rows = self.get_network_rows()
        found = any(name in (row.text or "") for row in rows)
        assert not found, f"Network '{name}' is still present in the list"
        logger.info(f"Network '{name}' correctly not in list")
        