import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
cpdef void iterate(np.ndarray cur_board, np.ndarray new_board):
    cdef unsigned char [:, ::1] c_ = cur_board
    cdef unsigned char [:, ::1] n_ = new_board
    cdef int hmax = cur_board.shape[0]-1
    cdef int vmax = cur_board.shape[1]-1
    cdef int i, j, c

    n_[:] = 0

    for i in range(1, hmax):
        for j in range(1, vmax):
            c = c_[i-1, j-1] + c_[i-1, j] + c_[i-1, j+1] + c_[i, j-1] + c_[i, j+1] + c_[i+1, j-1] + c_[i+1, j] + c_[i+1, j+1]
            if (c == 3) : n_[i, j] = 1
            elif (c == 2) : n_[i, j] = c_[i, j]
    c_[:] = n_