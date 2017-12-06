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
        self.clickThisByXPath('//*[@id="cdk-overlay-0"]/md-dialog-container/intro-screen-host/div/div/button', waitUntilAvaible=True)
        self.clickThisByXPath('//*[@id="cdk-overlay-0"]/md-dialog-container/intro-screen-host/div/bring-intro-push/div/div[2]/button[1]', waitUntilAvaible=True)

    def clickThisByXPath(self, xpath, waitUntilAvaible=False):
        if waitUntilAvaible:
            found = False
            while not found:
                try:
                    self.clickThisByXPath(xpath)
                    found = True
                except seleniumExceptions.NoSuchElementException:
                    pass
            return
        self.driver.find_element_by_xpath(xpath).click()

    def getShoppingLists(self):
        shoppingLists = []
        for l in self.driver.find_elements_by_class_name('bring-list-selector-entry'):
            data = {}
            data['name'] = l.find_element_by_class_name('bring-list-selector-list-name').text
            data['count'] = int(l.find_element_by_class_name('bring-list-selector-list-item-count').text)
            classes = l.find_element_by_class_name('bring-list-selector-list-name').get_attribute('class')
            if 'selected' in classes:
                data['active'] = True
            else:
                data['active'] = False
            shoppingLists.append(data)
        return(shoppingLists)

    def openShoppingList(self, index):
        self.driver.find_elements_by_class_name('bring-list-selector-entry')[index].click()
