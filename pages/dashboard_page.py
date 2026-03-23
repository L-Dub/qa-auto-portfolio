"""
Page Object for the Dashboard.
Handles device selection, arming, blasting, alerts, grouping, and event log.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver import driver
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """
    Main dashboard after login.
    """

    # Locators
    DEVICE_CHECKBOX = driver.find_element(
    By.XPATH,
    "//span[@class='locationLabel' and text()='Chromium mine']/ancestor::bcu-card-high-detail//input[@type='checkbox']"
    )  # Checkbox for device name 'Chromium mine' (adjust as needed)
    DEVICE_STATUS = "//span[@class='locationLabel' and text()='{}']/ancestor::bcu-title//span[@class='titleValue']"
    ALERT_ICON = (By.XPATH, "//span[@class='material-icons' and text()='notifications']")
    ALERTS_DROPDOWN = (By.XPATH, "//span[@class='material-icons' and contains(text(),'arrow_drop_down')]")
    ACTION_PANEL = (By.XPATH, "//span[@class='mat-ripple mat-mdc-button-ripple']")
    ARM_SELECTED = (By.CSS_SELECTOR, "button.actionIconBtn.mat-accent")
    BLAST_SELECTED = (By.XPATH, "//button[.//i[contains(@class, 'icon-blast')]]")
    ARM_ALL_READY = (By.XPATH, "//button[.//i[contains(@class, 'icon-arm-all')]]")
    BLAST_ALL_READY = (By.XPATH, "//button[.//i[contains(@class, 'icon-blast')]]")
    ACKNOWLEDGE_FAULTS = (By.CSS_SELECTOR, "[data-testid='ack-faults-checkbox']")
    PROCEED_BLAST = (By.XPATH, "//button[.//span[contains(text(), 'Proceed to blast')]]")
    USER_PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='Enter Password']")
    SUPERVISOR_USERNAME_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='username']")
    SUPERVISOR_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='password']")
    EVENTS_LOG = (By.XPATH, "//button[.//span[text()='EVENTS']]")
    GROUPING_DROPDOWN = (By.ID, "deviceGroupingFunctionSelector")
    OFFSET_ICON = (By.CSS_SELECTOR, ".offsetButton")
    CHANNEL_OFFSET_INPUTS = (By.CSS_SELECTOR, "div.msClass input")
    CHANNEL_OFFSET_SAVE_BUTTON = (By.XPATH, "//button[.//span[text()='Save']]")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/dashboard"

    def navigate(self):
        """Go to dashboard."""
        self.open(self.url)
        # Wait for some dashboard element to confirm load
        self.assert_element_displayed(self.ACTION_PANEL)

    # ---------- Device Selection ----------
    def select_first_device(self):
        """Select the checkbox of the first device."""
        checkbox = self.find_element(self.DEVICE_CHECKBOX)
        checkbox.click()
        return checkbox.is_selected()

    def select_all_devices(self):
        """Select all device checkboxes (if 'Select All' exists, use that; else iterate)."""
        # Prefer a 'Select All' checkbox if present
        try:
            select_all = self.find_element((By.ID, "select-all"))
            select_all.click()
        except:
            # Fallback: click each checkbox
            checkboxes = self.find_elements(self.DEVICE_CHECKBOX)
            for cb in checkboxes:
                if not cb.is_selected():
                    cb.click()

    # ---------- Status ----------
    def get_device_status(self):
        """Return the status text of the first device (e.g., IDLE, READY TO ARM)."""
        return self.get_text(self.DEVICE_STATUS)

    # ---------- Action Panel ----------
    def open_action_panel(self):
        """Open the action panel (if it's collapsible)."""
        self.click(self.ACTION_PANEL)

    def click_arm_selected(self):
        """Click 'Arm Selected' button."""
        self.click(self.ARM_SELECTED)

    def click_blast_selected(self):
        """Click 'Blast Selected' button."""
        self.click(self.BLAST_SELECTED)

    def click_arm_all_ready(self):
        """Click 'Arm All Ready' button."""
        self.click(self.ARM_ALL_READY)

    def click_blast_all_ready(self):
        """Click 'Blast All Ready' button."""
        self.click(self.BLAST_ALL_READY)

    def acknowledge_faults(self):
        """Check the acknowledge faults checkbox."""
        self.click(self.ACKNOWLEDGE_FAULTS)

    def proceed_to_blast(self):
        """Click the 'Proceed to Blast' button."""
        self.click(self.PROCEED_BLAST)

    def enter_password(self, password):
        """Enter password when prompted during blast."""
        self.type(self.PASSWORD_INPUT, password)
        
    def enter_supervisor_credentials(self, username, password):
        """Enter supervisor credentials when prompted."""
        self.type(self.SUPERVISOR_USERNAME_INPUT, username)
        self.type(self.SUPERVISOR_PASSWORD_INPUT, password)

    # ---------- Alerts ----------
    def get_alerts(self):
        """Open the alerts dropdown and return the list of alert items."""
        self.click(self.ALERTS_DROPDOWN)
        return self.find_elements((By.CSS_SELECTOR, ".alert-item"))

    # ---------- Channel Offset ----------
    def set_channel_offsets(self, seconds_list):
        """
        Set channel offsets for all six channels.
        :param milli_seconds_list: list of six integers/strings, e.g. [3000, 6000, 9000, 12000, 15000, 20000]
        """
        # Click the offset icon to open the panel
        self.click(self.OFFSET_ICON)
    
        # Find all six offset input fields (order matches channels C1–C6)
        inputs = self.driver.find_elements(*CHANNEL_OFFSET_INPUTS)
    
        # Ensure we have exactly six inputs
        if len(inputs) != 6:
            raise ValueError(f"Expected 6 offset inputs, found {len(inputs)}")
    
        # Set each input
        for i, value in enumerate(seconds_list):
            inputs[i].clear()
            inputs[i].send_keys(str(value))
    
        # Click save
        self.click(self.SAVE_BUTTON)
        
    # ---------- Grouping ----------
    def select_grouping(self, group_name):
        """Select a grouping option from the dropdown."""
        self.select_dropdown(self.GROUPING_DROPDOWN, group_name)

    # ---------- Events Log ----------
    def get_event_log_entries(self):
        """Return the list of event log entries."""
        return self.find_elements((By.CSS_SELECTOR, "#events-log .event-entry"))

    # ---------- Assertions ----------
    def assert_device_status(self, expected_status):
        """Assert that the first device's status matches expected."""
        actual = self.get_device_status()
        assert actual == expected_status, f"Device status expected '{expected_status}', got '{actual}'"
        logger.info(f"Device status correctly '{expected_status}'")

    def assert_alert_present(self, alert_type):
        """Assert that a specific alert type (e.g., 'Short Circuit') appears in alerts dropdown."""
        alerts = self.get_alerts()
        alert_texts = [alert.text for alert in alerts]
        assert any(alert_type in text for text in alert_texts), f"Alert '{alert_type}' not found"
        logger.info(f"Alert '{alert_type}' present")