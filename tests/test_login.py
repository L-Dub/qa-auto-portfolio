import pytest
from pages.login_page import LoginPage
from config import Config
from selenium.webdriver.support import expected_conditions as EC


class TestLogin:
    @pytest.mark.parametrize("username,password,expected", [
        (Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD, "dashboard"),
        ("invalid", "invalid", "Unauthorized - Token invalid , user unauthorized!")
    ])
    def test_login_scenarios(self, driver, base_url, username, password, expected):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(username, password)

        if expected == "dashboard":
            login_page.wait_for_logged_in()
        else:
            login_page.wait_for_error_message(expected)

        # No extra assertion – the wait already confirms the outcome

    def test_logout(self, driver, base_url, admin_credentials):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(admin_credentials["username"], admin_credentials["password"])
        login_page.wait_for_logged_in()
        login_page.logout()

        # Wait for the login page URL and verify login button is displayed
        login_page.wait.until(lambda d: "/en/login" in d.current_url)
        login_page.assert_element_displayed(login_page.LOGIN_BUTTON)

    def test_password_visibility(self, driver, base_url):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.wait.until(EC.element_to_be_clickable(login_page.PASSWORD_INPUT))

        login_page.type(login_page.PASSWORD_INPUT, "secret")
        assert login_page.get_password_field_type() == "password"

        login_page.reveal_password()
        assert login_page.get_password_field_type() == "text"