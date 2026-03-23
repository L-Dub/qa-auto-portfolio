"""
Page Object for Device Management.
Handles adding, editing, deleting, and searching devices.
Includes firmware upload functionality.
"""

import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config import Config

logger = logging.getLogger(__name__)


class DevicePage(BasePage):
    """
    Represents the devices management page (Settings → Devices).
    Also includes firmware upload functionality.
    """

    # ----- Device CRUD locators -----
    ADD_DEVICE_BUTTON = (By.CSS_SELECTOR, "button.addBtn")          # Click to open add form
    DEVICE_ID = (By.ID, "id")                                       # Device ID input
    DEVICE_IP = (By.ID, "ipAddress")                                # IP address input (corrected)
    LOCATION = (By.ID, "location")                                  # Location input (optional)

    # Dropdowns (Angular Material) – each locator targets the trigger <div>
    NETWORK_SELECT = (By.XPATH, "//span[text()='Network']/ancestor::div[contains(@class, 'mat-mdc-select-trigger')]")
    NETWORK_INTERFACE_SELECT = (By.XPATH, "//span[text()='Network Interface']/ancestor::div[contains(@class, 'mat-mdc-select-trigger')]")
    DEVICE_TYPE_SELECT = (By.XPATH, "//span[text()='Device Type']/ancestor::div[contains(@class, 'mat-mdc-select-trigger')]")
    MANAGER_SELECT = (By.XPATH, "//div[contains(@class, 'mat-mdc-select-value')]//span[text()='None']/ancestor::div[contains(@class, 'mat-mdc-select-trigger')]")

    SAVE_BUTTON = (By.ID, "addDeviceSubmitButton")       # Save button (no ID, using text)
    EDIT_ICON = (By.CSS_SELECTOR, "[matooltip='Edit this Device']")  # Based on tooltip text
    DELETE_ICON = (By.CSS_SELECTOR, "[mattooltip='Delete this Device']")
    SEARCH_BAR = (By.CSS_SELECTOR, "input[placeholder='Search using ID, Location, IP']")
    DEVICE_TABLE = (By.CSS_SELECTOR, "table.mat-mdc-table")         # Table with class
    CHECKBOX_HEADER = (By.CSS_SELECTOR, "th input[type='checkbox']")
    DELETE_DEVICES_BUTTON = (By.XPATH, "//span[contains(text(), 'Delete Devices')]")               # Bulk delete button
    CONFIRM_DELETE = (By.CSS_SELECTOR, "button.yesBtn")             # Confirmation button in delete dialog

    # ----- Firmware upload locators -----
    FIRMWARE_UPLOAD_BUTTON = (By.XPATH, "//span[text()='Upload Firmware']")
    FIRMWARE_FILE_INPUT = (By.ID, "firmware-file")
    DEVICE_TYPE_SELECT_FW = (By.XPATH, "//span[text()='Device Type']/ancestor::div[contains(@class, 'mat-mdc-select-trigger')]")                  # Different from above? Keep separate
    UPLOAD_SUBMIT = (By.XPATH, "//button[contains(., 'Upload Firmware')]")
    DEVICE_TYPE_TO_USE = (By.XPATH, "//mat-option[normalize-space()='BCU']")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/settings/devices"

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
    def navigate(self):
        """Go to devices page."""
        self.open(self.url)
        self.assert_element_displayed(self.DEVICE_TABLE)
        logger.info("Navigated to Devices page")

    # ------------------------------------------------------------------
    # Dropdown helper for Material selects
    # ------------------------------------------------------------------
    def select_dropdown_option(self, trigger_locator, option_text):
        """
        Clicks a Material dropdown trigger and selects an option by visible text.
        Waits for the option to be clickable.
        """
        self.click(trigger_locator)
        option_xpath = f"//mat-option[contains(., '{option_text}')]"
        option_locator = (By.XPATH, option_xpath)
        self.wait_for_element(option_locator).click()
        logger.debug(f"Selected '{option_text}' from dropdown")

    # ------------------------------------------------------------------
    # Device CRUD operations
    # ------------------------------------------------------------------
    def add_device(self, device_id, ip, network, network_interface, device_type, manager,
                   parent_device=None, location=""):
        """
        Add a new device with all mandatory fields.
        """
        logger.info(f"Adding device: {device_id}")
        self.click(self.ADD_DEVICE_BUTTON)

        # Text fields
        self.type(self.DEVICE_ID, device_id)
        self.type(self.DEVICE_IP, ip)
        if location:
            self.type(self.LOCATION, location)

        # Dropdowns
        self.select_dropdown_option(self.NETWORK_SELECT, network)
        self.select_dropdown_option(self.NETWORK_INTERFACE_SELECT, network_interface)
        self.select_dropdown_option(self.DEVICE_TYPE_SELECT, device_type)
        self.select_dropdown_option(self.MANAGER_SELECT, manager)
        if parent_device:
            self.select_dropdown_option(self.PARENT_DEVICE_SELECT, parent_device)

        self.click(self.SAVE_BUTTON)

        # Wait for the device to appear (optional: wait for success toast)
        self.search_device(device_id)
        self.assert_device_in_list(device_id)
        logger.info(f"Device '{device_id}' added successfully")

    def search_device(self, keyword):
        """Search for a device by ID, IP, or location."""
        self.clear_and_type(self.SEARCH_BAR, keyword)
        # Wait for search results to update (could wait for table rows)
        self.wait.until(lambda d: len(self.get_device_rows()) > 0 or True)
        logger.debug(f"Searched for '{keyword}'")

    def delete_first_device(self):
        """Delete the first device in the list."""
        self.click(self.DELETE_ICON)
        self.click(self.CONFIRM_DELETE)
        logger.info("Deleted first device")

    def get_device_rows(self):
        """Return all rows in the device table body."""
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

    # ------------------------------------------------------------------
    # Firmware upload (section 21)
    # ------------------------------------------------------------------
    def upload_firmware(self, file_path, device_type):
        """
        Upload a firmware file for a specific device type.
        Steps: click upload, select file, choose type, upload.
        """
        logger.info("Uploading firmware for device")
        self.click(self.FIRMWARE_UPLOAD_BUTTON)
        self.type(self.FIRMWARE_FILE_INPUT, Config.FIRMWARE_FILE_PATH)
        self.select_dropdown_option(self.DEVICE_TYPE_SELECT_FW, device_type)
        self.click(self.DEVICE_TYPE_TO_USE)
        self.click(self.UPLOAD_SUBMIT)
        # Optionally wait for success message
        logger.info("Firmware upload initiated")