import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import Config
from utils.logger import logger
from utils.screenshot import take_screenshot


def _as_bool(value, fallback: bool) -> bool:
    if value is None:
        return fallback
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("1", "true", "yes")


def _in_ci() -> bool:
    return (
        os.getenv("TF_BUILD") == "True"
        or os.getenv("CI", "").lower() in ("1", "true", "yes")
    )


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=Config.BROWSER or "chrome",
        help="Browser: chrome or firefox",
    )
    parser.addoption(
        "--headless",
        action="store",
        default=None,
        help="true/false. Defaults to Config.HEADLESS, or true in CI.",
    )


@pytest.fixture(scope="function")
def driver(request):
    browser = (request.config.getoption("--browser") or "chrome").split()[0].strip().lower()
    headless = _as_bool(
        request.config.getoption("--headless"),
        True if _in_ci() else bool(Config.HEADLESS),
    )

    if browser != "chrome":
        raise ValueError(f"Browser {browser} not supported")

    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    if headless:
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    if not headless:
        driver.maximize_window()
    logger.info(f"Started {browser} driver (headless={headless})")

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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = take_screenshot(driver, item.name)
            logger.info(f"Screenshot saved: {screenshot_path}")
            try:
                import allure
                allure.attach.file(
                    screenshot_path,
                    name="Screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except ImportError:
                pass


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "hardware: mark test as requiring real hardware (skipped in CI)",
    )


def pytest_collection_modifyitems(config, items):
    if Config.MOCK_HARDWARE:
        skip_hardware = pytest.mark.skip(
            reason="Hardware test skipped in CI (MOCK_HARDWARE=true)"
        )
        for item in items:
            if "hardware" in item.keywords:
                item.add_marker(skip_hardware)
