from pytest import Config
from selenium.webdriver.common.by import By
import time
from pages.base_page import BasePage
from tests.conftest import driver
from utils.logger import logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os

class FirmwareUploadPage(BasePage):
    """
    Represents the devices management page (Settings → Devices).
    Also includes firmware upload functionality.
    """

    # Dropdowns (Angular Material) – each locator targets the trigger <div>
    DEVICE_TYPE_SELECT = (By.XPATH, "//span[text()='Device Type']/ancestor::div[contains(@class, 'mat-mdc-select-trigger')]")
    DEVICE_TYPE_OPTION = (By.XPATH, "//span[contains(text(), 'BCU')]")

    # ----- Firmware upload locators -----
    FIRMWARE_UPLOAD_BUTTON = (By.XPATH, "//span[text()='Upload Firmware']")
    SELECT_FILE_BTN = (By.XPATH, "//span[contains(text(), 'Select File')]")
    DEVICE_TYPE_SELECT_FW = (By.XPATH, "//span[text()='Device Type']/ancestor::div[contains(@class, 'mat-mdc-select-trigger')]") #This select the device type dropdown                 # Different from above? Keep separate
    UPLOAD_SUBMIT = (By.XPATH, "//button//span[contains(text(), 'Upload Firmware')]")
    DEVICE_TYPE_TO_USE = (By.XPATH, "//mat-option[normalize-space()='BCU']")
    UPGRADE_SELECTED_DEVICES = (By.XPATH, "//i[contains(@class, 'icon-upgrade')]/ancestor::button")
    DEVICE_IS_UPGRADING = (By.XPATH, "//mat-progress-spinner")
    BOOTLOADER_ICON = (By.XPATH, "//i[contains(@class, 'icon-upgrade') and contains(@class, 'positive')]")
    BOOTLOAD_SELECTED_DEVICES = (By.XPATH, "//button[@mattooltip='Bootload Selected Devices']")
    NEW_DEVICE_VERSION = (By.XPATH, "//span[@class='configurationValue' and text()='51316']")   #Replace the text with the expected version number after upgrade to verify the new version is displayed on the card.

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/settings/devices"

    def navigate(self):
        """Go to devices page."""
        self.open(self.url)

    def device_update(self, file_path, device_type="BCU"):

        # Step 1: Open the upload form
        self.click(self.FIRMWARE_UPLOAD_BUTTON)

        # Step 2: Find the file input element (type="file") and send the path
        # The file input might be hidden, but it's present in the DOM.
        # Adjust the locator to match your page – common selectors:
        file_input_locator = (By.CSS_SELECTOR, "input[type='file']")
        # Wait for the file input to be present and interactable
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(file_input_locator)
        )
        file_input.send_keys(file_path)   # Send the absolute path to the file

        # Step 3: Select device type after file selection
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.DEVICE_TYPE_SELECT)
        ).click()

        # Click the option matching device_type
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.DEVICE_TYPE_TO_USE)
        ).click()
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.UPLOAD_SUBMIT)
        ).click()
        
        #Wait for success message
        logger.info(f"Firmware upload initiated for {device_type} from {os.path.basename(file_path)}")
        
    def select_device(self, device_name: str):
        """Click the checkbox for a specific device - Robust version"""
        print(f"Attempting to select device: '{device_name}'")

        # 1. Find the card by device name
        # 2. Find the mat-checkbox INSIDE that card (we click the mat-checkbox itself,
        #    NOT the hidden <input> that Angular Material uses)
        locator = (By.XPATH,
            f"//bcu-card-high-detail[.//span[@class='locationLabel' and contains(text(), '{device_name}')]]"
            "//mat-checkbox"
        )

        try:
            checkbox = WebDriverWait(self.driver, 25).until(
                EC.element_to_be_clickable(locator)
            )
            
            # Optional: scroll into view (helps with flaky clicks on modern UIs)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
            
            checkbox.click()
            
            print(f"✅ SUCCESS: Checkbox clicked for device '{device_name}'")

        except TimeoutException:
            self.driver.save_screenshot(f"debug_checkbox_failed_{device_name}.png")
            print(f"❌ Timeout: Could not locate checkbox for '{device_name}'")
            print("Screenshot saved for debugging.")
            
            # Extra debug info
            print("Current page title:", self.driver.title)
            print("URL:", self.driver.current_url)
            raise
        
    def upgrade_selected_devices(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.UPGRADE_SELECTED_DEVICES)
        ).click()
        
    def bootload_device(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.BOOTLOAD_SELECTED_DEVICES)
        ).click()
        
    def assert_upgrade_successful(self):
        try:
            WebDriverWait(self.driver, 1200).until(
                EC.presence_of_element_located(self.BOOTLOADER_ICON)
            )
        except:
            assert False, f"Upgrade NOT successful - Bootloader icon not found after upgrade completion"
        
    def assert_device_is_upgrading(self):
        assert self.driver.find_elements(*self.DEVICE_IS_UPGRADING), "Device is NOT upgrading - Progress spinner not found"
        
    def assert_bootloading_is_successful(self):
        try:
            WebDriverWait(self.driver, 600).until(
                EC.presence_of_element_located(self.NEW_DEVICE_VERSION)
            )
        except:
            assert False, f"Bootload NOT successful - New device version not displayed after bootload completion"
