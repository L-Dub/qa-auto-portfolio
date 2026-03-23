from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class ReportsPage(BasePage):
    REPORTS_DROPDOWN = (By.XPATH, "//span[text()='Reports']/ancestor::button")
    EVENTS_REPORT_LINK = (By.XPATH, "//button[.//span[text()='Events report']]")
    BLAST_SUMMARY_LINK = (By.XPATH, "//button[.//span[text()='Blast Summary']]")
    BLAST_REPORT_LINK = (By.XPATH, "//button[.//span[text()='Blast Report']]")
    NETWORK_REPORT_LINK = (By.XPATH, "//button[.//span[text()='Network report']]")
    GENERATE_BLAST_REPORT = (By.XPATH, "//button[contains(., 'Generate Report')]")
    # EXPORT_BUTTON = (By.ID, "export")
    DATE_FROM = (By.XPATH, "//label[contains(text(), 'From')]/following-sibling::input")
    DATE_TO = (By.XPATH, "//label[contains(text(), 'To')]/following-sibling::input")
    DEVICE_SELECT = (By.ID, "selectDevice")
    EVENT_CATEGORY = (By.XPATH, "//mat-chip[contains(., '{}')]")
    REPORT_TABLE = (By.CSS_SELECTOR, "table.mat-mdc-table")
    GENERATE_EVENT_REPORT = (By.XPATH, "//button[contains(@class, 'generateReportBtn') and .//span[text()='Generate Report']]")

    def navigate_to_events(self):
        self.click(self.REPORTS_DROPDOWN)
        self.click(self.EVENTS_REPORT_LINK)

    def navigate_to_blast_summary(self):
        self.click(self.REPORTS_DROPDOWN)
        self.click(self.BLAST_SUMMARY_LINK)

    def navigate_to_blast_report(self):
        self.click(self.REPORTS_DROPDOWN)
        self.click(self.BLAST_REPORT_LINK)

    def navigate_to_network_report(self):
        self.click(self.NETWORK_REPORT_LINK)

    def set_date_range(self):
        self.click(self.DATE_FROM)
        self.click(self.DATE_TO)

    def select_device(self, device_id):
        self.select_dropdown(self.DEVICE_SELECT, device_id)

    def select_event_category(self, category_names):
        for name in category_names:
            self.select_event_category(name)

    def generate_blast_report(self):
        self.click(self.GENERATE_BLAST_REPORT)

    def generate_event_report(self):
        self.click(self.GENERATE_EVENT_REPORT)
        wait = webdriver.WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.mat-mdc-table")))