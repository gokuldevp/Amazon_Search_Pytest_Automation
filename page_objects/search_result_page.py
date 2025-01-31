import csv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utilities.utilities import ScreeShots
from configs.configs import TIMEOUT

class SearchResultPage:
    INPUT_SEARCH_ID = "twotabsearchtextbox"
    BUTTON_SEARCH_ID = "nav-search-submit-button"
    LOGO_ID = "nav-logo-sprites"
    DESKTOP_BANNER_ID = "desktop-banner"
    SEARCH_RESULTS_XPATH = '//div[@data-component-type="s-search-result"]'
    TEXT_PRODUCT_TITLES_XPATH = '//div[@data-component-type="s-search-result"]//h2//span'
    TEXT_PRODUCT_PRICES_XPATH = '//div[@data-component-type="s-search-result"]//span[@class="a-price-whole"]'
    TEXT_PRODUCT_RATING_XPATH = '//i[@data-cy="reviews-ratings-slot"]/parent::a'
    TEXT_PRODUCT_URL_XPATH = '//div[@data-component-type="s-search-result"]//span[@data-component-type="s-product-image"]//a'
    LINK_NEXT_PAGE_XPATH = '//a[contains(@aria-label,"Go to next page")]'

    def __init__(self, driver, logger):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, TIMEOUT, 2)
        self.SS = ScreeShots(self.driver)
        self.logger = logger
        self.browser_name = self.driver.capabilities.get('browserName', 'Unknown')

    def _log(self, message, is_error=False):
        """Log messages with appropriate severity."""
        log_method = self.logger.error if is_error else self.logger.info
        log_method(f"{'Error' if is_error else 'Info'} :: {self.browser_name} :: {message}")

    def extract_product_information(self):
        """Extracts product information from Amazon search results."""
        self._log("Starting to extract product information.")
        products_info = []

        try:
            products = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.SEARCH_RESULTS_XPATH)))
            names = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.TEXT_PRODUCT_TITLES_XPATH)))
            prices = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.TEXT_PRODUCT_PRICES_XPATH)))
            ratings = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.TEXT_PRODUCT_RATING_XPATH)))
            urls = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.TEXT_PRODUCT_URL_XPATH)))

            self._log("Found product details in the search results.")

            for i in range(len(products)):
                product_info = {
                    "Name": names[i].text.strip(),
                    "Price": f"Rs. {prices[i].text.strip()}" if i < len(prices) else "N/A",
                    "Rating": ratings[i].get_attribute("aria-label").split()[0] if i < len(ratings) else "N/A",
                    "URL": urls[i].get_attribute("href") if i < len(urls) else "N/A"
                }
                products_info.append(product_info)

        except TimeoutException as e:
            self._log("Timeout while extracting product details", is_error=True)
            raise e
        except Exception as e:
            self._log("Unexpected error while extracting product details", is_error=True)
            raise e

        self._log("Finished extracting product information.")
        return products_info
    
    def get_csv_file_path(self):
        """Constructs and returns the file path for the CSV file."""
        return os.path.join(os.path.dirname(os.path.abspath(__file__).replace('page_objects'+ os.sep, '')),'test_data', 'product_info.csv')

    def write_product_info_to_csv(self, file_path, product_name, device, product_info):
        """Writes the product information to the CSV file."""
        try:
            file_exists = os.path.isfile(file_path)

            with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
                csvfile.write(f'Product Name: {product_name}\n')
                csvfile.write(f'Browser Name: {self.browser_name}\n')
                csvfile.write(f'Device Name: {device}\n')
                fieldnames = ['Name', 'Price', 'Rating', 'URL']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                for product in product_info:
                    writer.writerow(product)

            self._log(f"Product information for {product_name} saved successfully.")
        except Exception as e:
            self._log("Error saving product information", is_error=True)
            raise e

    def save_product_information_to_csv(self, product_name, device, product_info):
        """Saves extracted product information to a CSV file."""
        self._log(f"Saving product information for {product_name}.")
        file_path = self.get_csv_file_path()
        self.write_product_info_to_csv(file_path, product_name, device, product_info)

    def click_next_page(self):
        """Clicks the "Next Page" button to navigate search results."""
        self._log("Attempting to click the Next Page link.")

        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self.LINK_NEXT_PAGE_XPATH))).click()
            self._log("Successfully clicked the Next Page link.")
        except (TimeoutException, NoSuchElementException) as e:
            self._log("Next Page link not found or not clickable. Possibly the last page.", is_error=True)
            raise e

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
            self._log("Error while trying to click the first product link.", is_error=True)
            raise e

    def return_first_product_name(self):
        """Returns the name of the first product in the list."""
        self._log("Attempting to retrieve the name of the first product.")
        try:
            product_name = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.TEXT_PRODUCT_TITLES_XPATH))).text
            self._log("First product name retrieved successfully")
            return product_name
        except (TimeoutException, NoSuchElementException) as  e:
            self._log("Error retrieving the first product name.", is_error=True)
            raise e
