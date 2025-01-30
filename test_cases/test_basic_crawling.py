import pytest
import os
from page_objects.home_page import HomePage
from page_objects.search_result_page import SearchResultPage
from configs.configs import SEARCH_ITEMS

@pytest.mark.usefixtures("setup")
class TestBasicCrawling:
    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def remove_csv_file_once(cls):
        """
        Removes the existing CSV file before running tests, ensuring this runs only once.
        """
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__).replace('test_cases\\', '')), 'test_data', 'product_info.csv')
        if os.path.exists(file_path):
            os.remove(file_path)

    @pytest.fixture(autouse=True)
    def setup_pages(self):
        self.home_page = HomePage(self.driver, self.logger)
        self.search_result_page = SearchResultPage(self.driver, self.logger)
        # Open Amazon homepage
        success = self.home_page.open_amazon_website()
        assert success, "Failed to open Amazon homepage"

    @pytest.mark.parametrize("search_term", SEARCH_ITEMS)
    def test_amazon_product_search_and_export(self, search_term):

        # Step 1: Search for the product based on the given search term
        self.home_page.search_product(search_term)
        assert search_term in self.driver.current_url, f"Failed to search for the product {search_term}"

        # Step 2: Extract product information from the search results
        products_info = self.search_result_page.extract_product_information()
        assert len(products_info) > 0, f"No products found for search term {search_term}"

        # Step 3: Navigate to the next page of search results, Extract product information from the results
        self.search_result_page.click_next_page()
        products_info.extend(self.search_result_page.extract_product_information())
        assert len(products_info) > 0, f"No products found for search term {search_term}"

        # Step 4: Save all the extracted product information to a CSV file
        self.search_result_page.save_product_information_to_csv(search_term, products_info)


