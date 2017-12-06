#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from . import Debug
from .low_level import Bring


class BringPy(Bring):
    # user-friendly abstraction of class Bring
    def __init__(self):
        Bring.__init__(self)

    def openShoppingList(self, name):
        # open shopping list by name
        index = -1
        # loop through avaible list names to find list index
        for i, l in enumerate(self.getShoppingLists()):
            if l['name'] == name:
                index = i
                break
        # exit if name not found
        if index == -1:
            raise KeyError
        # open shopping list
        Bring.openShoppingList(self, index)
