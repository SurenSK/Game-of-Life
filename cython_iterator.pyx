from __future__ import print_function
import numpy as np
cimport numpy as np
cimport cython

DTYPE = np.int
ctypedef np.int_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
def iterate(np.ndarray cy_board_o, np.ndarray cy_board_n):
    cdef int hmax = cy_board_n.shape[0]-1
    cdef int vmax = cy_board_n.shape[1]-1
    cdef int [:, :]  o_view = cy_board_o
    cdef int [:, :]  n_view = cy_board_n
    cdef int i, j, c
    for i in range(1, hmax):
        for j in range(1, vmax):
            c = o_view[i-1, j-1] + o_view[i-1, j] + o_view[i-1, j+1] + o_view[i, j-1] + o_view[i, j+1] + o_view[i+1, j-1] + o_view[i+1, j] + o_view[i+1, j+1]
            if (c == 3) :
                n_view[i, j] = 1
            elif (c == 2) :
                n_view[i, j] = o_view[i, j]
            else :
                n_view[i, j] = 0
    return cy_board_n