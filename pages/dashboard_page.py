from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import logger

class DashboardPage(BasePage):
    # Locators (as tuples)
    DEVICE_CHECKBOX = (By.XPATH, "//span[@class='locationLabel' and text()='Chromium mine']/ancestor::bcu-card-high-detail//input[@type='checkbox']")
    DEVICE_STATUS = (By.XPATH, "//span[@class='locationLabel' and text()='{}']/ancestor::bcu-title//span[@class='titleValue']")
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

   # ------- Actions ----------

    def enter_password(self, password):
        """Enter password when prompted during blast."""
        self.type(self.USER_PASSWORD_INPUT, password)

    def set_channel_offset(self, seconds_list):
        """Set multiple channel offsets."""
        self.click(self.OFFSET_ICON)
        inputs = self.find_elements(self.CHANNEL_OFFSET_INPUTS)
        if len(inputs) != len(seconds_list):
            raise ValueError(f"Expected {len(seconds_list)} offset inputs, got {len(inputs)}")
        for i, value in enumerate(seconds_list):
            inputs[i].clear()
            inputs[i].send_keys(str(value))
        self.click(self.CHANNEL_OFFSET_SAVE_BUTTON)