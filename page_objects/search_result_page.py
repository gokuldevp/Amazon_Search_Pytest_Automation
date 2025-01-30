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

    def _handle_logger(self, info):
        """Log general information messages."""
        self.logger.info(f"{self.browser_name} :: {info}")

    def _handle_error(self, error):
        """Log error messages."""
        self.logger.error(f"{self.browser_name} :: {error}")

    def extract_product_information(self):
        """
        Extracts product information from Amazon search results.
        
        Returns:
            list: A list of dictionaries containing product name, price, rating, and URL.
        """
        self._handle_logger("Starting to extract product information.")
        products_info = []

        try:
            products = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.SEARCH_RESULTS_XPATH)))
            names = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.TEXT_PRODUCT_TITLES_XPATH)))
            prices = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.TEXT_PRODUCT_PRICES_XPATH)))
            ratings = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.TEXT_PRODUCT_RATING_XPATH)))
            urls = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.TEXT_PRODUCT_URL_XPATH)))

            self._handle_logger("Found product details in the search results.")

            for i in range(len(products)):
                try:
                    product_info = {
                        "Name": names[i].text.strip(),
                        "Price": f"Rs. {prices[i].text.strip()}" if i < len(prices) else "N/A",
                        "Rating": ratings[i].get_attribute("aria-label").split()[0] if i < len(ratings) else "N/A",
                        "URL": urls[i].get_attribute("href") if i < len(urls) else "N/A"
                    }
                    products_info.append(product_info)
                    self._handle_logger(f"Extracted info for product {i + 1}: {product_info}")
                except IndexError as e:
                    self._handle_error(f"Missing data for product {i + 1}.")
                    raise e

        except TimeoutException as e:
            self._handle_error(f"Timeout while extracting product details")
            raise
        except Exception as e:
            self._handle_error(f"Unexpected error while extracting product details.")
            raise e

        self._handle_logger("Finished extracting product information.")
        return products_info
    
    def get_csv_file_path(self):
        """
        Constructs and returns the file path for the CSV file.
        """
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__).replace('page_objects\\', '')),'test_data', 'product_info.csv')
        return file_path

    def write_product_info_to_csv(self, file_path, product_name, product_info):
        """
        Writes the product information to the CSV file.
        """
        try:
            file_exists = os.path.isfile(file_path)

            with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
                csvfile.write(f'\nProduct Name: {product_name}\n')
                fieldnames = ['Name', 'Price', 'Rating', 'URL']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                for product in product_info:
                    writer.writerow(product)

            self._handle_logger(f"Product information for {product_name} saved successfully to {file_path}.")
        except Exception as e:
            self._handle_error(f"Error saving product information. Error: {str(e)}")
            raise e

    def save_product_information_to_csv(self, product_name, product_info):
        """
        Saves extracted product information to a CSV file.

        Args:
            product_name (str): The name of the product.
            product_info (list): List of dictionaries containing product details.
        """
        self._handle_logger(f"Saving product information for {product_name}.")

        try:
            # Get the file path
            file_path = self.get_csv_file_path()

            # Write the product information to the CSV file
            self.write_product_info_to_csv(file_path, product_name, product_info)

        except Exception as e:
            self._handle_error(f"Error saving product information. Error: {str(e)}")
            raise e


    # def save_product_information_to_csv(self, product_name, product_info):
    #     """
    #     Saves extracted product information to a CSV file.

    #     Args:
    #         product_name (str): The name of the product.
    #         product_info (list): List of dictionaries containing product details.
    #     """
    #     self._handle_logger(f"Saving product information for {product_name}.")

    #     try:
    #         file_path = os.path.join(os.path.dirname(os.path.abspath(__file__).replace('page_objects\\', '')),
    #                                  'test_data', 'product_info.csv')

    #         file_exists = os.path.isfile(file_path)

    #         with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
    #             csvfile.write(f'\nProduct Name: {product_name}\n')
    #             fieldnames = ['Name', 'Price', 'Rating', 'URL']
    #             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    #             if not file_exists:
    #                 writer.writeheader()

    #             for product in product_info:
    #                 writer.writerow(product)

    #         self._handle_logger(f"Product information for {product_name} saved successfully to {file_path}.")
    #     except Exception as e:
    #         self._handle_error(f"Error saving product information. Error: {str(e)}")
    #         raise e

    def click_next_page(self):
        """
        Clicks the "Next Page" button to navigate search results.
        Logs an error if the button is not found or not clickable.
        """
        self._handle_logger("Attempting to click the Next Page link.")

        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self.LINK_NEXT_PAGE_XPATH))).click()
            self._handle_logger("Successfully clicked the Next Page link.")
        except TimeoutException:
            self._handle_error("Next Page link not found or not clickable. Possibly the last page.")
            raise e
        except NoSuchElementException:
            self._handle_error("Next Page element does not exist on this page.")
            raise e
        except Exception as e:
            self._handle_error(f"Unexpected error clicking Next Page link.")
            raise e
        
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
            self._handle_logger(f"First product name retrieved successfully")
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