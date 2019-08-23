# cython: boundscheck=False
# cython: wraparound=False
# cython: nonecheck=False
# cython: profile=False
# cython: overflowcheck=False
# cython: initializedcheck=False
# cython: language=3
from cython.parallel import prange
from libc.stdio cimport printf
from libc.stdlib cimport rand, RAND_MAX
cimport numpy as np
import numpy as np
import random
cimport cython
import struct

cdef enum:
	w = 1+10000
	h = 1+10000
	wn = w-1
	hn = h-1

#1.15ms frametime @ 1920*1080
cpdef void iterate_multithread(np.uint8_t [:, :, ::1] b_, np.uint8_t flag):
	cdef Py_ssize_t i, j
	cdef int n

	#~0.15ms to 0.20ms to wrap
	b_[:,0,:]=b_[:,wn,:]
	b_[:,:,0]=b_[:,:,hn]
	b_[:,w,:]=b_[:,1,:]
	b_[:,:,h]=b_[:,:,1]

	if flag == 0:
		for i in prange(1, w, nogil=True, schedule='guided', num_threads=12, chunksize=3):
			for j in range(1, h):
				n = (b_[0, i-1, j-1] + b_[0, i-1, j] + b_[0, i-1, j+1] + b_[0, i, j-1] + b_[0, i, j+1] + b_[0, i+1, j-1] + b_[0, i+1, j] + b_[0, i+1, j+1])
				b_[1, i, j] = b_[0, i, j] if n==2 else (1 if n==3 else 0)
	else:
		for i in prange(1, w, nogil=True, schedule='guided', num_threads=12, chunksize=3):
			for j in range(1, h):
				n = (b_[1, i-1, j-1] + b_[1, i-1, j] + b_[1, i-1, j+1] + b_[1, i, j-1] + b_[1, i, j+1] + b_[1, i+1, j-1] + b_[1, i+1, j] + b_[1, i+1, j+1])
				b_[0, i, j] = b_[1, i, j] if n==2 else (1 if n==3 else 0)

#3.15ms frametime @ 1920*1080
cpdef void iterate_singlethread(np.uint8_t [:, :, ::1] b_, np.uint8_t flag):
	cdef Py_ssize_t i, j
	cdef int n

	#~0.15ms to 0.20ms to wrap
	b_[:,0,:]=b_[:,wn,:]
	b_[:,:,0]=b_[:,:,hn]
	b_[:,w,:]=b_[:,1,:]
	b_[:,:,h]=b_[:,:,1]

	if flag == 0:
		for i in range(1, w):
			for j in range(1, h):
				n = (b_[0, i-1, j-1] + b_[0, i-1, j] + b_[0, i-1, j+1] + b_[0, i, j-1] + b_[0, i, j+1] + b_[0, i+1, j-1] + b_[0, i+1, j] + b_[0, i+1, j+1])
				b_[1, i, j] = b_[0, i, j] if n==2 else 1 if n==3 else 0
	else:
		for i in range(1, w):
			for j in range(1, h):
				n = (b_[1, i-1, j-1] + b_[1, i-1, j] + b_[1, i-1, j+1] + b_[1, i, j-1] + b_[1, i, j+1] + b_[1, i+1, j-1] + b_[1, i+1, j] + b_[1, i+1, j+1])
				#b_[0, i, j] = b_[1, i, j] if n==2 else 1 if n==3 else 0
				b_[0, i, j] = lut_[b_[0, i, j], n]

cpdef void iterate_pure(np.uint8_t [:, :, ::1] b_, int iterations):
	cdef Py_ssize_t i, j
	cdef int n
	cdef int iteration

	iterations /= 2
	for iteration in range(iterations):
		b_[:,0,:]=b_[:,wn,:]
		b_[:,:,0]=b_[:,:,hn]
		b_[:,w,:]=b_[:,1,:]
		b_[:,:,h]=b_[:,:,1]
		for i in prange(1, w, nogil=True, schedule='guided', num_threads=12):
			for j in range(1, h):
				n = (b_[0, i-1, j-1] + b_[0, i-1, j] + b_[0, i-1, j+1] + b_[0, i, j-1] + b_[0, i, j+1] + b_[0, i+1, j-1] + b_[0, i+1, j] + b_[0, i+1, j+1])
				b_[1, i, j] = b_[0, i, j] if n==2 else (1 if n==3 else 0)
		b_[:,0,:]=b_[:,wn,:]
		b_[:,:,0]=b_[:,:,hn]
		b_[:,w,:]=b_[:,1,:]
		b_[:,:,h]=b_[:,:,1]
		for i in prange(1, w, nogil=True, schedule='guided', num_threads=12):
			for j in range(1, h):
				n = (b_[1, i-1, j-1] + b_[1, i-1, j] + b_[1, i-1, j+1] + b_[1, i, j-1] + b_[1, i, j+1] + b_[1, i+1, j-1] + b_[1, i+1, j] + b_[1, i+1, j+1])
				b_[0, i, j] = b_[1, i, j] if n==2 else (1 if n==3 else 0)

cpdef void set_random(np.uint8_t [:, :, ::1] b_, float p):
	cdef Py_ssize_t i, j
	cdef int threshold = <int>(RAND_MAX * p)

	for i in prange(1, w, nogil=True, schedule='guided', num_threads=12):
		for j in range(1, h):
			b_[0, i, j] = 0 if (<int>rand() < threshold) else 1
			b_[1, i, j] = 0 if (<int>rand() < threshold) else 1