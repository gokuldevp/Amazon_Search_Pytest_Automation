from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from page_objects.base_page import BasePage

class TestProductDetailsPage(BasePage):
    BUTTON_ADD_TO_CART_ID = 'add-to-cart-button'
    TEXT_PRODUCT_OVERVIEW_ID = 'productOverview_feature_div'
    TEXT_PRODUCT_FEATURES_ID = 'featurebullets_feature_div'
    IMAGE_GALLERY_ID = 'altImages'

    def switch_to_new_tab(self):
        """Switches the WebDriver to the newly opened tab."""
        try:
            tabs = self.driver.window_handles
            self.driver.close()
            self.driver.switch_to.window(tabs[-1])
            self._log("Switched to the new tab successfully.")
        except Exception as e:
            self._log("Failed to switch to the new tab.", is_error=True)
            raise e

    def click_first_product(self):
        """Clicks on the first product in the list."""
        self._log("Attempting to click the first product.")
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self.TEXT_PRODUCT_URL_XPATH))).click()
            self._log("First product link clicked successfully.")
            self.switch_to_new_tab()
        except (TimeoutException, NoSuchElementException) as e:
            self._log(f"Error while clicking the first product link: {str(e)}", is_error=True)
            raise e

    def return_first_product_name(self):
        """Returns the name of the first product in the list."""
        self._log("Attempting to retrieve the name of the first product.")
        try:
            product_name = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.TEXT_PRODUCT_TITLES_XPATH))).text
            self._log(f"First product name retrieved successfully: {product_name}")
            return product_name
        except (TimeoutException, NoSuchElementException) as e:
            self._log(f"Error retrieving the first product name: {str(e)}", is_error=True)
            raise e

    def verify_product_page_loaded(self, product_name):
        """Verify that the product page has loaded successfully."""
        self._log(f"Attempting to verify product page is loaded for {product_name}.")
        try:
            is_page_loaded = self.wait.until(EC.title_contains(product_name))
            assert is_page_loaded, "Product page is not loaded successfully"
            self._log("Product page loaded successfully.")
        except (TimeoutException, NoSuchElementException) as e:
            self._log(f"Error verifying product page load: {str(e)}", is_error=True)
            raise e

    def verify_presence_of_element(self, element_id, description):
        """Generic method to verify the presence of an element."""
        self._log(f"Attempting to verify presence of {description}.")
        try:
            is_present = self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
            assert is_present, f"{description} is not present on the product details page"
            self._log(f"{description} is present.")
        except Exception as e:
            self._log(f"Error verifying presence of {description}: {str(e)}", is_error=True)
            raise e

    def verify_presence_of_add_to_cart(self):
        """Verify the presence of the 'Add to Cart' button."""
        self.verify_presence_of_element(self.BUTTON_ADD_TO_CART_ID, "Add to Cart button")

    def verify_presence_of_product_overview(self):
        """Verify the presence of the product overview section."""
        self.verify_presence_of_element(self.TEXT_PRODUCT_OVERVIEW_ID, "Product overview section")

    def verify_presence_of_product_details(self):
        """Verify the presence of the product details section."""
        self.verify_presence_of_element(self.TEXT_PRODUCT_FEATURES_ID, "Product details section")

    def verify_presence_of_image_gallery(self):
        """Verify the presence of the image gallery."""
        self.verify_presence_of_element(self.IMAGE_GALLERY_ID, "Image gallery")
