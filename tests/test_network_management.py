import pytest
from pages.network_page import NetworkPage
from pages.login_page import LoginPage


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
        """View Networks"""
        self.network_page = NetworkPage(driver)   
        self.network_page.assert_element_displayed(self.network_page.NETWORK_TABLE) # Fails if network table not found on page
    
    def test_add_network(self, driver):
        """Add Network"""
        network_name = "ETHERNET1"
        self.network_page.add_network(network_name)
        self.network_page.assert_network_in_list(network_name) # Fails if network not found after addition
        self.network_page.delete_network_using_icon(network_name) # Clean up after test
    
    def test_delete_using_icon(self):
        """Delete Network Using Icon"""
        network_name = "ETHERNET1"
        
        self.network_page.add_network(network_name)
        self.network_page.search_network(network_name)
        self.network_page.delete_network_using_icon(network_name)
        self.network_page.assert_network_not_in_list(network_name) # Fails if network still found after deletion
        
    def test_search_network(self, network_name="ETHERNET1"):
        """Search Networks"""
        self.network_page.add_network(network_name)
        self.network_page.search_network(network_name)
        self.network_page.assert_network_in_list(network_name) # Fails if network not found
        self.network_page.delete_network_using_icon(network_name) # Clean up after test

    def test_edit_network(self):
        """Edit Network"""
        network_name = "ETHERNET1"
        new_network_name = "ETHERNET323"
        
        self.network_page.add_network(network_name)
        self.network_page.search_network(network_name)
        self.network_page.edit_network(new_network_name,network_name)
        self.network_page.search_network(new_network_name)
        self.network_page.assert_network_in_list(new_network_name) # Fails if edited network not found
        self.network_page.delete_network_using_icon(new_network_name) # Clean up after test
        
    def test_delete_using_button(self):
        """Delete Network Using Button"""
        network_name = "ETHERNET1"
        self.network_page.add_network(network_name)
        self.network_page.search_network(network_name)
        self.network_page.delete_network_using_btn(network_name)
        self.network_page.assert_network_not_in_list(network_name) # Fails if network still found after deletion
