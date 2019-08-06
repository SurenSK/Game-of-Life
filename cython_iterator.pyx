import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
cpdef void iterate(np.ndarray cy_board_o, np.ndarray cy_board_n):
    cdef unsigned char [:, ::1] o_view = cy_board_o
    cdef unsigned char [:, ::1] n_view = cy_board_n
    cdef int hmax = cy_board_o.shape[0]-1
    cdef int vmax = cy_board_o.shape[1]-1
    cdef int i, j, c

    n_view[:] = 0

    for i in range(1, hmax):
        for j in range(1, vmax):
            c = o_view[i-1, j-1] + o_view[i-1, j] + o_view[i-1, j+1] + o_view[i, j-1] + o_view[i, j+1] + o_view[i+1, j-1] + o_view[i+1, j] + o_view[i+1, j+1]
            if (c == 3) : n_view[i, j] = 1
            elif (c == 2) : n_view[i, j] = o_view[i, j]
    o_view[:] = n_view