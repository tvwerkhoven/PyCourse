#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
@file python102-answer-mkflat.py -- average or sum several images, and store the result to disk
@author Tim van Werkhoven (t.i.m.vanwerkhoven@gmail.com)
@date 20110920
@copyright Copyright (c) 2011 Tim van Werkhoven

Given a series of input images, make a single flatfield image. Can also be 
used to make darkfields.

This file is licensed under the Creative Commons Attribution-Share Alike
license versions 3.0 or higher, see
http://creativecommons.org/licenses/by-sa/3.0/
"""

# Import libs
import numpy as N
import pyfits
import pylab as plt
import matplotlib
from time import time, localtime, gmtime, asctime
import argparse
import sys

# Color maps
# Deviation around zero colormap (blue--red)
cols = []
for x in N.linspace(0,1, 256):
	rcol = 0.237 - 2.13*x + 26.92*x**2 - 65.5*x**3 + 63.5*x**4 - 22.36*x**5
	gcol = ((0.572 + 1.524*x - 1.811*x**2)/(1 - 0.291*x + 0.1574*x**2))**2
	bcol = 1/(1.579 - 4.03*x + 12.92*x**2 - 31.4*x**3 + 48.6*x**4 - 23.36*x**5)
	cols.append((rcol, gcol, bcol))

cm_plusmin = matplotlib.colors.LinearSegmentedColormap.from_list("PaulT_plusmin", cols)

# Define some contants
AUTHOR = "Tim van Werkhoven (t.i.m.vanwerkhoven@gmail.com)"
DATE = "20110920"

def main():
	## Parse arguments check options
	(parser, args) = parsopts()
	
	# Print some debug output
	print "Running program %s on %d files" % (sys.argv[0], len(args.files))
	print args
	
	### Run program now.
	
	# Define read function depending on datatype
	read_func = plt.imread
	if (args.dtype == 'fits'):
		read_func = pyfits.getdata
	
	# Sum all data
	flatfield = sum(read_func(path) for path in args.files)
	
	# Divide by number of files if average is requested
	if (args.avg):
		flatfield /= len(args.files)
	
	# Make FITS header with metadata
	clist = pyfits.CardList()
	clist.append(pyfits.Card('Program', 'python102-answer-mkflat.py') )
	clist.append(pyfits.Card('Epoch', time()) )
	clist.append(pyfits.Card('utctime', asctime(gmtime(time()))) )
	clist.append(pyfits.Card('loctime', asctime(localtime(time()))) )
	clist.append(pyfits.Card('Desc', args.desc) )
	hdr = pyfits.Header(cards=clist)
	
	# Write output to disk
	pyfits.writeto('calib_frame_%s.fits' % (args.desc), flatfield, clobber=True, checksum=True, header=hdr)
	
	if (args.plot):
		# Make nice human-readable plot
		plt.clf()
		plt.title("Calibration frame %s (avg=%d)" % (args.desc, args.avg))
		plt.xlabel('X [pix]')
		plt.ylabel('Y [pix]')
		plt.imshow(flatfield, interpolation='nearest', cmap=plt.get_cmap(cm_plusmin), aspect='equal')
		plt.colorbar()
		plt.savefig('calib_frame_%s.pdf' % (args.desc))
	### END


def parsopts():
	"""Parse program options, check sanity and return results"""
	parser = argparse.ArgumentParser(description='Given a series of input frames, calculate the average or sum of these (e.g. a flat/darkfield). Store the result to disk as fits file and optionally as pretty 2D plot.', epilog='Comments & bugreports to %s' % (AUTHOR))
	
	parser.add_argument('files', metavar='F', type=str, nargs='+',
						help='files to average or sum.')
	
	parser.add_argument('--avg', dest='avg',
						action='store_true', default=False,
						help='average result (sum)')
	
	parser.add_argument('--plot', dest='plot',
						action='store_true', default=True,
						help='beside storing as fits file, also plot results (true)')
	
	parser.add_argument('--description', type=str, dest='desc',
						action='store', default='auto',
						help='Description for output file [text]')
	
	parser.add_argument('--type', dest='dtype', choices=(['png', 'fits']),
						action='store', default='png',
						help='input datatype (png)')
	
	parser.add_argument('-v', dest='debug', action='append_const', const=1,
						help='increase verbosity')
	parser.add_argument('-q', dest='debug', action='append_const', const=-1,
						help='decrease verbosity')
	parser.add_argument('--version', action='version', version='%(prog)s 0.1')
	
	args = parser.parse_args()
	
 	# Check & fix some options
	checkopts(parser, args)
	
	# Return results
	return (parser, args)

def checkopts(parser, args):
	"""Check program options sanity (nothing to do here)"""
	return

if __name__ == "__main__":
	sys.exit(main())
