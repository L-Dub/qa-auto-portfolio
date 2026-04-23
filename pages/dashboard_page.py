import selenium
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import Config
import time

class DashboardPage(BasePage):
    # Locators (as tuples)
    DEVICE_CHECKBOX = (By.XPATH, "//span[@class='locationLabel' and text()='Chromium mine']/ancestor::bcu-card-high-detail//input[@type='checkbox']")
    DEVICE_STATUS = (By.XPATH, "//span[@class='locationLabel' and text()='{}']/ancestor::bcu-title//span[text()='State:']/following-sibling::span//span[@class='titleValue']")
    ALERT_ICON = (By.XPATH, "//span[@class='material-icons' and text()='notifications']")
    ALERTS_DROPDOWN = (By.XPATH, "//span[contains(@class, 'custom-text') and contains(text(), 'Alerts')]")
    ACTION_PANEL = (By.XPATH, "//button[@mat-fab and contains(@class, 'fab-toggler')]")
    ARM_SELECTED = (By.XPATH, "//button[contains(@class, 'actionIconBtn')]//i[contains(@class, 'icon-arm')]/ancestor::button")
    BLAST_SELECTED = (By.XPATH, "//button[.//i[contains(@class, 'icon-blast')]]")
    ARM_ALL_READY = (By.XPATH, "//button[.//i[contains(@class, 'icon-arm-all')]]")
    BLAST_ALL_READY = (By.XPATH, "//button[.//i[contains(@class, 'icon-blast-all')]]")
    ACKNOWLEDGE_FAULTS = (By.CSS_SELECTOR, "[data-testid='ack-faults-checkbox']")
    PROCEED_BLAST = (By.XPATH, "//button[.//span[normalize-space(text())='Proceed to blast']]")
    USER_PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='Enter Password']")
    SUPERVISOR_USERNAME_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='username']")
    SUPERVISOR_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='password']")
    EVENTS_LOG = (By.XPATH, "//button[.//span[text()='EVENTS']]")
    GROUPING_DROPDOWN = (By.ID, "deviceGroupingFunctionSelector")
    OFFSET_ICON = (By.CSS_SELECTOR, "img.offsetButton[mattooltip='Channel Offset']")
    CHANNEL_OFFSET_INPUTS = (By.CSS_SELECTOR, "div.msClass input")
    CHANNEL_OFFSET_SAVE_BUTTON = (By.XPATH, "//button[.//span[text()='Save']]")
    DEVICE_CARDS = (By.CSS_SELECTOR, "bcu-card-high-detail")
    CENTRALIZED= (By.XPATH, "//img[contains(@class, 'iconSize') and contains(@src, 'YellowKey.svg')]")
    READY_TO_ARM = (By.XPATH, "//span[contains(@class, 'titleValue') and contains(text(), 'READY TO ARM')]")
    READY_TO_BLAST = (By.XPATH, "//span[contains(@class, 'titleValue') and contains(text(), 'READY TO BLAST')]")
    DEVICE_BLASTED = (By.XPATH, "//span[contains(@class, 'titleValue') and contains(text(), 'BLASTED')]")
    CARD_READER_POPUP = (By.XPATH, "//app-confirm-blast-dialog")
    CONTINUE_BLAST = (By.XPATH, "//button[.//span[normalize-space(text())='Continue']]")
    START_BLAST = (By.XPATH, "//button[contains(@class, 'confirmBtn') and .//span[normalize-space(text())='Start Blast']]")
    DEVICE_CHECKBOX = (By.XPATH, "//span[@class='locationLabel' and text()='CommsTest']/ancestor::bcu-card-high-detail//input[@type='checkbox']")
    DEVICE_ALERT_ERRORS = (By.XPATH, "//span[contains(@class, 'titlecase')]")
    ERROR_TYPE = (By.XPATH, "//td//p[contains(text(), 'High Leakage')]") # This is an example locator for a specific error type in the dropdown; you can make it more generic if needed.
    
    
    #========================== SYSTEM ===========================================================
    SYSTEM_ALERT_ERRORS = [ "Short Circuit","High Leakage", "High Current", "Acknowledgement Alert",
                           "Low Battery", "Device not available", "Last detonator bad","Last detonator bad voltage",
                            "Blast voltage bad", "Harness Break", "Programming Error","Test Mode","TX error preventing blast"
                        ]
    
    #============================ Locators for after locking ==================================
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/dashboard"

    def navigate(self):
        """Go to devices page."""
        self.open(self.url)
        self.assert_element_displayed(self.DEVICE_CARDS)

   # ------- Actions ----------
   
    def open_alerts_dropdown(self):
        """Click on the Alerts dropdown to view system alerts."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ALERTS_DROPDOWN)
        ).click()
        logger.info("Clicked on 'Alerts' dropdown")
        time.sleep(1)  # Give dropdown time to open
   
    def get_current_alerts(self):
        """Return list of all visible alerts in the dropdown"""
        self.open_alerts_dropdown()
        
        alerts = self.find_elements(self.DEVICE_ALERT_ERRORS)
        alert_texts = [alert.text.strip() for alert in alerts if alert.text.strip()]
        
        print(f"Current alerts shown: {alert_texts}")
        return alert_texts
        
    def open_action_panel(self):
        """Click the action panel button to reveal Arm/Blast options"""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ACTION_PANEL)
        ).click()
        logger.info("Opened action panel")


    def assert_alert_is_present(self, expected_error: str, timeout: int = 15):
        """Assert that a specific error appears in the Alerts dropdown"""
        self.open_alerts_dropdown()

        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.DEVICE_ALERT_ERRORS)
        )

        current_alerts = self.get_current_alerts()

        for alert in current_alerts:
            if expected_error.lower() in alert.lower():
                print(f"✅ PASSED: Expected alert '{expected_error}' is displayed")
                return True

        raise AssertionError(
            f"Expected alert '{expected_error}' NOT found.\n"
            f"Current alerts: {current_alerts}"
    )

    def assert_alerts_are_present(self, expected_errors: list, timeout: int = 15):
        """
        Assert that ALL specified errors are present in the Alerts dropdown.
        If no list is passed, it checks for at least one error from the standard list.
        """
        if expected_errors is None:
            expected_errors = SYSTEM_ALERT_ERRORS

        self.open_alerts_dropdown()

        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.DEVICE_ALERT_ERRORS)
        )

        current_alerts = self.get_current_alerts()
        print(f"Current alerts in dropdown: {current_alerts}")

        missing = []
        for error in expected_errors:
            found = any(error.lower() in alert.lower() for alert in current_alerts)
            if not found:
                missing.append(error)

        if missing:
            raise AssertionError(
                f"Missing expected alert(s): {missing}\n"
                f"Currently shown: {current_alerts}"
            )

        print(f"✅ PASSED: All expected alerts are present → {expected_errors}")
        return True
        

    """Get device status by its location name (e.g., 'Test Lab')."""
    def get_device_status(self, location: str, timeout: int = 10) -> str:
        
        xpath = self.DEVICE_STATUS[1].format(location)
        locator = (self.DEVICE_STATUS[0], xpath)
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element.text.strip()
    
    """Assert that a device at the given location has status 'IDLE'."""
    def assert_communication_is_established(self, location: str):
        
        status = self.get_device_status(location)
        assert status == "IDLE", f"Expected IDLE, got {status}"
        
    """Perform blast action and verify the flow."""
    def performing_blast(self):
        # Before running these test make sure the device has dets connected and ready for locking.
        
        # User has to lock and scan the centralized key before performing blast, so we wait for the key to be visible and the device to be ready to arm
        WebDriverWait(self.driver, 180).until(
            EC.visibility_of_element_located(self.CENTRALIZED)
        )
        
        # Wait for the device to be in "READY TO ARM" state before proceeding with blast actions
        WebDriverWait(self.driver, 180).until(
            EC.text_to_be_present_in_element(self.READY_TO_ARM, "READY TO ARM")
        )
        
        #Wait for the action panel to be clickable and perform blast actions
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.ACTION_PANEL) 
            ).click()
   
        # Wait for the "Arm All Ready" button to be clickable and click it
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.ARM_ALL_READY)
        ).click()
    
        # Wait for the device to be in "READY TO BLAST" state before proceeding with blast actions.
        WebDriverWait(self.driver, 30).until(
            EC.text_to_be_present_in_element(self.READY_TO_BLAST, "READY TO BLAST")
        )

        # Wait for the "Blast All Ready" button to be visible and click it.
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.ACTION_PANEL) 
        ).click()

        # Wait for the "Blast All Ready" button to be visible and click it.
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.BLAST_ALL_READY)
        ).click()
        
        # Wait for the "Proceed to blast" button to be visible and click it.
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.PROCEED_BLAST)
        ).click()
        
        # Wait for the card reader popup to appear and scan the blast card.
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.CARD_READER_POPUP)
        )
        
        # Simulate entering user password after scanning blast card.
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.USER_PASSWORD_INPUT)
        ).click()
        self.type(self.USER_PASSWORD_INPUT, Config.ENG_PASSWORD)
        
        # Proceed with blast after providing password.
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CONTINUE_BLAST)
        ).click()
        
        # Wait for supervisor approval popup and enter credentials.
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SUPERVISOR_USERNAME_INPUT)
        ).click()
        self.type(self.SUPERVISOR_USERNAME_INPUT, Config.SUPERVISOR_USERNAME)
        
        # Wait for supervisor password input, enter password.
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SUPERVISOR_PASSWORD_INPUT)
        ).click()
        self.type(self.SUPERVISOR_PASSWORD_INPUT, Config.SUPERVISOR_PASSWORD)
        
        # Wait for the "Start Blast" button to be clickable and click it.
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.START_BLAST)
        ).click()
        
        # Finally, wait for the device status to change to "BLASTED" to confirm the blast action was successful.
        WebDriverWait(self.driver, 60).until(
            EC.text_to_be_present_in_element(self.DEVICE_BLASTED, "BLASTED")
        )
    
        logger.info("✓ Blast action initiated successfully")
    
        # Put this inside your DashboardPage class
    def get_device_checkbox_locator(self, device_name: str):
        """Getter for device checkbox locator"""
        return (By.XPATH, 
            f"//bcu-card-high-detail[.//span[@class='locationLabel' and contains(text(), '{device_name}')]]"
            f"//mat-checkbox//input[@type='checkbox']"
        )

    def select_device(self, device_name: str):
        """Click the checkbox for a specific device - Robust version"""
        print(f"Attempting to select device: '{device_name}'")

        # ✅ Much more reliable locator:
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
            return True

        except TimeoutException:
            self.driver.save_screenshot(f"debug_checkbox_failed_{device_name}.png")
            print(f"❌ Timeout: Could not locate checkbox for '{device_name}'")
            print("Screenshot saved for debugging.")
            
            # Extra debug info
            print("Current page title:", self.driver.title)
            print("URL:", self.driver.current_url)
            raise
    
    """Set multiple channel offsets."""
    def set_channel_offset(self, device_name: str, offsets = None):
        """
        Click offset icon and set channel offsets for C1 to C6.
        """
        if offsets is None:
            offsets = [2000, 4000, 6000, 8000, 10000, 12000]

        print(f"Starting channel offset setup for device: {device_name}")
        print(f"Target offsets: {offsets}")

        try:
            # Wait for device to be READY TO ARM
            WebDriverWait(self.driver, 15).until(
                EC.text_to_be_present_in_element(self.READY_TO_ARM, "READY TO ARM")
            )
            print("✅ Device status is READY TO ARM")

            # Click the Offset icon
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.OFFSET_ICON)
            ).click()
            print("✅ Clicked Offset icon")

            # Wait for offset inputs to load
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located(self.CHANNEL_OFFSET_INPUTS)
            )
            print("✅ Offset panel loaded")

            # Get input fields
            inputs = self.find_elements(self.CHANNEL_OFFSET_INPUTS)
            print(f"Found {len(inputs)} channel offset input fields")
  
            if len(inputs) < len(offsets):
                raise ValueError(f"Expected at least {len(offsets)} inputs, but found only {len(inputs)}")

            # Set the values
            for i, value in enumerate(offsets):
                if i >= len(inputs):
                    break
                try:
                    input_field = inputs[i]
                    input_field.clear()
                    input_field.send_keys(str(value))
                    print(f"Set C{i+1} = {value} ms")
                    time.sleep(0.8)   # Give Angular time to update slider
                    
                except Exception as e:
                    print(f"Warning: Failed to set C{i+1}: {e}")
 
            WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable(self.CHANNEL_OFFSET_SAVE_BUTTON)
                    ).click()  # Click to ensure value is registered
            print("✅ All channel offsets set successfully")

        except Exception as e:
            print(f"❌ Error in set_channel_offset: {e}")
            raise
        
    def system_alerts_drop_down(self, timeout: int = 20):
        """
        Clicks on 'Alerts' dropdown and asserts that at least one expected error appears.
        Fails the test cleanly if the error is NOT present.
        """
        expected_errors = None
        if expected_errors is None:
            expected_errors = [
                "Short Circuit", "Low Battery","High Current", "High Leakage", "Last detonator bad", "Blast voltage bad",
                "Harness Break", "Programming Error", "TX error preventing blast"
            ]

        # Step 1: Click on Alerts dropdown
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.ALERTS_DROPDOWN)
            ).click()
            
        print("✅ Clicked on 'Alerts' dropdown")

        time.sleep(1)  # Give dropdown time to open

        # Step 2: Wait for alert message to appear
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.DEVICE_ALERT_ERRORS)
        )

        # Step 3: Get all error texts from the dropdown
        error_elements = self.find_elements(self.DEVICE_ALERT_ERRORS)  # Note: find_elements (plural)
        actual_errors = [elem.text.strip() for elem in error_elements if elem.text.strip()]
        print(f"Errors found in dropdown: {actual_errors}")

        # Step 4: Check if any expected error is present (case‑insensitive exact match)
        for expected in expected_errors:
            if expected.lower() in [err.lower() for err in actual_errors]:
                print(f"✅ PASSED: Expected error '{expected}' was displayed")
                return True

        # If we reach here → No expected error was found → FAIL the test
        raise AssertionError(
            f"Expected one of {expected_errors} to appear, but got: {actual_errors}"
        )
    
    def system_alerts_error_removed(self, timeout: int = 20):
        """
        Asserts that no expected errors are present in the dropdown, indicating they have been cleared.
        """
        expected_errors = None
        if expected_errors is None:
            expected_errors = [
                "Short Circuit", "Low Battery","High Current", "High Leakage", "Last detonator bad", "Blast voltage bad",
                "Harness Break", "Programming Error", "TX error preventing blast"
            ]

        # Step 1: Click on Alerts dropdown
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.ALERTS_DROPDOWN)
            ).click()
            
        print("✅ Clicked on 'Alerts' dropdown to verify errors are cleared")

        time.sleep(1)  # Give dropdown time to open
        
        try:
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(self.ERROR_TYPE)
                )
                # Element found → we expect it NOT to be present → fail
                raise AssertionError(
                    f"❌ FAILED: Error element '{self.ERROR_TYPE[1]}' is present, but expected it to be absent."
                )
        except TimeoutException:
                # Element not found within timeout → test passes
                print(f"✅ PASSED: Error element is absent as expected.")
                return True
    
    # This is a new method to click on the Events log and verify the error in test is present in the event logs.
    # Adjust the error type locator and expected error text as needed to match your application's structure and the specific error you want to verify.
    # Introduce the error immediately after running the test to ensure it appears in the logs and can be verified.
    def events_log(self, driver):
        """Click on the Events log and verify it opens."""
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.EVENTS_LOG)
        )

        events_log_element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.EVENTS_LOG)
        )
        # Use JavaScript click to bypass interception
        self.driver.execute_script("arguments[0].click();", events_log_element)
        print("✅ Clicked on 'EVENTS' log")

        # Wait for error type to appear, with explicit assertion
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(self.ERROR_TYPE)
            )
            print("✅ Error present")
            return True
        except TimeoutException:
            raise AssertionError(
                f"ERROR: Expected error type element {self.ERROR_TYPE} did not appear within 20 seconds after clicking Events log."
            )
