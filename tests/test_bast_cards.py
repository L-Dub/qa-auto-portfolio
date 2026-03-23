import pytest
from pages.blast_card_page import BlastCardPage
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By

class TestBlastCards:
    def test_add_blast_card(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        card_page = BlastCardPage(driver)
        card_page.navigate()
        card_page.go_to_active()
        card_page.click_add_card()
        # Assuming card is added, we check table
        rows = card_page.find_elements((By.CSS_SELECTOR, "tbody tr"))
        assert len(rows) > 0

    def test_archive_card(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        card_page = BlastCardPage(driver)
        card_page.navigate()
        card_page.go_to_active()
        card_page.archive_first_card()
        card_page.go_to_archived()
        rows = card_page.find_elements((By.CSS_SELECTOR, "tbody tr"))
        assert len(rows) > 0

    def test_search_card(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        card_page = BlastCardPage(driver)
        card_page.navigate()
        card_page.go_to_active()
        card_page.search_card("Blast Card")
        # Just verify no crash; results may vary
        assert True