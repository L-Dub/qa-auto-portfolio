import pytest
from pages.device_page import DevicePage
from pages.login_page import LoginPage

@pytest.mark.hardware
class TestFirmware:
    def test_upload_firmware(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        device_page = DevicePage(driver)
        device_page.navigate()
        device_page.upload_firmware("/path/to/firmware.bin", "BCU II")
        # Check events log for upload completion
        # ...