from selenium.webdriver.support.ui import WebDriverWait
from configs.configs import TIMEOUT

class BasePage:
    """Base class for all page objects to handle common operations."""
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        self.browser_name = self.driver.capabilities.get('browserName', 'Unknown')

    def _log(self, message, is_error=False):
        """Centralized logging method."""
        log_method = self.logger.error if is_error else self.logger.info
        log_method(f"{'ERROR' if is_error else 'INFO'} :: {self.browser_name} :: {message}")