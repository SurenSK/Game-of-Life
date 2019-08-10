# cython: boundscheck=False
# cython: wraparound=False
# cython: nonecheck=False
from cython.parallel import prange
from libc.stdio cimport printf
cimport numpy as np
import numpy as np
cimport cython
cimport openmp

cdef enum:
	w = 1+1920
	h = 1+1080

cpdef void iterate(np.uint8_t [:, :, ::1] b_, np.uint8_t flag) nogil:
	cdef Py_ssize_t i, j
	cdef int n

	if flag == 0:
		b_[1,:,:] = 0
		for i in prange(1, w, schedule='guided', num_threads=4):
			for j in range(1, h):
				n = b_[0, i-1, j-1] + b_[0, i-1, j] + b_[0, i-1, j+1] + b_[0, i, j-1] + b_[0, i, j+1] + b_[0, i+1, j-1] + b_[0, i+1, j] + b_[0, i+1, j+1]
				if n == 2: b_[1, i, j] = b_[0, i, j]
				elif n == 3: b_[1, i, j] = 1
	else:
		b_[0,:,:] = 0
		for i in prange(1, w, schedule='guided', num_threads=4):
			for j in range(1, h):
				n = b_[1, i-1, j-1] + b_[1, i-1, j] + b_[1, i-1, j+1] + b_[1, i, j-1] + b_[1, i, j+1] + b_[1, i+1, j-1] + b_[1, i+1, j] + b_[1, i+1, j+1]
				if n == 2: b_[0, i, j] = b_[1, i, j]
				elif n == 3: b_[0, i, j] = 1