import pytest
from pages.device_page import DevicePage
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from config import Config
import random

class TestDeviceManagement:
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url, admin_credentials):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(admin_credentials["username"], admin_credentials["password"])
        login_page.assert_login_successful()
        self.device_page = DevicePage(driver)
        self.device_page.navigate()

    def test_view_devices(self, driver):
        """Test Case: View Devices"""
        # Ensure at least one device is present to view the table.
        self.device_page.assert_element_displayed(self.device_page.DEVICE_TABLE)

    def test_add_device(self, driver):
        """Test Case: Add Device"""
        device_id = str(random.randint(257, 910) + 10)  # Generate a random ID to avoid conflicts
        location = "Test Lab"
        ip = "172.20.10.48"
        self.device_page.add_device(device_id, ip, location)
        self.device_page.assert_device_in_list(device_id)

    def test_edit_device(self, driver):
        """Test Case: Edit Device"""
        device_id = str(random.randint(257, 910) + 10)  # Avoid conflict with add test
        location = "Test Lab"
        ip = "172.20.10.48"
        edited_location = "Edited Location"
        new_ip = "169.254.157.43"
        self.device_page.add_device(device_id, ip, location)
        self.device_page.search_device(device_id)
        self.device_page.edit_device(edited_location, new_ip)
        self.device_page.assert_device_in_list(device_id)
        
    def test_delete_device(self, driver):
        """Test Case: Delete Device"""
        device_id = str(random.randint(257, 910) + 10)  # Avoid conflict with add test
        ip = "172.20.10.48"
        self.device_page.add_device(device_id, ip, location="DeleteTest")
        self.device_page.delete_device(device_id)
        self.device_page.assert_device_not_in_list(device_id)

    def test_search_device(self, driver):
        """Test Case: Search Devices"""
        device_id = str(random.randint(257, 910) + 10)  # Avoid conflict with add test
        ip = "172.20.10.48"
        location = "SearchTest"
        self.device_page.add_device(device_id, ip, location)
        self.device_page.search_device(device_id)
        self.device_page.assert_device_in_list(device_id)

    def test_delete_multiple_devices(self, driver):
        """Test Case: Delete Multiple Devices"""
        device_id = str(random.randint(257, 910) + 10)  # Avoid conflict with add test
        device_id2 = str(random.randint(257, 910) + 20)  # Ensure second ID is different
        ip = "172.20.10.48"
        location = "DeleteTest"
        location2 = "DeleteTest2"
        self.device_page.add_device(device_id, ip, location)
        self.device_page.add_device(device_id2, ip, location2) # Add second device for multiple delete test
        self.device_page.delete_multiple_devices()
        self.device_page.assert_no_devices_present(driver)

        
    