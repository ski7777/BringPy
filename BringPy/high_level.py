#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from . import Debug
from .low_level import Bring


class BringPy(Bring):
    # user-friendly abstraction of class Bring
    def __init__(self):
        Bring.__init__(self)

