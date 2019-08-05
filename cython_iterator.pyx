from __future__ import print_function
import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef np.ndarray iterate(np.ndarray cy_board_o):
    cdef np.ndarray cy_board_n = np.zeros_like(cy_board_o)
    cdef int hmax = cy_board_o.shape[0]-1
    cdef int vmax = cy_board_o.shape[1]-1
    cdef unsigned char [:, :]  o_view = cy_board_o
    cdef unsigned char [:, :]  n_view = cy_board_n
    cdef int i, j, c
    for i in range(1, hmax):
        for j in range(1, vmax):
            c = o_view[i-1, j-1] + o_view[i-1, j] + o_view[i-1, j+1] + o_view[i, j-1] + o_view[i, j+1] + o_view[i+1, j-1] + o_view[i+1, j] + o_view[i+1, j+1]
            if (c == 3) :
                n_view[i, j] = 1
            elif (c == 2) :
                n_view[i, j] = o_view[i, j]
    return cy_board_n