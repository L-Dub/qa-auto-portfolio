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
        self.device_page.assert_element_displayed(self.device_page.DEVICE_TABLE)

    def test_add_device(self, driver):
        """Test Case: Add Device"""
        device_id = str(random.randint(257, 910) + 10)  # Generate a random ID to avoid conflicts
        ip = "172.20.10.48"
        self.device_page.add_device(device_id, ip, location="Test Lab")
        self.device_page.assert_device_in_list(device_id)
        # self.device_page.delete_device(device_id)  # Clean up after test

    def test_delete_device(self, driver):
        """Test Case: Delete Device"""
        device_id = str(random.randint(257, 910) + 10)  # Avoid conflict with add test
        ip = "172.20.10.48"
        self.device_page.add_device(device_id, ip, location="DeleteTest")
        self.device_page.delete_device(device_id)
        self.device_page.assert_device_not_in_list(device_id)
        # self.device_page.delete_device(device_id)  # Clean up after test

    def test_search_device(self, driver):
        """Test Case: Search Devices"""
        device_id = str(random.randint(257, 910) + 10)  # Avoid conflict with add test
        ip = "172.20.10.48"
        self.device_page.add_device(device_id, ip, location="SearchTest")
        self.device_page.search_device(device_id)
        rows = self.device_page.get_device_rows()
        assert len(rows) == 1
        assert device_id in rows[0].text
        self.device_page.delete_device(device_id)  # Clean up after test
        
    def test_upload_firmware(self, driver):
        """Test Case: Upload Firmware"""
        self.device_page = DevicePage(driver)
        self.device_page.upload_firmware(file_path = Config.FIRMWARE_FILE_PATH)
        