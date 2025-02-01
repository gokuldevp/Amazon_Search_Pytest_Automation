import random
import logging
import datetime
import os

def get_current_date_time():
    """ Function to return datetime int YYMMDDHHmmSS format """
    current_datetime = str(datetime.datetime.now())[0:19]
    return datetime.datetime.strptime(current_datetime, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')

def get_current_date():
    """ Function to return datetime int YYMMDDHHmmSS format """
    current_date = str(datetime.date.today().strftime("%Y_%m_%d"))
    return current_date

def loggen(): 
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__).replace('utilities'+ os.sep, '')), 'logs', 'automation.log') 
    log_handler = logging.FileHandler(log_file) 
    log_handler.setFormatter( logging.Formatter("%(asctime)s: %(levelname)s: %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")) 
    logger = logging.getLogger() 
    logger.addHandler(log_handler) 
    logger.setLevel(logging.INFO) 
    return logger

class ScreeShots:
    def __init__(self, driver):
        self.driver = driver
    def take_screenshots_as_png(self,screenshot_name):
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__).replace('utilities'+ os.sep, '')),'Reports'+ os.sep,datetime.date.today().strftime("%Y_%m_%d"))
        
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        
        screenshot_name = "" + datetime.datetime.strptime(get_current_date_time(), '%Y%m%d%H%M%S').strftime('%d_%m_%Y_%H_%M_%S') + f"_{screenshot_name}" + ".png"
        screenshot_file = os.path.join(dir_path, screenshot_name)
        
        self.driver.save_screenshot(screenshot_file)

        # re_path = screenshot_file.replace(os.path.dirname(os.path.abspath(__file__).replace('utilities'+ os.sep, '')),"")
        return screenshot_name
