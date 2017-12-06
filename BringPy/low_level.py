#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from . import Debug
from selenium import webdriver
import selenium.common.exceptions as seleniumExceptions
import os
import time


class Bring:
    def __init__(self):
        # initialize selenium
        self.driver = webdriver.Chrome(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver'))
        # open login page
        self.driver.get('https://web.getbring.com/login')
        # wait until the user has logged in
        while True:
            if 'https://web.getbring.com/app/lists/' in self.driver.current_url:
                break
            time.sleep(1)
