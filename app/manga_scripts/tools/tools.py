import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from app.config.config import config


def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('-profile')
    options.add_argument(config.get('Settings', 'fier_fox_profile'))

    service = Service(log_path=os.path.devnull)
    return webdriver.Firefox(options=options, service=service)
