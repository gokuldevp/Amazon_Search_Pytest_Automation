import pytest
from datetime import datetime
from pathlib import Path
from utilities.utilities import SingletonLogger, BrowserFactory, DateFactory, ScreenshotManager

# --------------------------
# Pytest Hooks & Fixtures
# --------------------------
@pytest.fixture(scope="class", params=["edge"])#, "chrome", "firefox"])
def setup(request):
    browser_name = request.param
    browser = BrowserFactory.get_browser(browser_name)
    
    if not browser:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    driver = browser.create_driver()
    logger = SingletonLogger().get_logger()
    logger.info(f"Launching {browser_name.capitalize()} Browser")
    
    request.cls.driver = driver
    request.cls.logger = logger

    yield driver, logger

    driver.quit()
    logger.info(f"Closing {browser_name.capitalize()} Browser")

# Rest of your hooks (pytest_runtest_makereport, etc.)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    now = datetime.now()
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    
    if report.when in ['call', 'setup']:
        driver = getattr(item.instance, 'driver', None)
        if driver:
            screenshot_manager = ScreenshotManager(driver)
            file_name = screenshot_manager.take_screenshot("screenshot")
            if file_name:
                html = f'<div><img src="{file_name}" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>'
                extra.append(pytest_html.extras.html(html))
        report.extras = extra

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    now = datetime.now()
    report_dir = Path('Reports', DateFactory.get_current_date("%Y_%m_%d"))
    report_dir.mkdir(parents=True, exist_ok=True)
    config.option.htmlpath = report_dir / f"report_{now.strftime('%H%M%S')}.html"
    config.option.self_contained_html = True

def pytest_html_report_title(report):
    report.title = "Automation Report"