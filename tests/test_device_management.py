import pytest
from pages.device_page import DevicePage
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By

class TestDeviceManagement:
    def test_view_devices(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        device_page = DevicePage(driver)
        device_page.navigate()
        assert device_page.is_displayed(device_page.DEVICE_TABLE)

    def test_add_device(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        device_page = DevicePage(driver)
        device_page.navigate()
        device_page.add_device("257", "192.168.1.100", "Test Location")
        device_page.search_device("257")
        rows = device_page.find_elements((By.CSS_SELECTOR, "tbody tr"))
        assert len(rows) == 1