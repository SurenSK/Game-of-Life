# cython: boundscheck=False
# cython: wraparound=False
# cython: nonecheck=False
cimport numpy as np
cimport cython
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
        for i in range(1, w):
            for j in range(1, h):
                n = b_[0, i-1, j-1] + b_[0, i-1, j] + b_[0, i-1, j+1] + b_[0, i, j-1] + b_[0, i, j+1] + b_[0, i+1, j-1] + b_[0, i+1, j] + b_[0, i+1, j+1]
                if n==2: b_[1, i, j] = b_[0, i, j]
                elif n==3: b_[1, i, j] = 1
    else:
        b_[0,:,:]=0
        for i in range(1, w):
            for j in range(1, h):
                n = b_[1, i-1, j-1] + b_[1, i-1, j] + b_[1, i-1, j+1] + b_[1, i, j-1] + b_[1, i, j+1] + b_[1, i+1, j-1] + b_[1, i+1, j] + b_[1, i+1, j+1]
                if n==2: b_[0, i, j] = b_[1, i, j]
                elif n==3: b_[0, i, j] = 1