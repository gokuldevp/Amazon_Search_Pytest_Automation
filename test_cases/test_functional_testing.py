import pytest
from page_objects.home_page import HomePage
from page_objects.search_result_page import SearchResultPage
from page_objects.product_detailed_page import TestProductDetailsPage
from configs.configs import SEARCH_ITEMS, SCREEN_SIZES

@pytest.mark.usefixtures("setup")
class TestFunctionalTesting:

    @pytest.fixture(autouse=True)
    def setup_pages(self):
        """
        Set up page objects for the test.
        This fixture runs automatically before each test.
        """
        self.home_page = HomePage(self.driver, self.logger)
        self.search_result_page = SearchResultPage(self.driver, self.logger)
        self.product_details_page = TestProductDetailsPage(self.driver, self.logger)

    @pytest.mark.parametrize("device", SCREEN_SIZES)
    @pytest.mark.parametrize("search_term", SEARCH_ITEMS)
    def test_amazon_product_search_and_export(self, search_term, device):
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

        # Step 2: Retrieve the name of the first product in the search results
        product_name = self.search_result_page.return_first_product_name()

        # Step 3: Click on the first product and verify its details
        self.search_result_page.click_first_product()
        self.product_details_page.verify_product_page_loaded(product_name)

        # Step 4: Verify the presence of essential elements on the product details page
        self.product_details_page.verify_presence_of_add_to_cart()
        self.product_details_page.verify_presence_of_product_overview()
        self.product_details_page.verify_presence_of_product_details()
        self.product_details_page.verify_presence_of_image_gallery()
