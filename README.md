# Automated Crawling and Testing for a Sample Ecommerce Website

## Project Description
### Objective
This project aims to automate crawling and testing a sample e-commerce website (e.g., Amazon India) using Selenium. The script will focus on extracting product details from product pages and verifying specific elements on the website.

### Limitations
CAPTCHA challenges may prevent automation of certain actions. These cannot be bypassed within this script.

## Project Structure
```markdown
Reports/
  ├── 2025_01_30/
      ├── 30_01_2025_15_06_27_271530012025.png
      ├── report_150614.html
configs/
  ├── configs.py
  └── __pycache__/
page_objects/
  ├── __pycache__/
  ├── __init__.py
  ├── home_page.py
  ├── product_detailed_page.py
  ├── search_result_page.py
test_cases/
  ├── __pycache__/
  ├── __init__.py
  ├── conftest.py
  ├── test_basic_crawling.py
  ├── test_functional_testing.py
test_data/
  └── product_info.csv
utilities/
  ├── __pycache__/
  ├── __init__.py
  └── utilities.py
README.md
install_package.bat
requirements.txt
run.bat
```
## Features
* Automated Crawling: Automates the crawling of product pages on the sample e-commerce website (Amazon India).
* Product Information Extraction: Extracts key product details such as name, price, ratings, and availability from each product page.
* Functional Testing: Validates if the expected elements like product title, price, etc., are present on the product detail page.
* CSV Output: Stores the extracted product details in a structured CSV format (product_info.csv).

## Prerequisites
* Python 3.8+
* Required Python Libraries listed in requirements.txt
* Pip
* Google Chrome or any other supported browser

## Tools and Frameworks Used
* Selenium: For automating the web crawling and functional testing.
* Python: Primary language used for scripting.
* pytest: For running the tests.
* CSV: For storing extracted product details.

## Steps to Execute the Script
1. **Step 1**: Clone the Repository
```cmd
git clone https://github.com/gokuldevp/Amazon_Search_Pytest_Automation.git 
```

2. **Step 2**: Install Dependencies
There are two ways to install the required dependencies for this project:
* Option 1: Using pip install (Manual Method)
```cmd
cd your-repository-directory
pip install -r requirements.txt
```

* Option 2: Using install_package.bat (Automated Method)
Double-click the install_package.bat file or run the following command from the terminal or command prompt:
```cmd
install_package.bat
```

3. **Step 3**: Run the tests
There are two ways to run the test for this project:
* Option 1: Using Terminal (Manual Method)
```cmd
# Basic crawling
pytest test_cases/test_basic_crawling.py

# Basic crawling
pytest test_cases/test_functional_testing.py

# whole suite
pytest test_cases
```

* Option 2: Using run.bat (Automated Method)
Double-click the run.bat file or run the following command from the terminal or command prompt:
- Note: currently setup for whole suite
```cmd
run.bat
```
4. **Step 4**: Check the Output
* The extracted product information will be saved in product_info.csv located in the test_data/ folder
* Logs and screenshots will be stored in the Reports/2025_01_30/ folder

## Test Execution
You can view the test execution process and how to run the tests in this video:

Watch Test Execution on YouTube[https://youtu.be/f8BHg7vmhxI?si=ECYRETFpJD7rh4-W]