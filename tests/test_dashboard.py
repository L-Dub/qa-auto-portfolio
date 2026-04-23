import pytest
from time import sleep
from pages.dashboard_page import DashboardPage
from pages.device_page import DevicePage
from pages.login_page import LoginPage

class TestDashboard:
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url, eng_credentials):
        """Login and navigate to Blast Cards page before each test"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(eng_credentials["username"], eng_credentials["password"])
        login_page.assert_login_successful()
        self.dashboard_page = DashboardPage(driver)
        self.dashboard_page.navigate()
    
    def test_system_alert(self, driver):
        dashboard = DashboardPage(driver)
        dashboard.navigate()
        self.device_page = DevicePage(driver)
        device_id = "404"  #Fix ID for consistent testing; can be randomized if needed
        ip = "172.20.10.48"
        device_name = "CommsTest"
        self.device_page.navigate()
        self.device_page.add_device(device_id, ip, device_name)
        dashboard.navigate()  # Refresh dashboard to see the new device
        sleep(5)  # Wait for the error to get triggered on the BCU
        dashboard.system_alerts_drop_down()
        dashboard.events_log(self)
        sleep(30) #Wait for the user to clear the error.
        dashboard.system_alerts_error_removed()
        #dashboard.system_alerts(expect_present=False)  # Verify error is cleared after viewing logs
'''
    def test_device_selection(self, driver):
        dashboard = DashboardPage(driver)
        dashboard.navigate()
        self.device_page = DevicePage(driver)
        device_id = "404"  #Fix ID for consistent testing; can be randomized if needed
        ip = "172.20.10.48"
        device_name = "CommsTest"
        self.device_page.navigate()
        self.device_page.add_device(device_id, ip, device_name)
        self.dashboard_page.navigate()  # Refresh dashboard to see the new device
        assert dashboard.select_device(device_name) is True
        
    def test_arm_selected(self, driver, base_url, admin_credentials):
        dashboard = DashboardPage(driver)
        dashboard.navigate()
        self.device_page = DevicePage(driver)
        device_id = "404"  #Fix ID for consistent testing; can be randomized if needed
        ip = "172.20.10.48"
        device_name = "CommsTest"
        self.device_page.navigate()
        self.device_page.add_device(device_id, ip, device_name)
        dashboard.select_device(device_name)
        dashboard.open_action_panel()
        assert dashboard.is_displayed(dashboard.ARM_SELECTED)

    def test_alerts_display(self, driver):
        self.device_page = DevicePage(driver)
        device_id = "404"  #Fix ID for consistent testing; can be randomized if needed
        ip = "172.20.10.48"
        device_name = "CommsTest"
        self.device_page.navigate()
        self.device_page.add_device(device_id, ip, device_name)
        self.dashboard_page.navigate()  # Refresh dashboard to see the new device
        self.dashboard_page.drop_down_errors()
        self.device_page.navigate()  # Ensure we're on the device page to delete
        self.device_page.delete_device(device_id)  # Clean up after test
'''