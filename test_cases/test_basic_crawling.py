import pytest
import os
from page_objects.home_page import HomePage
from page_objects.search_result_page import SearchResultPage
from configs.configs import SEARCH_ITEMS, SCREEN_SIZES

@pytest.mark.usefixtures("setup")
class TestBasicCrawling:

    @classmethod
    @pytest.fixture(scope="session", autouse=True)
    def remove_csv_file_once(cls):
        """
        Removes the existing CSV file before running tests, ensuring this runs only once.
        """
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_data')
        file_path = os.path.join(dir_path, 'product_info.csv')

        # Remove the existing CSV file
        if os.path.exists(file_path):
            os.remove(file_path)

        # Create the directory if it doesn't exist
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @pytest.fixture(autouse=True)
    def setup_pages(self):
        """
        Set up page objects for the test.
        This fixture runs automatically before each test.
        """
        self.home_page = HomePage(self.driver, self.logger)
        self.search_result_page = SearchResultPage(self.driver, self.logger)

    @pytest.mark.parametrize("device", SCREEN_SIZES)
    @pytest.mark.parametrize("search_term", SEARCH_ITEMS)
    def test_amazon_product_search_and_product_details(self, search_term, device):
        """
        Test to search for a product and verify its details on Amazon.

        :param search_term: The search term to look for products.
        :param device: The device type (e.g., desktop, tablet, mobile).
        """
        # Open Amazon homepage
        assert self.home_page.open_amazon_website(device), "Failed to open Amazon homepage"

        # Step 1: Search for the product based on the given search term
        self.home_page.search_product(search_term)
        assert search_term in self.driver.current_url, f"Failed to search for the product {search_term}"

        # Step 2: Extract product information from the search results
        products_info = self.search_result_page.extract_product_information()
        assert products_info, f"No products found for search term {search_term}"

        # Step 3: Navigate to the next page of search results and extract product information
        self.search_result_page.click_next_page()
        products_info.extend(self.search_result_page.extract_product_information())
        assert products_info, f"No products found for search term {search_term}"

        # Step 4: Save all the extracted product information to a CSV file
        self.search_result_page.save_product_information_to_csv(search_term, device, products_info)
