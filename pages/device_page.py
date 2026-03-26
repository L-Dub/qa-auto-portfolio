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


    # ----- Device CRUD locators -----
    ADD_DEVICE_BUTTON = (By.CSS_SELECTOR, "button.addBtn")          # Click to open add form
    DEVICE_ID = (By.ID, "id")                                       # Device ID input
    DEVICE_IP = (By.ID, "ipAddress")                                # IP address input (corrected)
    LOCATION = (By.ID, "location")                                  # Location input (optional)

    # Dropdowns (Angular Material) – each locator targets the trigger <div>
    NETWORK_SELECT = (By.XPATH, "//span[text()='Network']/ancestor::div[contains(@class, 'mat-mdc-select-trigger')]")
    NETWORK_TYPE_OPTION = (By.XPATH, "//span[contains(text(), 'ETHERNET')]")
    NETWORK_INTERFACE_SELECT = (By.XPATH, "//span[text()='Network Interface']/ancestor::div[contains(@class, 'mat-mdc-select-trigger')]")
    NETWORK_INTERFACE_OPTION = (By.XPATH, "//span[contains(text(), 'Ethernet')]")
    DEVICE_TYPE_SELECT = (By.XPATH, "//span[text()='Device Type']/ancestor::div[contains(@class, 'mat-mdc-select-trigger')]")
    DEVICE_TYPE_OPTION = (By.XPATH, "//span[contains(text(), 'BCU')]")
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
    SELECT_FILE_BTN = (By.XPATH, "//span[contains(text(), 'Select File')]")
    DEVICE_TYPE_SELECT_FW = (By.XPATH, "//span[text()='Device Type']/ancestor::div[contains(@class, 'mat-mdc-select-trigger')]") #This select the device type dropdown                 # Different from above? Keep separate
    UPLOAD_SUBMIT = (By.XPATH, "//button[contains(., 'Upload Firmware')]")
    DEVICE_TYPE_TO_USE = (By.XPATH, "//mat-option[normalize-space()='BCU']")

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
        self.click(self.ADD_DEVICE_BUTTON)
        self.type(self.DEVICE_ID, device_id)
        self.type(self.LOCATION, location)
        self.click(self.NETWORK_SELECT)
        self.click(self.NETWORK_TYPE_OPTION)
        self.click(self.NETWORK_INTERFACE_SELECT)
        self.click(self.NETWORK_INTERFACE_OPTION)
        self.click(self.DEVICE_TYPE_SELECT)
        self.click(self.DEVICE_TYPE_OPTION)
        self.type(self.DEVICE_IP, ip)
        self.click(self.SAVE_BUTTON)
        
        # Verify device appears
        self.assert_device_in_list(device_id)

    def search_device(self, keyword):
        """Search for a device by ID, location, or IP."""
        self.click(self.SEARCH_BAR)  # Ensure search bar is focused
        self.type(self.SEARCH_BAR, keyword)

    def delete_device(self, device_id):
        # 1. Locate the delete icon for the specific device
        delete_icon_xpath = f"//tr[.//td[contains(@class,'cdk-column-id')]/a[text()='{device_id}']]//span[@mattooltip='Delete this Device']"
        delete_locator = (By.XPATH, delete_icon_xpath)

        # 2. Wait for the delete icon to be clickable (max 10 sec)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(delete_locator)
            )
        except TimeoutException:
            raise Exception(f"Delete icon for device {device_id} not found or not clickable")

        # 3. Click the delete icon
        self.click(delete_locator)

        # 4. Wait for the confirmation dialog and click the Yes button
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.CONFIRM_DELETE)
            )
        except TimeoutException:
            raise Exception("Confirmation dialog did not appear after clicking delete")

        self.click(self.CONFIRM_DELETE)

        # 5. Optional: Wait for the device row to disappear
        row_locator = (By.XPATH, f"//tr[.//td[contains(@class,'cdk-column-id')]/a[text()='{device_id}']]")
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located(row_locator)
        )

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
        time.sleep(1)  # Small wait to ensure file is processed by the UI
        # Step 3: Select device type (if needed after file selection)
        self.click(self.DEVICE_TYPE_SELECT)
        time.sleep(1)  # Small wait to ensure dropdown options are loaded
        self.click(self.DEVICE_TYPE_TO_USE)  # Click the option matching device_type

        time.sleep(1)  # Small wait to ensure UI updates before submitting

        # Step 4: Submit the upload
        self.click(self.UPLOAD_SUBMIT)
        time.sleep(1)  # Wait for upload to process (adjust as needed)
        # Optionally wait for success message
        logger.info(f"Firmware upload initiated for {device_type} from {os.path.basename(file_path)}")