#!/usr/bin/env python
# This program adds up integers in the command line

"""
@file py-example1-8.py
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

import sys
try:
    total = sum(int(arg) for arg in sys.argv[1:])
    print 'sum =', total
except ValueError:
    print 'Please supply integer arguments'
