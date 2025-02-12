import logging
import os
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver import Chrome, Firefox, Edge
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from datetime import datetime, date

# --------------------------
# Date Factory
# --------------------------
class DateFactory:
    @staticmethod
    def get_current_date(format_str: str = "%Y_%m_%d") -> str:
        return date.today().strftime(format_str)

    @staticmethod
    def get_current_datetime(format_str: str = "%Y%m%d%H%M%S") -> str:
        return datetime.now().strftime(format_str)
    
    # --------------------------
# Screenshot Strategies
# --------------------------
class ScreenshotStrategy(ABC):
    @abstractmethod
    def save(self, driver, path: str):
        pass

class PNGStrategy(ScreenshotStrategy):
    def save(self, driver, path: str):
        driver.save_screenshot(path)

class ScreenshotManager:
    def __init__(
        self, 
        driver, 
        strategy: ScreenshotStrategy = PNGStrategy(),
        base_dir: str = "Reports"
    ):
        self.driver = driver
        self.strategy = strategy
        self.base_dir = base_dir

    def take_screenshot(self, screenshot_name: str) -> str:
        dir_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            self.base_dir, 
            DateFactory.get_current_date("%Y_%m_%d")
        )
        os.makedirs(dir_path, exist_ok=True)

        timestamp = DateFactory.get_current_datetime('%d_%m_%Y_%H_%M_%S')
        file_name = f"{timestamp}_{screenshot_name}.png"
        full_path = os.path.join(dir_path, file_name)

        self.strategy.save(self.driver, full_path)
        return file_name
    
# --------------------------
# Singleton Logger
# --------------------------
class SingletonLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._configure_logger()
        return cls._instance

    def _configure_logger(self):
        self.logger = logging.getLogger('automation')
        self.logger.setLevel(logging.INFO)
        
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'automation.log')
        
        if not self.logger.handlers:
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                "%(asctime)s: %(levelname)s: %(message)s", 
                datefmt="%m/%d/%Y %I:%M:%S %p"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger
    
# Factory Pattern for Browsers
class Browser(ABC):
    @abstractmethod
    def create_driver(self):
        pass

class ChromeBrowser(Browser):
    def create_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        service = ChromeService(ChromeDriverManager().install())
        return Chrome(service=service, options=options)

class FirefoxBrowser(Browser):
    def create_driver(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        service = FirefoxService(GeckoDriverManager().install())
        return Firefox(service=service, options=options)

class EdgeBrowser(Browser):
    def create_driver(self):
        options = webdriver.EdgeOptions()
        options.add_argument('--headless')
        service = EdgeService(EdgeChromiumDriverManager().install())
        return Edge(service=service, options=options)

class BrowserFactory:
    @staticmethod
    def get_browser(browser_name: str) -> Browser:
        browsers = {
            "chrome": ChromeBrowser(),
            "firefox": FirefoxBrowser(),
            "edge": EdgeBrowser()
        }
        return browsers.get(browser_name.lower())