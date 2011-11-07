#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
@file py102-example2-zernike.py
@brief Fitting a surface in Python example for Python 102 lecture
@author Tim van Werkhoven (t.i.m.vanwerkhoven@gmail.com)
@url http://python101.vanwerkhoven.org
@date 20111012

Created by Tim van Werkhoven (t.i.m.vanwerkhoven@xs4all.nl) on 2011-10-12
Copyright (c) 2011 Tim van Werkhoven. All rights reserved.

This file is licensed under the Creative Commons Attribution-Share Alike
license versions 3.0 or higher, see
http://creativecommons.org/licenses/by-sa/3.0/
"""

### Libraries

import pyfits
import numpy as N
from scipy.misc import factorial as fac

### Init functions
def zernike_rad(m, n, rho):
	"""
	Calculate the radial component of Zernike polynomial (m, n) 
	given a grid of radial coordinates rho.
	
	>>> zernike_rad(3, 3, 0.333)
	0.036926037000000009
	>>> zernike_rad(1, 3, 0.333)
	-0.55522188900000002
	>>> zernike_rad(3, 5, 0.12345)
	-0.007382104685237683
	"""
	
	if (n < 0 or m < 0 or abs(m) > n):
		raise ValueError
	
	if ((n-m) % 2):
		return rho*0.0
	
	pre_fac = lambda k: (-1.0)**k * fac(n-k) / ( fac(k) * fac( (n+m)/2.0 - k ) * fac( (n-m)/2.0 - k ) )
	
	return sum(pre_fac(k) * rho**(n-2.0*k) for k in xrange((n-m)/2+1))

def zernike(m, n, rho, phi):
	"""
	Calculate Zernike polynomial (m, n) given a grid of radial
	coordinates rho and azimuthal coordinates phi.
	
	>>> zernike(3,5, 0.12345, 1.0)
	0.0073082282475042991
	>>> zernike(1, 3, 0.333, 5.0)
	-0.15749545445076085
	"""
	if (m > 0): return zernike_rad(m, n, rho) * N.cos(m * phi)
	if (m < 0): return zernike_rad(-m, n, rho) * N.sin(-m * phi)
	return zernike_rad(0, n, rho)

def zernikel(j, rho, phi):
	"""
	Calculate Zernike polynomial with Noll coordinate j given a grid of radial
	coordinates rho and azimuthal coordinates phi.
	
	>>> zernikel(0, 0.12345, 0.231)
	1.0
	>>> zernikel(1, 0.12345, 0.231)
	0.028264010304937772
	>>> zernikel(6, 0.12345, 0.231)
	0.0012019069816780774
	"""
	n = 0
	while (j > n):
		n += 1
		j -= n
	
	m = -n+2*j
	return zernike(m, n, rho, phi)

### Generate Zernike polynomials

# Make coordinate grid for rho and phi

grid = (N.indices((256, 256), dtype=N.float) - 128) / 128.0
grid_rho = (grid**2.0).sum(0)**0.5
grid_phi = N.arctan2(grid[0], grid[1])
grid_mask = grid_rho <= 1

# Compute list of explicit Zernike polynomials

zern_list = [zernikel(i, grid_rho, grid_phi)*grid_mask for i in xrange(25)]

### Generate test surface

test_vec = N.random.random(25)
test_surf = 0
for (i, val) in enumerate(test_vec):
	test_surf += val * zernikel(i, grid_rho, grid_phi)

### Try to reconstruct test surface

# Calculate covariance between all Zernike polynomials
cov_mat = N.array([[N.sum(zerni * zernj) for zerni in zern_list] for zernj in zern_list])

# Invert covariance matrix using SVD
cov_mat_in = N.linalg.pinv(cov_mat)

# Calculate the inner product of each Zernike mode with the test surface

wf_zern_inprod = N.array([N.sum(test_surf * zerni) for zerni in zern_list])

# Given the inner product vector of the test wavefront with Zernike basis,
# calculate the Zernike polynomial coefficients

rec_wf_pow = N.dot(cov_mat_in, wf_zern_inprod)

# Reconstruct surface from Zernike components
rec_wf = 0
for (i, val) in enumerate(rec_wf_pow):
	rec_wf += val * zernikel(i, grid_rho, grid_phi)

# Test reconstruct
print test_vec-rec_wf_pow
print N.allclose(test_vec, rec_wf_pow)
print N.allclose(test_surf, rec_wf)

### Plot some results

fig = plt.figure(1)
ax = fig.add_subplot(111)

ax.set_xlabel('Zernike mode')
ax.set_ylabel('Power [AU]')
ax.set_title('Reconstruction quality')

ax.plot(test_vec, 'r-', label='Input')
ax.plot(rec_wf_pow, 'b--', label='Recovered')
ax.legend()
fig.show()
fig.savefig('py-example2-plot1.pdf')

plt.imshow(surf)

fig = plt.figure(1)
fig.clf()
ax = fig.add_subplot(111)
surf_pl = ax.imshow(test_surf*grid_mask, interpolation='nearest')
fig.colorbar(surf_pl)
fig.show()
fig.savefig('py-example2-plot2.pdf')
