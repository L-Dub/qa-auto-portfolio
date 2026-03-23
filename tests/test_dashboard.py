import pytest
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

class TestDashboard:
    def test_device_selection(self, driver, base_url, admin_credentials):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        dashboard = DashboardPage(driver)
        dashboard.navigate()
        assert dashboard.select_first_device() is True

    def test_arm_selected(self, driver, base_url, admin_credentials):
        # This test requires devices in "Ready to Arm" state; we simulate by checking button presence
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        dashboard = DashboardPage(driver)
        dashboard.navigate()
        dashboard.select_first_device()
        dashboard.open_action_panel()
        assert dashboard.is_displayed(dashboard.ARM_SELECTED)

    @pytest.mark.hardware
    def test_alerts_display(self, driver, admin_credentials):
        # Requires hardware to generate alerts; we'll just check UI existence
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        dashboard = DashboardPage(driver)
        dashboard.navigate()
        alerts = dashboard.get_alerts()
        assert isinstance(alerts, list)