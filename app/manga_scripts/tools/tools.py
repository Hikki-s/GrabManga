import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


def get_driver():
    options = Options()
    options.add_argument('--headless')
    service = Service(log_path=os.path.devnull)
    return webdriver.Firefox(options=options, service=service)
