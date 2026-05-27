import pytest
from pages.login_page import LoginPage
from pages.group_page import GroupPage
import time


class TestGroups:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        login_page.assert_login_successful()
        self.group_page = GroupPage(driver)
        self.group_page.navigate()

    def test_view_groups(self, driver):
        #Test Case: View Groups
        self.group_page.assert_element_displayed(self.group_page.GROUP_TABLE)
        
    def test_add_group(self, driver):
        #Test Case: Add Group
        name="test group"
        self.group_page.add_group(name)
        self.group_page.search_group(name)
        self.group_page.delete_using_icon()

    def test_delete_group_using_icon(self, driver):
        #Test Case: Delete Group using Icon
        name="test group"
        self.group_page.add_group(name)
        self.group_page.search_group(name)
        self.group_page.delete_using_icon()

"""
    def test_delete_multiple_groups(self, driver):
        #Test Case: Delete Group using Checkbox
        name="test group"
        self.group_page.add_group(name)
        self.group_page.delete_multiple_groups_using_button()
        print("Delete by button completed successfully")

    def test_search_group(self, driver):
        #Test Case: Search Group
        name="test group"
        self.group_page.add_group(name)
        self.group_page.search_group(name)
        self.group_page.assert_group_in_list(name)
        self.group_page.delete_using_icon()  # Clean up by deleting the group
""" 
