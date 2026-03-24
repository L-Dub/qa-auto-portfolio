import pytest
from pages.user_page import UserPage
from pages.login_page import LoginPage
from tests.conftest import driver
from config import Config


class TestUserManagement:
    def test_view_users(self, driver, base_url, admin_credentials):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        user_page = UserPage(driver)
        user_page.navigate()
        assert user_page.is_displayed(user_page.USER_TABLE)

    def test_add_user(self, driver, base_url, admin_credentials):
        # Implementation depends on actual form; here we just click add and verify navigation
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        user_page = UserPage(driver)
        user_page.navigate()
        user_page.click_add_user()
        user_page.fill_user_form("Tester1", "Tested", "Tester_surname", "tester@example.com")
        assert "add-user" in driver.current_url  # adjust
        
    def test_change_user_password(self, driver, new_password="NewPass123!"):
        # Implementation would depend on the actual UI flow for changing password.
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        user_page = UserPage(driver)
        user_page.navigate()
        user_page.reset_user_password()
        
    def test_edit_user(self, driver, base_url, admin_credentials):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(admin_credentials["username"], admin_credentials["password"])
        user_page = UserPage(driver)
        user_page.navigate()
        user_page.click_edit_user()
        # Fill form with new details (this is just a placeholder, adjust as needed)
        user_page.fill_user_form(username="test1", first_name="tester1", last_name="Tester", email="tester@example.com")

    def test_delete_single_user(self, driver, base_url, admin_credentials):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        user_page = UserPage(driver)
        user_page.navigate()
        initial_count = len(user_page.get_user_rows())
        if initial_count > 1:  # ensure there is a deletable user
            user_page.delete_first_user()
            # Wait for deletion
            import time
            time.sleep(1)
            new_count = len(user_page.get_user_rows())
            assert new_count == initial_count - 1

    def test_search_user(self, driver, base_url, admin_credentials):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        user_page = UserPage(driver)
        user_page.navigate()
        user_page.search_user("admin")
        rows = user_page.get_user_rows()
        assert len(rows) >= 1