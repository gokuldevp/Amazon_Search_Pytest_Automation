from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from utilities.utilities import ScreeShots
from configs.configs import BASE_URL, TIMEOUT

class HomePage:
    INPUT_SEARCH_ID = "twotabsearchtextbox"
    BUTTON_SEARCH_ID = "nav-search-submit-button"
    LOGO_ID = "nav-logo-sprites"
    DESKTOP_BANNER_ID = "desktop-banner"

    def __init__(self, driver, logger):
        """Initialize WebDriver, WebDriverWait, Screenshots, and Logger."""
        self.driver = driver
        self.wait = WebDriverWait(self.driver, TIMEOUT, 2)
        self.SS = ScreeShots(self.driver)
        self.logger = logger
        self.browser_name = self.driver.capabilities.get('browserName', 'Unknown')

    # Logger functions
    def _handle_logger(self, info):
        """Log general information messages."""
        self.logger.info(f"Info :: {self.browser_name} :: {info}")

    def _handle_error(self, error):
        """Log error messages."""
        self.logger.error(f"Error :: {self.browser_name} :: {error}")

    # Open Amazon homepage and verify essential elements
    def open_amazon_website(self):
        """
        Opens the Amazon home page and verifies essential elements.

        Returns:
            bool: True if both the logo and banner are displayed, False otherwise.
        """
        self._handle_logger("Navigating to Amazon home page.")

        try:
            self.driver.get(BASE_URL)
            logo_displayed = self.wait.until(EC.presence_of_element_located((By.ID, self.LOGO_ID))).is_displayed()
            banner_displayed = self.wait.until(EC.presence_of_element_located((By.ID, self.DESKTOP_BANNER_ID))).is_displayed()

            if logo_displayed and banner_displayed:
                self._handle_logger("Amazon home page loaded successfully.")
                return True

        except TimeoutException as e:
            self._handle_error("Timeout while loading Amazon home page.")
        except WebDriverException as e:
            self._handle_error(f"WebDriver error: {str(e)}")
        except Exception as e:
            self._handle_error(f"Unexpected error while opening Amazon: {str(e)}")

        return False

    # Perform a product search
    def search_product(self, search):
        """
        Searches for a product on Amazon.

        Args:
            search (str): The search query.

        Returns:
            bool: True if search was performed successfully, False otherwise.
        """
        self._handle_logger(f"Attempting to search for: {search}")

        try:
            search_box = self.wait.until(EC.element_to_be_clickable((By.ID, self.INPUT_SEARCH_ID)))
            search_box.clear()
            search_box.send_keys(search)

            search_button = self.wait.until(EC.element_to_be_clickable((By.ID, self.BUTTON_SEARCH_ID)))
            search_button.click()

            self._handle_logger("Search executed successfully.")
            return True

        except TimeoutException as e:
            self._handle_error("Search box or search button not found.")
        except NoSuchElementException as e:
            self._handle_error("Search elements not present on the page.")
        except Exception as e:
            self._handle_error(f"Unexpected error during search: {str(e)}")
        return False
