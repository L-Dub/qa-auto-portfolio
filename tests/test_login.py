import pytest
from pages.login_page import LoginPage
from config import Config

class TestLogin:
    @pytest.mark.parametrize("username,password,expected", [
        (Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD, "dashboard"),
        ("invalid", "invalid", "Your username is invalid!")
    ])
    def test_login_scenarios(self, driver, base_url, expected):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        assert expected in driver.page_source.lower()

    def test_logout(self, driver, base_url, admin_credentials):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        login_page.open_settings()
        login_page.logout()
        assert "Login Page" in driver.title

    def test_password_visibility(self, driver, base_url):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.type(login_page.PASSWORD_INPUT, "secret")
        assert login_page.get_password_field_type() == "password"
        login_page.reveal_password()
        assert login_page.get_password_field_type() == "text"