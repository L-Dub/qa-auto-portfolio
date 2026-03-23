"""
Test suite for Email Recipients (section 12 of test plan).
"""

import pytest
from pages.login_page import LoginPage
from pages.recipient_page import RecipientPage
import time


class TestRecipients:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        login_page.assert_login_successful()
        self.recipient_page = RecipientPage(driver)
        self.recipient_page.navigate()

    def test_view_recipients(self, driver):
        """Test Case: View Email Recipients"""
        self.recipient_page.assert_element_displayed(self.recipient_page.RECIPIENT_TABLE)

    def test_add_recipient(self, driver):
        """Test Case: Add Recipient"""
        ts = int(time.time())
        username = f"rec_{ts}"
        self.recipient_page.add_recipient(
            username=username,
            first="Test",
            last="Recipient",
            email=f"{username}@example.com"
        )
        self.recipient_page.assert_recipient_in_list(username)

    def test_delete_recipient(self, driver):
        """Test Case: Delete Recipient"""
        ts = int(time.time())
        username = f"delrec_{ts}"
        self.recipient_page.add_recipient(username, "Del", "Rec", f"{username}@example.com")
        self.recipient_page.assert_recipient_in_list(username)
        self.recipient_page.search_recipient(username)
        self.recipient_page.delete_first_recipient()
        self.recipient_page.assert_recipient_not_in_list(username)