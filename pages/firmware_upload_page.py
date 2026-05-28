from pytest import Config
from selenium.webdriver.common.by import By
import time
from pages.base_page import BasePage
from utils.logger import logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os

class DevicePage(BasePage):
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

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/settings/devices"

    def navigate(self):
        """Go to devices page."""
        self.open(self.url)

    def upload_firmware(self, file_path, device_type="BCU"):

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
        