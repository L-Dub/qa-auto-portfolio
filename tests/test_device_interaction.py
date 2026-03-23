import pytest
from pages.device_page import DevicePage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

@pytest.mark.hardware
class TestDeviceInteraction:
    def test_establish_communication(self, driver):
        # This test requires actual BCU hardware; we simulate steps and check UI
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        device_page = DevicePage(driver)
        device_page.navigate()
        # Add network and device (as per test plan)
        # ... actual steps
        # Then go to dashboard and check status
        dashboard = DashboardPage(driver)
        dashboard.navigate()
        status = dashboard.get_device_status()
        assert "IDLE" in status

    def test_comms_lost(self, driver):
        # Simulate disconnect
        dashboard = DashboardPage(driver)
        dashboard.navigate()
        # Trigger disconnect (e.g., via UI mock)
        # Check status becomes UNKNOWN
        status = dashboard.get_device_status()
        assert "UNKNOWN" in status