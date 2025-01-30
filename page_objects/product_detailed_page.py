from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utilities.utilities import ScreeShots
from configs.configs import TIMEOUT

class TestProductDetailsPage:
    BUTTON_ADD_TO_CART_ID ='add-to-cart-button'
    TEXT_PRODUCT_OVERVIEW_ID = 'productOverview_feature_div'
    TEXT_PRODUCT_FEATURES_ID = 'featurebullets_feature_div'
    

    def __init__(self, driver, logger):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, TIMEOUT, 2)
        self.SS = ScreeShots(self.driver)
        self.logger = logger
        self.browser_name = self.driver.capabilities.get('browserName', 'Unknown')

    def _handle_logger(self, info):
        """Log general information messages."""
        self.logger.info(f"{self.browser_name} :: {info}")

    def _handle_error(self, error):
        """Log error messages."""
        self.logger.error(f"{self.browser_name} :: {error}")

        
    def switch_to_new_tab(self):
        """
        Switches the WebDriver to the newly opened tab.
        Logs the tab switch operation.
        """
        try:
            tabs = self.driver.window_handles
            self.driver.close()
            self.driver.switch_to.window(tabs[-1])
            self._handle_logger("Switched to the new tab successfully.")
        except Exception as e:
            self._handle_error(f"Failed to switch to the new tab.")
            raise e

    def click_first_product(self):
        """
        Clicks on the first product in the list. 
        Logs each step for better traceability.
        """
        try:
            self._handle_logger("Attempting to click the first product.")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self.TEXT_PRODUCT_URL_XPATH))).click()
            self._handle_logger("First product link clicked successfully.")
            self.switch_to_new_tab()
        
        except TimeoutException as e:
            self._handle_error("Timeout while waiting for the first product link to become clickable.")
            raise e

        except NoSuchElementException as e:
            self._handle_error("No such element found while trying to click the first product link.")
            raise e
        
        except Exception as e:
            self._handle_error(f"Unexpected error clicking the first product link.")
            raise e
        
    def return_first_product_name(self):
        """
        Returns the name of the first product in the list.
        Logs each step for better traceability.
        """
        try:
            self._handle_logger("Attempting to retrieve the name of the first product.")
            product_name = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.TEXT_PRODUCT_TITLES_XPATH))).text
            self._handle_logger(f"First product name retrieved successfully: {product_name}")
            return product_name
        
        except TimeoutException as e:
            self._handle_error("Timeout while waiting for the first product name to become visible.")
            raise e

        except NoSuchElementException as e:
            self._handle_error("No such element found while trying to retrieve the first product name.")
            raise e
        
        except Exception as e:
            self._handle_error(f"Unexpected error retrieving the first product name.")
            raise e
        
    def verify_product_page_loaded(self, product_name):
        """
        Verify that the product page has loaded successfully by checking if the page title contains the product name.

        :param product_name: The name of the product to verify.
        """
        try:
            self._handle_logger(f"Attempting to verify product page is loaded for {product_name}.")
            is_page_loaded = self.wait.until(EC.title_contains(product_name))
        
        except Exception as e:
            self._handle_error("Unexpected error while verifying product page is loaded.")
            raise e
        
        assert is_page_loaded, "Product page is not loaded successfully"

        self._handle_logger("Product page loaded successfully.")

    def verify_presence_of_add_to_cart(self):
        """
        Verify the presence of the 'Add to Cart' button on the product details page.
        """
        try:
            self._handle_logger(f"Attempting to verify presence of add to cart in the product details page.")

            is_present = self.wait.until(EC.presence_of_element_located((By.ID, self.BUTTON_ADD_TO_CART_ID)))
        
        except Exception as e:
            self._handle_error("Unexpected error while verifying presence of add to cart in the product details page.")
            raise e
        
        assert is_present, "Add to Cart is not present on the product details page"

        self._handle_logger("Product page loaded successfully.")

    def verify_presence_of_product_overview(self):
        """
        Verify the presence of the product overview section on the product details page.
        """
        try:
            self._handle_logger(f"Attempting to verify presence of product overview.")
            is_present = self.wait.until(EC.presence_of_element_located((By.ID, self.TEXT_PRODUCT_OVERVIEW_ID)))

        except Exception as e:
            self._handle_error("Unexpected error while verifying presence of product overview.")
            raise e
        
        assert is_present, "Product overview is not present on the product details page"
        self._handle_logger("Product overview section is present.")

    def verify_presence_of_product_details(self):
        """
        Verify the presence of the product details section on the product details page.
        """
        try:
            self._handle_logger(f"Attempting to verify presence of product details.")
            is_present = self.wait.until(EC.presence_of_element_located((By.ID, self.TEXT_PRODUCT_FEATURES_ID)))

        except Exception as e:
            self._handle_error("Unexpected error while verifying presence of product details.")
            raise e
        assert is_present, "Product details are not present on the product details page"
        self._handle_logger("Product details section is present.")
