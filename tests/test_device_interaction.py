import random

import pytest
from pages.device_page import DevicePage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


# @pytest.mark.hardware
class TestDeviceInteraction:
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url, eng_credentials):
        """Login and navigate to Blast Cards page before each test"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(eng_credentials["username"], eng_credentials["password"])
        login_page.assert_login_successful()
        self.dashboard_page = DashboardPage(driver)
        self.dashboard_page.navigate()
        
    def test_view_devices(self, driver):
        self.device_page = DevicePage(driver)
        # Verify device card is displayed
        self.dashboard_page.assert_element_displayed(self.dashboard_page.DEVICE_CARDS)

    """
    def test_establish_communication(self, driver):
        self.device_page = DevicePage(driver)
        device_id = "404"  #Fix ID for consistent testing; can be randomized if needed
        ip = "172.20.10.48"
        device_name = "CommsTest"
        self.device_page.navigate()
        self.device_page.add_device(device_id, ip, device_name)
        self.dashboard_page.navigate()  # Refresh dashboard to see the new device
        self.dashboard_page.assert_communication_is_established(device_name)
        self.device_page.navigate()  # Ensure we're on the device page to delete
        self.device_page.delete_device(device_id)  # Clean up after test
   
    def test_perform_blast(self, driver):
        self.device_page = DevicePage(driver)
        device_id = "404"  #Fix ID for consistent testing; can be randomized if needed
        ip = "172.20.10.48"
        device_name = "CommsTest"
        self.device_page.navigate()
        self.device_page.add_device(device_id, ip, device_name)
        self.dashboard_page.navigate()  # Refresh dashboard to see the new device
        self.dashboard_page.performing_blast()
        self.device_page.navigate()  # Ensure we're on the device page to delete
        self.device_page.delete_device(device_id)  # Clean up after test
    
    def test_set_channel_offset(self, driver):
        self.device_page = DevicePage(driver)
        device_id = "404"  #Fix ID for consistent testing; can be randomized if needed
        ip = "172.20.10.48"
        device_name = "CommsTest"
        self.device_page.navigate()
        self.device_page.add_device(device_id, ip, device_name)
        self.dashboard_page.navigate()  # Refresh dashboard to see the new device
        self.dashboard_page.set_channel_offset(device_name)
        # self.dashboard_page.performing_blast()  # Verify blast still works after setting offset
        self.device_page.navigate()  # Ensure we're on the device page to delete
        self.device_page.delete_device(device_id)  # Clean up after test
    
    """
    def test_select_device(self, driver):
        self.device_page = DevicePage(driver)
        device_id = "404"  #Fix ID for consistent testing; can be randomized if needed
        ip = "172.20.10.48"
        device_name = "CommsTest"
        self.device_page.navigate()
        self.device_page.add_device(device_id, ip, device_name)
        self.dashboard_page.navigate()  # Refresh dashboard to see the new device
        self.dashboard_page.select_device(device_id)
        #assert self.dashboard_page.select_device(device_name) is True

        