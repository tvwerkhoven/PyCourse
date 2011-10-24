#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
@file py-example1-11.py
@brief First set of example for Python 102 lecture
@author Tim van Werkhoven (t.i.m.vanwerkhoven@xs4all.nl)
@date 20111012

Examples taken from http://wiki.python.org/moin/SimplePrograms

Created by Tim van Werkhoven (t.i.m.vanwerkhoven@xs4all.nl) on 2011-10-12
Copyright (c) 2011 Tim van Werkhoven. All rights reserved.

This file is licensed under the Creative Commons Attribution-Share Alike
license versions 3.0 or higher, see
http://creativecommons.org/licenses/by-sa/3.0/
"""

print "--- Example 11 lines: Triple-quoted strings, while loop "

REFRAIN = '''
%d bottles of beer on the wall,
%d bottles of beer,
take one down, pass it around,
%d bottles of beer on the wall!
'''
bottles_of_beer = 99
while bottles_of_beer > 1:
    print REFRAIN % (bottles_of_beer, bottles_of_beer,
        bottles_of_beer - 1)
    bottles_of_beer -= 1
