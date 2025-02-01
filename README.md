# Automated Web Crawling and Functional Testing for E-Commerce Sites

## Objective
This project aims to automate crawling and testing a sample e-commerce website (e.g., Amazon India) using Selenium. The script will focus on extracting product details from product pages and verifying specific elements on the website.

## Limitations
1. **CAPTCHA Challenges**
* **Description**: CAPTCHA challenges are designed to distinguish between human users and automated scripts. They can significantly hinder the automation of certain actions.
* **Workaround**: Refreshing the page might help bypass a CAPTCHA in some cases, especially if it is triggered by temporary high traffic or session-related issues. However, this is not a guaranteed solution and may not be effective in all scenarios.
* **Note**: Manual intervention may be required to solve CAPTCHAs, particularly for those that are persistent.
2. **High Traffic Errors**
* **Description**: High traffic or server load can result in errors while page inaccessibility, as seen in the "Oops! It's rush hour and traffic is piling up on that page" message from Amazon.in.
* Note: This issue is challenging to handle entirely through an automation script

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

## **Features**  

### **1. Basic Crawling**  
- Automates the process of opening the homepage.  
- Searches for a product.  
- Extracts product details from search results, including:  
  - **Product Name**  
  - **Price**  
  - **Ratings**  
  - **URL**  

### **2. Functional Testing**  
- Validates key elements on the product page:  
  - **Presence of "Add to Cart" button**  
  - **Product details section** (e.g., description, specifications)  
  - **Image gallery**  

### **3. Reporting**  
- Stores extracted product information in a **CSV file**.  
- Logs test results (pass/fail) in a **pytest HTML report**.  

### **4. Additional Features**  
- Crawls multiple pages of search results (**part of Basic Crawling, Step 3**).  
- Tests website responsiveness by simulating different screen sizes:  
  - **Desktop:** 1920 × 1080  
  - **Tablet:** 768 × 1024  
  - **Mobile:** 375 × 667  
- Supports **parallel test execution** using **pytest-xdist**.

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

[Watch Test Execution on YouTube](https://youtu.be/x2gSy37OCPg)