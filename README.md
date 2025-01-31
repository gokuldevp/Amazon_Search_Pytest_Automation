# Automated Web Crawling and Functional Testing for E-Commerce Sites

## Objective
This project aims to automate crawling and testing a sample e-commerce website (e.g., Amazon India) using Selenium. The script will focus on extracting product details from product pages and verifying specific elements on the website.

## Limitations
CAPTCHA challenges may prevent automation of certain actions. These cannot be bypassed within this script.

## Project Structure
```markdown
Reports/
  ├── 2025_01_30/
      ├── 30_01_2025_15_06_27_271530012025.png
      ├── report_150614.html
configs/
  ├── configs.py
page_objects/
  ├── __init__.py
  ├── home_page.py
  ├── product_detailed_page.py
  ├── search_result_page.py
test_cases/
  ├── __init__.py
  ├── conftest.py
  ├── test_basic_crawling.py
  ├── test_functional_testing.py
test_data/
  └── product_info.csv
utilities/
  ├── __init__.py
  └── utilities.py
README.md
install_package.bat
requirements.txt
run.bat
```
## Features
### **Basic Crawling**
1. Automate the process of opening the homepage.
2. Search for a product
3. Extract the following details from the search results:
- Product Name
- Price
- Ratings
- URL

### **Functional Testing**
1. Automate the process of opening the homepage.
2. Search for a product
3. Validate the following elements on the product page:
- Presence of "Add to Cart" button.
- Product details section (e.g., description, specifications).
- Image gallery.

### **Reporting**
1. Store the extracted product information in a CSV file.
2. Log test results (pass/fail) for each validation via pytest html report

### **Additional**
1. Crawl multiple pages of search results (part of Basic Crawling, Step 3).
2. Test website responsiveness by simulating different screen sizes:
- "desktop": 1920 x 1080
- "tablet": 768 x 1024
- "mobile": 375 x 667
3. Parallel Execution using pytest-xdist

## Prerequisites
* Python 3.8+
* Required Python Libraries listed in requirements.txt
* Pip
* Google Chrome or any other supported browser

## Tools and Frameworks Used
* Selenium: For automating the web crawling and functional testing.
* pytest: For running the tests.
* CSV: For storing extracted product details.
* pytest-xdist: Parallel Execution

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
pytest

# Parallel Execution
pytest -n=3
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

[Watch Test Execution on YouTube](https://youtu.be/f8BHg7vmhxI)