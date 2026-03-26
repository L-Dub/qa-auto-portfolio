import pytest
from pages.network_page import NetworkPage
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By

class TestNetworkManagement:
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url, admin_credentials):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(admin_credentials["username"], admin_credentials["password"])
        login_page.assert_login_successful()
        self.network_page = NetworkPage(driver)
        self.network_page.navigate()
    
    def test_view_networks(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        network_page = NetworkPage(driver)
        network_page.navigate()
        assert network_page.is_displayed(network_page.NETWORK_TABLE)

    '''
    def test_add_network(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        network_page = NetworkPage(driver)
        network_page.navigate()
        network_page.add_network("ETHERNET1", report_detonators=True, in_use=True)
        
        # Verify network appears in table
        network_page.search_network("ETHERNET1")
        rows = network_page.find_elements((By.CSS_SELECTOR, "tbody tr"))
        assert len(rows) == 1
    '''