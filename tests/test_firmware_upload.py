import pytest
from time import sleep
from pages.dashboard_page import DashboardPage
from pages.device_page import DevicePage
from pages.login_page import LoginPage
from config import Config


class TestFirmwareUpload:
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url, admin_credentials):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(admin_credentials["username"], admin_credentials["password"])
        login_page.assert_login_successful()
        self.device_page = DevicePage(driver)
        self.device_page.navigate()
        
    def test_upload_firmware(self, driver):
        """Test Case: Upload Firmware"""
        self.device_page = DevicePage(driver)
        self.device_page.upload_firmware(file_path = Config.FIRMWARE_FILE_PATH)
        