"""
Page Object for Blast Cards Management.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import logger


class BlastCardPage(BasePage):
    """
    Represents the Blast Cards management page (Settings → Blast Cards).
    """

    # Locators
    ACTIVE_CARDS_TAB = (By.XPATH, "span[text()='Active Cards']")
    ARCHIVED_CARDS_TAB = (By.XPATH, "//span[text()='Archived Cards']")
    ARCHIVE_BUTTON = (By.XPATH, "//span[text()='Archive Cards']/ancestor::button[1]")
    SEARCH_BAR = (By.XPATH, "//input[contains(@placeholder,'Search')]")
    CARD_TABLE = (By.CSS_SELECTOR, "table.mat-mdc-table")
    ARCHIVE_ICON = (By.CSS_SELECTOR, ".archiveIcon")
    ACTIVATE_ICON = (By.XPATH, "//mat-icon[@mattooltip='Activate this card']")
    CONFIRM_YES_BUTTON = (By.XPATH, "//span[text()='Yes']/ancestor::button[1]")
    SUCCESS_SNACKBAR = (By.CSS_SELECTOR, "div.mat-mdc-snack-bar-label.mdc-snackbar__label")
    NO_BLAST_CARDS_MESSAGE = (By.XPATH, "//h2[contains(text(), 'No Blast Cards Present')]")
    FIRST_CHECKBOX = (By.XPATH, "//tbody/tr[1]//div[@class='mdc-checkbox']")

    # Add Blast Card button
    ADD_BLAST_CARD_BTN = (By.XPATH, "//span[contains(text(),'Add Blast Card')]")
    DELETE_CARD_BTN = (By.XPATH, "//span[contains(., 'Delete Cards')]")
    DELETE_ICON = (By.XPATH, "//span[@mattooltip='Delete this card']")
    

    # No data message
    NO_BLAST_CARDS_MESSAGE = (By.XPATH, "//h2[contains(text(), 'No Blast Cards Present')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/settings/activeCards"

    def navigate(self):
        """Navigate to Blast Cards page and wait for content to load."""
        self.open(self.url)
        self.wait_for_page_content_to_load()

    def wait_for_page_content_to_load(self, timeout: int = 15):
        """
        Wait until either the table is loaded OR the 'No Blast Cards Present' message appears.
        This prevents timeout when the table is empty.
        """
        def page_ready(driver):
            # Check if table exists
            table_exists = len(driver.find_elements(*self.CARD_TABLE)) > 0
            # Check if "No Blast Cards" message exists
            no_data_exists = len(driver.find_elements(*self.NO_BLAST_CARDS_MESSAGE)) > 0
            return table_exists or no_data_exists

        WebDriverWait(self.driver, timeout).until(
            page_ready,
            message="Neither Blast Cards table nor 'No Blast Cards Present' message appeared"
        )
        logger.info("Blast Cards page content loaded successfully")

    def wait_for_table_to_load(self, timeout: int = 15):
        """Wait specifically for the table (use only when you expect data)."""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.CARD_TABLE)
        )

    #===============Actions================
    
    def add_blast_card(self):
        """Add a new Blast Card using the Add button."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ADD_BLAST_CARD_BTN)
        ).click()
        self.wait_for_success_snackbar()

    def archive_cards_using_icon(self):
        """Click Archive Cards button and confirm."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ARCHIVE_ICON)
        ).click()
        self.click(self.CONFIRM_YES_BUTTON)
        self.wait_for_success_snackbar()
        
    def activate_cards_using_icon(self):
        """Click Activate icon and confirm."""
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ARCHIVED_CARDS_TAB)
        ).click()

        self.search_card("Blast")  # Ensure the card is visible before clicking activate
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ACTIVATE_ICON)
        ).click()
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CONFIRM_YES_BUTTON)
        ).click()
        self.wait_for_success_snackbar()

    def search_card(self, keyword: str):
        """Search for a card by keyword (e.g., serial number). Independent method."""
        logger.info(f"Searching for card with keyword: {keyword}")
        self.type(self.SEARCH_BAR, keyword)
        self.wait_for_page_content_to_load(timeout=10)

    def delete_cards_icon(self):
        """Click the bulk 'Delete Cards' button and confirm."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.DELETE_CARD_BTN)
        ).click()
        
        self.click(self.CONFIRM_YES_BUTTON)
        self.wait_for_success_snackbar()
        
    def delete_card_using_icon(self):
        """Delete a card using the delete icon and confirm."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.DELETE_ICON)
        ).click()
        self.click(self.CONFIRM_YES_BUTTON)
        self.wait_for_success_snackbar()
        
    def delete_card_using_btn(self):
        # Wait for the first data row checkbox to be present and clickable
        checkbox = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.FIRST_CHECKBOX)
        )
        checkbox.click()
    
        # Wait for delete button to become enabled and click it
        delete_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.DELETE_CARD_BTN)
    )
        delete_btn.click()
        
        # Confirm deletion
        self.click(self.CONFIRM_YES_BUTTON)
        self.wait_for_success_snackbar()

    def go_to_active(self):
        """Switch to Active Cards tab."""
        self.click(self.ACTIVE_CARDS_TAB)
        self.wait_for_page_content_to_load()

    def ensure_blast_card_exists(self):
        """Ensure at least one Blast Card exists. If not, add one."""
        try:
            # Try to find the table header
            WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'mat-sort-header-content') and contains(text(),'Serial Number')]"))
            )
            logger.info("Blast Card already exists")
        except Exception:
            logger.info("No Blast Card found. Adding a new one...")
            self.click(self.ADD_BLAST_CARD_BTN)
            
            # Wait for success or table update
            WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'mat-sort-header-content') and contains(text(),'Serial Number')]"))
            )
            logger.info("Blast Card added successfully")

    def select_first_card(self):
        """Select the first card using checkbox."""
        checkboxes = self.find_elements((By.CSS_SELECTOR, "input.mdc-checkbox__native-control"))
        if checkboxes:
            self.driver.execute_script("arguments[0].click();", checkboxes[0])
            logger.info("Selected first Blast Card")
            
    def archive_first_card(self):
        """Archive using the icon on the first card."""
        self.click(self.ARCHIVE_ICON)
        self.click(self.CONFIRM_YES_BUTTON)
        self.wait_for_success_snackbar()
        
    def delete_blast_card(self):
        """Delete a Blast Card using the delete icon and confirm."""
        self.click(self.DELETE_ICON)
        self.click(self.CONFIRM_YES_BUTTON)
        self.wait_for_success_snackbar()

    def wait_for_success_snackbar(self):
        """Wait for success snackbar message."""
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.SUCCESS_SNACKBAR)
        )
        logger.info("Success snackbar appeared")

    def get_table_rows(self):
        """Return all rows in the table."""
        return self.find_elements((By.CSS_SELECTOR, "tbody tr"))

    #===============Assertion Helpers===============

    def assert_blast_cards_page_loaded(self):
        """
        Assert that the Blast Cards page is loaded successfully.
        Accepts either the table OR the 'No Blast Cards Present' message.
        """
        try:
            # Check if table is present
            WebDriverWait(self.driver, 10).until(
                EC.any_of(
                    EC.presence_of_element_located(self.CARD_TABLE),
                    EC.presence_of_element_located(self.NO_BLAST_CARDS_MESSAGE)
                )
            )
            logger.info("✓ Blast Cards page loaded successfully (table or no data message)")
        except Exception:
            raise AssertionError("Blast Cards page failed to load - neither table nor 'No Blast Cards Present' message was found")

    def assert_card_is_added(self):
        """
        Assert that the Blast Card was successfully added.
        """
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.SUCCESS_SNACKBAR)
        )
        snackbar = self.find_element(self.SUCCESS_SNACKBAR)
        assert snackbar.is_displayed(), "Blast Card success snackbar is not visible"
        logger.info("✓ Blast Card added successfully - Success snackbar is visible")

    def assert_card_is_archived(self):
        """
        Assert that the Blast Card was successfully archived.
        """
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.SUCCESS_SNACKBAR)
        )
        snackbar = self.find_element(self.SUCCESS_SNACKBAR)
        assert snackbar.is_displayed(), "Blast Card archive success snackbar is not visible"
        logger.info("✓ Blast Card archived successfully")