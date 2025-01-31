from datetime import datetime
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utilities.utilities import ScreeShots, get_current_date, loggen

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
            screenshot_handler = ScreeShots(driver)
            file_name = now.strftime("%S%H%d%m%Y")
            file_name = screenshot_handler.take_screenshots_as_png(file_name)
            if file_name:
                html = f'<div><img src="{file_name}" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>'
                extra.append(pytest_html.extras.html(html))
        report.extras = extra

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    now = datetime.now()
    report_dir = Path('Reports', get_current_date())
    report_dir.mkdir(parents=True, exist_ok=True)
    config.option.htmlpath = report_dir / f"report_{now.strftime('%H%M%S')}.html"
    config.option.self_contained_html = True

def pytest_html_report_title(report):
    report.title = "Automation Report"

@pytest.fixture(scope="class", params=["edge"])#, "chrome", "firefox"])
def setup(request):
    browser = request.param
    driver = None

    browser_options = {
        "chrome": (webdriver.ChromeOptions(), ChromeService(ChromeDriverManager().install())),
        "edge": (webdriver.EdgeOptions(), EdgeService(EdgeChromiumDriverManager().install())),
        "firefox": (webdriver.FirefoxOptions(), FirefoxService(GeckoDriverManager().install()))
    }

    if browser in browser_options:
        options, service = browser_options[browser]
        driver = webdriver.Chrome(service=service, options=options) if browser == "chrome" else \
                 webdriver.Edge(service=service, options=options) if browser == "edge" else \
                 webdriver.Firefox(service=service, options=options)
    else:
        raise ValueError(f"Browser '{browser}' is not supported.")

    logger = loggen()
    logger.info(f"Launching {browser.capitalize()} Browser")
    request.cls.driver = driver
    request.cls.logger = logger

    yield driver, logger

    driver.quit()
    logger.info(f"Closing the {browser.capitalize()} Browser")
