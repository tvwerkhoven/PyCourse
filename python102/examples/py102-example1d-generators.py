#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
@file py102-example1d-generators.py
@brief First set of example for Python 102 lecture
@author Tim van Werkhoven (t.i.m.vanwerkhoven@gmail.com)
@url http://python101.vanwerkhoven.org
@date 20111012

Created by Tim van Werkhoven (t.i.m.vanwerkhoven@xs4all.nl) on 2011-10-12
Copyright (c) 2011 Tim van Werkhoven. All rights reserved.

This file is licensed under the Creative Commons Attribution-Share Alike
license versions 3.0 or higher, see
http://creativecommons.org/licenses/by-sa/3.0/
"""

print "--- Example generators"

def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib_gen = fib()
[fib_gen.next() for i in xrange(20)]
