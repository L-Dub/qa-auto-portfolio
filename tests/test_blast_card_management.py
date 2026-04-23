import time

import pytest
from pages.blast_card_page import BlastCardPage
from pages.login_page import LoginPage
from utils.logger import logger


class TestBlastCardsManagement:

    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url, admin_credentials):
        """Login and navigate to Blast Cards page before each test"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(admin_credentials["username"], admin_credentials["password"])
        login_page.assert_login_successful()

        self.blast_card_page = BlastCardPage(driver)
        self.blast_card_page.navigate()
    
    def test_view_devices(self, driver):
        """View Cards"""
        self.blast_card_page.assert_blast_cards_page_loaded()
    
    def test_add_blast_card(self):
        """Test Case: Add a new Blast Card"""
        self.blast_card_page.add_blast_card()
        logger.info("✓ Blast Card added successfully")
        self.blast_card_page.assert_card_is_added()
        
    def test_archive_active_card_icon(self):
        """Test Case: Archive an active Blast Card"""
        self.blast_card_page.search_card("Blast")
        self.blast_card_page.archive_cards_using_icon()
        
    def test_activate_archived_card_icon(self):
        """Test Case: Activate an archived Blast Card"""
        self.blast_card_page.activate_cards_using_icon()

    def test_search_bar_in_blast_card(self):
        """Test Case: Verify search functionality in Blast Cards"""
        #self.blast_card_page.ensure_blast_card_exists()
        self.blast_card_page.search_card("Activate")
        
        # Verify search input value
        search_input = self.blast_card_page.find_element(self.blast_card_page.SEARCH_BAR)
        assert search_input.get_attribute("value") == "Activate", "Search input value mismatch"
        logger.info("✓ Search functionality verified")

    def test_delete_card_using_icon(self):
        self.blast_card_page.add_blast_card()  # Ensure there's a card to delete
        self.blast_card_page.search_card("Activate")
        self.blast_card_page.delete_card_using_icon()
        logger.info("✓ Blast Card deleted successfully")

    def test_delete_card_using_btn(self):
        self.blast_card_page.add_blast_card()  # Ensure there's a card to delete
        self.blast_card_page.search_card("Activate")
        self.blast_card_page.delete_card_using_btn()
        logger.info("✓ Blast Card deleted successfully")
        

        
        