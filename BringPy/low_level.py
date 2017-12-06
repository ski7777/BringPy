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
        # click on first found element by xpath
        # check whether we should wiáit until the element is avaiable
        if waitUntilAvaible:
            # wait until avaible
            found = False
            while not found:
                try:
                    # click it
                    self.clickThisByXPath(xpath)
                    found = True
                except seleniumExceptions.NoSuchElementException:
                    pass
            return
        # click it
        self.driver.find_element_by_xpath(xpath).click()

    def getShoppingLists(self):
        # get all shopping lists and to-purchase counts
        shoppingLists = []
        # loop through all lists
        for l in self.driver.find_elements_by_class_name('bring-list-selector-entry'):
            data = {}
            # get name and count of list
            data['name'] = l.find_element_by_class_name('bring-list-selector-list-name').text
            data['count'] = int(l.find_element_by_class_name('bring-list-selector-list-item-count').text)
            # get list classes to determine whether this is the active list
            classes = l.find_element_by_class_name('bring-list-selector-list-name').get_attribute('class')
            if 'selected' in classes:
                data['active'] = True
            else:
                data['active'] = False
            shoppingLists.append(data)
        return(shoppingLists)

    def openShoppingList(self, index):
        # open shopping list by list index
        # check the index right before calling this command! (And maybe after)
        self.driver.find_elements_by_class_name('bring-list-selector-entry')[index].click()

    def getShoppingListItems(self):
        # get all to purcahse items on active shopping list
        rawList = self.driver.find_element_by_class_name('bring-list-item-container-to-purchase').find_elements_by_class_name('bring-list-item-content')
        items = {}
        # loop through the items
        for e in rawList:
            # get the name
            name = e.find_element_by_class_name('bring-list-item-name').text
            items[name] = {}
            # get description label classes to determine whether description label is avaible
            descriptionLabel = e.find_element_by_class_name('bring-list-item-specification-label')
            if 'empty' not in descriptionLabel.get_attribute('class'):
                items[name]['description'] = descriptionLabel.text
            items[name]['to-purchase'] = True
        return(items)

    def clearSearchBar(self):
        # clear the search bar
        try:
            self.driver.find_element_by_class_name('bring-list-search-bar-clear').click()
        except seleniumExceptions.NoSuchElementException:
            pass

    def typeInSearchBar(self, text):
        # type text in search SearchBar
        # clear search bar
        self.clearSearchBar()
        SearchBar = self.driver.find_element_by_class_name('bring-list-search-bar-input')
        SearchBar.send_keys(text)

    def searchItems(self, text):
        # search for items
        # type into search bar
        self.typeInSearchBar(text)
        # wait for processing
        time.sleep(0.1)
        rawList = self.driver.find_element_by_tag_name('bring-item-search-result').find_elements_by_class_name('bring-list-item-content')
        items = {}
        # loop through the items
        for e in rawList:
            # get item
            name = e.find_element_by_class_name('bring-list-item-name').text
            items[name] = {}
            # get item label classes to determine whether it is to purchase
            if 'not-selected' in e.get_attribute('class'):
                items[name]['to-purchase'] = False
            else:
                items[name]['to-purchase'] = True
        return(items)
