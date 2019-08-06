# cython: boundscheck=False
# cython: wraparound=False
# cython: nonecheck=False
from cython.parallel import parallel, prange
from libc.stdlib cimport abort, malloc, free
cimport numpy as np
cimport cython
cimport openmp
import numpy as np

ctypedef np.uint8_t int_8
cdef enum:
    w = 1+1920
    h = 1+1080

cpdef void iterate(int_8 [:, :, ::1] b_, int_8 flag) nogil:
    cdef Py_ssize_t i, j
    cdef int n

    if flag == 0:
        b_[1,:,:]=0
        for i in prange(1, w, nogil=True, schedule='static', num_threads = 4, chunksize=6):
            for j in range(1, h):
                n = b_[0, i-1, j-1] + b_[0, i-1, j] + b_[0, i-1, j+1] + b_[0, i, j-1] + b_[0, i, j+1] + b_[0, i+1, j-1] + b_[0, i+1, j] + b_[0, i+1, j+1]
                if n==2: b_[1, i, j] = b_[0, i, j]
                elif n==3: b_[1, i, j] = 1
    else:
        b_[0,:,:]=0
        for i in prange(1, w, nogil=True, schedule='static', num_threads = 4, chunksize=40):
            for j in range(1, h):
                n = b_[1, i-1, j-1] + b_[1, i-1, j] + b_[1, i-1, j+1] + b_[1, i, j-1] + b_[1, i, j+1] + b_[1, i+1, j-1] + b_[1, i+1, j] + b_[1, i+1, j+1]
                if n==2: b_[0, i, j] = b_[1, i, j]
                elif n==3: b_[0, i, j] = 1