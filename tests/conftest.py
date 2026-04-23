import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import Config
from utils.logger import logger
from utils.screenshot import take_screenshot


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=Config.BROWSER, help="Browser: chrome or firefox")
    parser.addoption("--headless", action="store_true", default=Config.HEADLESS, help="Run headless")

@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    if browser == "chrome":
        options = Options()
        options.add_argument("--log-level=3")   # 0=All, 1=Info, 2=Warnings, 3=Errors only
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Selenium Manager (built into Selenium 4.6+) automatically downloads and manages the correct ChromeDriver
        driver = webdriver.Chrome(options=options)
    else:
        raise ValueError(f"Browser {browser} not supported")
    
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.maximize_window()
    logger.info(f"Started {browser} driver")
    
    yield driver
    
    logger.info("Quitting driver")
    driver.quit()

@pytest.fixture
def base_url():
    return Config.BASE_URL

@pytest.fixture
def admin_credentials():
    return {"username": Config.ADMIN_USERNAME, "password": Config.ADMIN_PASSWORD}

@pytest.fixture
def cbo_credentials():
    return {"username": Config.CBO_USERNAME, "password": Config.CBO_PASSWORD}

@pytest.fixture
def eng_credentials():
    return {"username": Config.ENG_USERNAME, "password": Config.ENG_PASSWORD}

# Hook for screenshot on failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = take_screenshot(driver, item.name)
            logger.info(f"Screenshot saved: {screenshot_path}")
            # Attach to Allure
            try:
                import allure
                allure.attach.file(screenshot_path, name="Screenshot", attachment_type=allure.attachment_type.PNG)
            except ImportError:
                pass

# Marker for hardware-dependent tests
def pytest_configure(config):
    config.addinivalue_line("markers", "hardware: mark test as requiring real hardware (skipped in CI)")

def pytest_collection_modifyitems(config, items):
    if Config.MOCK_HARDWARE:
        skip_hardware = pytest.mark.skip(reason="Hardware test skipped in CI (MOCK_HARDWARE=true)")
        for item in items:
            if "hardware" in item.keywords:
                item.add_marker(skip_hardware)