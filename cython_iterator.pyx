# cython: boundscheck=False
# cython: wraparound=False
# cython: nonecheck=False
# cython: profile=True
from cython.parallel import prange
from libc.stdio cimport printf
from cpython cimport array
import array
from libc.string cimport memset
cimport numpy as np
import numpy as np
cimport cython
cimport openmp
import pygame

cdef enum:
	w = 1+1920
	h = 1+1080
	wn = w-1
	hn = h-1

cpdef void iterate(np.uint8_t [:, :, ::1] b_, np.uint8_t flag):
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
				b_[1, i, j] = b_[0, i, j] if n==2 else 1 if n==3 else 0
	else:
		for i in prange(1, w, nogil=True, schedule='guided', num_threads=12, chunksize=3):
			for j in range(1, h):
				n = (b_[1, i-1, j-1] + b_[1, i-1, j] + b_[1, i-1, j+1] + b_[1, i, j-1] + b_[1, i, j+1] + b_[1, i+1, j-1] + b_[1, i+1, j] + b_[1, i+1, j+1])
				b_[0, i, j] = b_[1, i, j] if n==2 else 1 if n==3 else 0