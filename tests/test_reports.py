import pytest
from pages.reports_page import ReportsPage
from pages.login_page import LoginPage

class TestReports:
    def test_navigate_to_events_report(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        reports = ReportsPage(driver)
        reports.navigate_to_events()
        assert "events" in driver.current_url

    def test_generate_events_report(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login()
        reports = ReportsPage(driver)
        reports.navigate_to_events()
        reports.set_date_range("2025-01-01", "2025-01-31")
        reports.select_device("257")
        reports.select_event_category("Blast")
        reports.generate_report()
        # Wait for report to load
        assert reports.is_displayed(reports.REPORT_TABLE)