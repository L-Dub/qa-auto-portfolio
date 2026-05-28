import pytest
from time import sleep
from pages.dashboard_page import DashboardPage
from pages.device_page import DevicePage
from pages.firmware_upload_page import FirmwareUploadPage
from pages.login_page import LoginPage
from config import Config


class TestFirmwareUpload:
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url, eng_credentials):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(eng_credentials["username"], eng_credentials["password"])
        login_page.assert_login_successful()
        self.device_page = DevicePage(driver)
        self.device_page.navigate()
        self.firmware_upload_page = FirmwareUploadPage(driver)
        self.firmware_upload_page.navigate()
        
    def test_upload_firmware(self, driver):
        """Test Case: Upload Firmware"""
        self.dashboard_page = DashboardPage(driver)
        device_name = "Test Device Upgrade" # Ensure this device exists in the test environment and State is IDLE before running the test
        self.firmware_upload_page.device_update(file_path = Config.FIRMWARE_FILE_PATH)
        self.dashboard_page.navigate()
        self.firmware_upload_page.select_device(device_name)
        self.dashboard_page.open_action_panel()
        self.firmware_upload_page.upgrade_selected_devices()
        self.firmware_upload_page.assert_device_is_upgrading()
        self.firmware_upload_page.assert_upgrade_successful()
        
    def test_bootload_device(self):
        self.dashboard_page.open_action_panel()
        self.firmware_upload_page.bootload_device()
        self.firmware_upload_page.assert_bootloading_is_successful()
        