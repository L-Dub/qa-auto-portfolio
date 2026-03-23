from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class BlastCardPage(BasePage):
    ACTIVE_CARDS_TAB = (By.XPATH, "//span[text()='Active Cards']")
    ARCHIVED_CARDS_TAB = (By.XPATH, "//span[text()='Archived Cards']")
    ADD_CARD_BUTTON = (By.XPATH, "//button[contains(., 'Add Blast Card')]")
    ARCHIVE_BUTTON = (By.XPATH, "//button[.//span[text()='Archive Cards']]")
    DELETE_BUTTON = (By.XPATH, "//button[.//span[text()='Delete Cards']]")
    ACTIVATE_BUTTON = (By.XPATH, "//button[.//span[text()='Activate Cards']]")
    SEARCH_BAR = (By.XPATH, "//input[@placeholder='Search using Serial Number, Key Type, Updated Date']")
    CARD_TABLE = (By.CSS_SELECTOR, "table.mat-mdc-table")
    CHECKBOX_HEADER = (By.CSS_SELECTOR, "th input[type='checkbox']")
    ARCHIVE_ICON = (By.CSS_SELECTOR, ".archiveIcon")
    DELETE_ICON = (By.XPATH, "//span[@mattooltip='Delete this card']")
    ACTIVATE_ICON = (By.XPATH, "//mat-icon[@mattooltip='Activate this card']")
    CONFIRM_ARCHIVE = (By.XPATH, "//button[.//span[text()='Yes']]")
    CONFIRM_DELETE = (By.XPATH, "//button[.//span[text()='Yes']]")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/settings/activeCards"

    def navigate(self):
        self.open(self.url)

    def go_to_active(self):
        self.click(self.ACTIVE_CARDS_TAB)

    def go_to_archived(self):
        self.click(self.ARCHIVED_CARDS_TAB)

    def click_add_card(self):
        self.click(self.ADD_CARD_BUTTON)
        # Wait for the success snackbar message
        success_locator = (By.XPATH, "//div[contains(@class, 'mat-mdc-snack-bar-label') and contains(text(), 'has been added successfully')]")
        self.wait_for_element(success_locator, timeout=40)  # allow time for NFC read

    def archive_selected_cards(self):
        self.click(self.ARCHIVE_BUTTON)
        self.click(self.CONFIRM_ARCHIVE)

    def delete_selected_cards(self):
        self.click(self.DELETE_BUTTON)
        self.click(self.CONFIRM_DELETE)

    def activate_selected_cards(self):
        self.click(self.ACTIVATE_BUTTON)
        self.click(self.CONFIRM_ARCHIVE)  # Assuming same confirmation

    def archive_first_card(self):
        self.click(self.ARCHIVE_ICON)
        self.click(self.CONFIRM_ARCHIVE)

    def delete_first_card(self):
        self.click(self.DELETE_ICON)
        self.click(self.CONFIRM_DELETE)

    def activate_first_card(self):
        self.click(self.ACTIVATE_ICON)
        self.click(self.CONFIRM_ARCHIVE)

    def search_card(self, keyword):
        self.type(self.SEARCH_BAR, keyword)

    def select_all_cards(self):
        self.click(self.CHECKBOX_HEADER)