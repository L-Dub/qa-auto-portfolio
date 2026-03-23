"""
Test suite for Group Management (section 11 of test plan).
"""

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
        """Test Case: View Groups"""
        self.group_page.assert_element_displayed(self.group_page.GROUP_TABLE)

    def test_add_group(self, driver):
        """Test Case: Add Group"""
        name = f"Group_{int(time.time())}"
        self.group_page.add_group(name, "Test description")
        self.group_page.assert_group_in_list(name)

    def test_delete_group(self, driver):
        """Test Case: Delete Group"""
        name = f"DeleteGroup_{int(time.time())}"
        self.group_page.add_group(name, "To be deleted")
        self.group_page.assert_group_in_list(name)
        self.group_page.search_group(name)
        self.group_page.delete_first_group()
        self.group_page.assert_group_not_in_list(name)