#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
@file python102-answer-palindrome.py
@brief Finding palindroms with Python
@author Tim van Werkhoven (t.i.m.vanwerkhoven@gmail.com)
@date 20111101
@url python101.vanwerkhoven.org

From <http://projecteuler.net/problem=4>:

A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit numbers.

This file is licensed under the Creative Commons Attribution-Share Alike
license versions 3.0 or higher, see
http://creativecommons.org/licenses/by-sa/3.0/
"""

# Import some packages
import sys, os

def main():
	# Generate all pairs of 3-digit palindroms. Let p1 run from 999 down to 100, and for each p1, let p2 run from the current value of p1 to 100. Given a pair <p1>, <p2>, check if they form a palindrome by converting <p1>*<p2> to string and comparing itself with the the reversed string. If this is true, we store the palindrome factors. The result is a list of all palindromes, such that we can easily check the maximum number afterwards.
	# This approach has speed O(N*log(N)) (?) and uses O(N) memory.
	palinlist = [(p1,p2,p1*p2) \
		for p1 in xrange(999,99,-1) \
			for p2 in xrange(p1,99,-1) \
				if str(p1*p2) == str(p1*p2)[::-1]]
	
	# This loop does the same as above, but stops when the largest palindrome has been found. <palin> is the current largest palindrome, <palinf> are the two 3-digit factors of <palin>.
	# Also here we let <p1> run from 999 to 100 and <p2> from <p1> to 100, and we check if <p1>*<p2> is a palindrome for all pairs. If this is the case, we check if this palindrome is larger than the current largest, and if so we store it in <palin> and the factors in <palinf>. If not, we do nothing. 
	# We let this run until <p1>*<p1> is smaller than the current largest palindrome, <palin>. If this is the case, we will not find a palindrome larger than <palin> anymore because <p2> is always equal or less than <p1>, such that subsequent <p1>*<p2> values will never exceed <palin>.
	# Finally, we print the palindrome value and its 3-digit factors.
	# This approach has speed O(N*log(N)) (?) and uses O(1) memory.
	palin=0;palinf=(0,0)
	for p1 in xrange(999,99,-1):
		if (p1*p1 < palin):
			break
		for p2 in xrange(p1,99,-1):
			if str(p1*p2) == str(p1*p2)[::-1]:
				if (p1*p2 > palin):
					palin = p1*p2
					palinf = (p1,p2)
	print palinf, palin

# Execute main() if this is run from the command line
if __name__ == "__main__":
	sys.exit(main())
