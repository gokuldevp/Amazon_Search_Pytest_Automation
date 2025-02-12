from time import sleep
from random import randint
from page_objects.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from configs.configs import BASE_URL, SCREEN_SIZES

class HomePage(BasePage):
    INPUT_SEARCH_ID = "twotabsearchtextbox"
    BUTTON_SEARCH_ID = "nav-search-submit-button"
    LOGO_ID = "nav-logo-sprites"
    DESKTOP_BANNER_ID = "desktop-banner"
    INPUT_CAPTCHA_ID = 'captchacharacters'

    def refresh_if_captcha(self):
        """Check for CAPTCHA presence and refresh the page if detected."""
        
        attempts = 3
        for attempt in range(attempts):
            self._log(f"Attempt {attempt + 1} to check CAPTCHA.")
            try:
                self.wait.until(EC.presence_of_element_located((By.ID, self.INPUT_CAPTCHA_ID)))
                self._log("CAPTCHA detected, refreshing the page.")
                sleep(randint(2, 6))
                self.driver.refresh()
                self._log("Page refreshed successfully.")
                # Re-check for CAPTCHA after refresh
                self.wait.until(EC.presence_of_element_located((By.ID, self.INPUT_CAPTCHA_ID)))
                self._log("CAPTCHA still present after refresh.")
            except (TimeoutException, NoSuchElementException):
                self._log("No CAPTCHA element found on the page.")
                return

        self._log("Run failed due to CAPTCHA being present after maximum attempts.")
        assert False, "Run failed due to CAPTCHA being present."

    def open_amazon_website(self, device='desktop'):
        """
        Opens the Amazon home page and verifies essential elements.

        :param device: Name of the device under test (e.g., desktop, tablet, mobile)
        :returns: bool: True if both the logo and banner are displayed, False otherwise.
        :raises: TimeoutException, WebDriverException, Exception
        """
        self._log("Navigating to Amazon home page.")

        try:
            self.driver.set_window_size(*SCREEN_SIZES[device])
            self.driver.get(BASE_URL)

            self.refresh_if_captcha()

            logo_displayed = self.wait.until(EC.presence_of_element_located((By.ID, self.LOGO_ID))).is_displayed()
            banner_displayed = self.wait.until(EC.presence_of_element_located((By.ID, self.DESKTOP_BANNER_ID))).is_displayed()

            if logo_displayed and banner_displayed:
                self._log("Amazon home page loaded successfully.")
                return True

        except (TimeoutException, WebDriverException) as e:
            self._log("Error while loading Amazon home page", is_error=True)
            raise e
        except Exception as e:
            self._log("Unexpected error while opening Amazon", is_error=True)
            raise e

        return False

    def search_product(self, search):
        """
        Searches for a product on Amazon.

        :param search: The search query.
        :returns: bool: True if search was performed successfully, False otherwise.
        """
        self._log(f"Attempting to search for: {search}")

        try:
            search_box = self.wait.until(EC.element_to_be_clickable((By.ID, self.INPUT_SEARCH_ID)))
            search_box.clear()
            search_box.send_keys(search)

            search_button = self.wait.until(EC.element_to_be_clickable((By.ID, self.BUTTON_SEARCH_ID)))
            search_button.click()

            self._log("Search executed successfully.")
            return True

        except (TimeoutException, NoSuchElementException) as e:
            self._log("Search elements not found on the page.", is_error=True)
        except Exception as e:
            self._log(f"Unexpected error during search: {str(e)}", is_error=True)

        return False
