from pytest import Config
from selenium.webdriver.common.by import By
import time
from pages.base_page import BasePage
from utils.logger import logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os

class DevicePage(BasePage):
    """
    Represents the devices management page (Settings → Devices).
    """

    # ----------------------- Add device locators ----------------------
    ADD_DEVICE_BUTTON = (By.CSS_SELECTOR, "button.addBtn")
    NETWORK_DROPDOWN = (By.XPATH, "//span[text()='Network']/ancestor::div[contains(@class, 'mat-mdc-select-trigger')]")
    NETWORK_TYPE_OPTION = (By.XPATH, "//span[contains(text(), 'ETHERNET')]")
    NETWORK_INTERFACE_DROPDOWN = (By.XPATH, "//span[text()='Network Interface']/ancestor::div[contains(@class, 'mat-mdc-select-trigger')]")
    NETWORK_INTERFACE_OPTION = (By.XPATH, "//span[contains(text(), 'Ethernet')]")
    DEVICE_TYPE_DROPDOWN = (By.XPATH, "//span[text()='Device Type']/ancestor::div[contains(@class, 'mat-mdc-select-trigger')]")
    DEVICE_TYPE_OPTION = (By.XPATH, "//span[contains(text(), 'BCU')]")
    MANAGER_SELECT = (By.XPATH, "//div[contains(@class, 'mat-mdc-select-value')]//span[text()='None']/ancestor::div[contains(@class, 'mat-mdc-select-trigger')]")
    
    # -----------------------Edit device locators -----------------------
    NETWORK_EDIT_DROPDOWN = (By.XPATH, "//label[contains(., 'Network')]/ancestor::div[contains(@class, 'mat-mdc-form-field')]//div[contains(@class, 'mat-mdc-select-trigger')]")
    NETWORK_TYPE_OPTION_EDIT = (By.XPATH, "//span[@class='mdc-list-item__primary-text' and contains(text(), 'ETHER-911')]")
    NETWORK_INTERFACE_EDIT_DROPDOWN = (By.XPATH, "//label[contains(., 'Network Interface')]/ancestor::div[contains(@class, 'mat-mdc-form-field')]//div[contains(@class, 'mat-mdc-select-trigger')]")
    NETWORK_INTERFACE_OPTION_EDIT = (By.XPATH, "//mat-option[contains(., 'Ethernet')]")
    DEVICE_TYPE_EDIT_DROPDOWN = (By.XPATH, "//label[contains(., 'Device Type')]/ancestor::div[contains(@class, 'mat-mdc-form-field')]//div[contains(@class, 'mat-mdc-select-trigger')]")
    DEVICE_TYPE_OPTION_FOR_EDIT = (By.XPATH, "//mat-option[contains(., 'BCU')]")
    
    # ----------------------- Common locators ---------------------------
    DEVICE_ID = (By.ID, "id")                                       
    DEVICE_IP = (By.ID, "ipAddress")                                
    LOCATION = (By.ID, "location")
    SAVE_BUTTON = (By.ID, "addDeviceSubmitButton")       
    EDIT_ICON = (By.XPATH, "//mat-icon[@mattooltip='Edit this Device' and text()='edit']")  
    DELETE_ICON = (By.CSS_SELECTOR, "[mattooltip='Delete this Device']")
    SEARCH_BAR = (By.CSS_SELECTOR, "input[placeholder='Search using ID, Location, IP']")
    DEVICE_TABLE = (By.CSS_SELECTOR, "table.mat-mdc-table")         
    CHECKBOX_HEADER = (By.XPATH, "//th[contains(@class, 'mat-column-checkBox')]//div[contains(@class, 'mdc-checkbox')]")
    DELETE_MULTIPLE_DEVICES_BUTTON = (By.XPATH, "//span[contains(text(), 'Delete Devices')]")              
    POPUP_DIALOG = (By.XPATH, "//div[contains(@class, 'mat-mdc-dialog-container')]")
    CONFIRM_DELETE = (By.CSS_SELECTOR, ".yesBtn")
    CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[contains(@class, 'yesBtn') and contains(., 'Yes')]")
    IS_TABLE_EMPTY = (By.XPATH, "//h2[normalize-space()='No Devices Present']") # Heading shown when no devices are present

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/settings/devices"

    def navigate(self):
        """Go to devices page."""
        self.open(self.url)
        self.assert_element_displayed(self.DEVICE_TABLE)

    def add_device(self, device_id, ip, location="" ):
        """
        Add a new device with required fields.
        Steps from test plan: click Add Device, fill ID, IP, location, save.
        """
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.ADD_DEVICE_BUTTON)
        ).click()
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.DEVICE_ID)
        ).click()
    
        self.type(self.DEVICE_ID, device_id)
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.LOCATION)
        ).click()
        
        self.type(self.LOCATION, location)

        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.NETWORK_DROPDOWN)
        ).click()
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.NETWORK_TYPE_OPTION)
        ).click()
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.NETWORK_INTERFACE_DROPDOWN)
        ).click()
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.NETWORK_INTERFACE_OPTION)
        ).click()
   
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.DEVICE_TYPE_DROPDOWN)
        ).click()
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.DEVICE_TYPE_OPTION)
        ).click()
        
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.DEVICE_IP)
        ).clear()
        
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.DEVICE_IP)
        ).send_keys(ip)
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.SAVE_BUTTON)
        ).click()
        
        # Verify device appears
        self.assert_device_in_list(device_id)

    def edit_device(self, new_location, new_ip):
        """Edit a device."""
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.EDIT_ICON)
        ).click()
        
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.LOCATION)
        ).clear()
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.LOCATION)
        ).click()
        
        self.type(self.LOCATION, new_location)
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.NETWORK_EDIT_DROPDOWN)
        ).click()
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.NETWORK_TYPE_OPTION_EDIT)
        ).click()
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.NETWORK_INTERFACE_EDIT_DROPDOWN)
        ).click()
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.NETWORK_INTERFACE_OPTION_EDIT)
        ).click()
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.DEVICE_TYPE_EDIT_DROPDOWN)
        ).click()
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.DEVICE_TYPE_OPTION_FOR_EDIT)
        ).click()
        
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.DEVICE_IP)
        ).clear()
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.DEVICE_IP)
        ).send_keys(new_ip)
        
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.SAVE_BUTTON)
        ).click()
    
    def search_device(self, keyword):
        """Search for a device by ID, location, or IP."""
        # Ensure search bar is focused before typing
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.SEARCH_BAR)
        ).click()                           
        self.type(self.SEARCH_BAR, keyword)

    def delete_device(self, device_id):
        # Locate the delete icon for the specific device
        delete_icon_xpath = f"//tr[.//td[contains(@class,'cdk-column-id')]/a[text()='{device_id}']]//span[@mattooltip='Delete this Device']"
        delete_locator = (By.XPATH, delete_icon_xpath)

        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(delete_locator)
            )
        except TimeoutException:
            raise Exception(f"Delete icon for device {device_id} not found or not clickable")

        self.click(delete_locator)

        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.CONFIRM_DELETE)
            )
        except TimeoutException:
            raise Exception("Confirmation dialog did not appear after clicking delete")

        self.click(self.CONFIRM_DELETE)

        # Wait for the device row to disappear
        row_locator = (By.XPATH, f"//tr[.//td[contains(@class,'cdk-column-id')]/a[text()='{device_id}']]")
        WebDriverWait(self.driver, 20).until(
            EC.invisibility_of_element_located(row_locator)
        )

    def delete_multiple_devices(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.CHECKBOX_HEADER)
        ).click()
        
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.DELETE_MULTIPLE_DEVICES_BUTTON)
        ).click()
        
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.CONFIRM_DELETE_BUTTON)
        ).click()
        
    def get_device_rows(self):
        """Return all rows in the device table."""
        return self.find_elements((By.CSS_SELECTOR, "tbody tr"))

    def assert_device_in_list(self, device_id):
        """Assert that a device with the given ID appears in the list."""
        rows = self.get_device_rows()
        found = any(device_id in row.text for row in rows)
        assert found, f"Device '{device_id}' not found in list"
        logger.info(f"Device '{device_id}' found in list")

    def assert_device_not_in_list(self, device_id):
        """Assert that a device with the given ID does NOT appear."""
        rows = self.get_device_rows()
        found = any(device_id in row.text for row in rows)
        assert not found, f"Device '{device_id}' should not be in list but was found"
        logger.info(f"Device '{device_id}' correctly absent")
        
    def assert_no_devices_present(self,driver):
        try:
            element = driver.find_element(By.XPATH, "//h2[normalize-space()='No Devices Present']")
            assert element.is_displayed(), "Element 'No Devices Present' is present but not visible"
        except NoSuchElementException:
            assert False, "Expected 'No Devices Present' heading not found"
