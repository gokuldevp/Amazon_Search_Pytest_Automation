import pytest
import os
from page_objects.home_page import HomePage
from page_objects.search_result_page import SearchResultPage
from page_objects.product_detailed_page import TestProductDetailsPage
from configs.configs import SEARCH_ITEMS

@pytest.mark.usefixtures("setup")
class TestFunctionalTesting:
    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def remove_csv_file_once(cls):
        """
        Removes the existing CSV file before running tests, ensuring this runs only once.
        """
        pass

    @pytest.fixture(autouse=True)
    def setup_pages(self, search_term):
        """Set up page objects for the test."""
        self.search_term = search_term
        self.home_page = HomePage(self.driver, self.logger)
        self.search_result_page = SearchResultPage(self.driver, self.logger)
        self.product_details_page = TestProductDetailsPage(self.driver, self.logger)

        # Open Amazon homepage
        success = self.home_page.open_amazon_website()
        assert success, "Failed to open Amazon homepage"

    @pytest.mark.parametrize("search_term", SEARCH_ITEMS)
    def test_amazon_product_search_and_export(self, search_term):
        """
        Test to search for a product and verify its details on Amazon.

        :param search_term: The search term to look for products.
        """

        # Step 1: Search for the product based on the given search term
        self.home_page.search_product(search_term)
        assert search_term in self.driver.current_url, f"Failed to search for the product {search_term}"

        # Step 2: Retrieve the name of the first product in the search results
        product_name = self.search_result_page.return_first_product_name()

        # Step 3: Click on the first product to open its details page
        self.search_result_page.click_first_product()

        # Step 4: Verify that the product details page is loaded for the selected product
        self.product_details_page.verify_product_page_loaded(product_name)

        # Step 5: Verify the presence of the 'Add to Cart' button on the product details page
        self.product_details_page.verify_presence_of_add_to_cart()

        # Step 6: Verify the presence of the product overview section on the product details page
        self.product_details_page.verify_presence_of_product_overview()

        # Step 7: Verify the presence of the product details section on the product details page
        self.product_details_page.verify_presence_of_product_details()
