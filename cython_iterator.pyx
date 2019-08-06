cimport numpy as np
cimport cython
import numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
cpdef void iterate_v2(np.ndarray board, int c_frame_n):
    cdef unsigned char [:, :, ::1] b_ = board
    cdef unsigned char dst = (c_frame_n+1) % 2
    cdef unsigned char src = c_frame_n % 2
    cdef int h = board.shape[1]-1
    cdef int v = board.shape[2]-1
    cdef int i, j, n
    b_[dst,:,:]=0
    for i in range(1, h):
        for j in range(1, v):
            n = b_[src, i-1, j-1] + b_[src, i-1, j] + b_[src, i-1, j+1] + b_[src, i, j-1] + b_[src, i, j+1] + b_[src, i+1, j-1] + b_[src, i+1, j] + b_[src, i+1, j+1]
            if n==3: b_[dst, i, j] = 1
            elif n==2: b_[dst, i, j] = b_[src, i, j]