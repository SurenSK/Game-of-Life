from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy as np

#python setup.py build_ext --inplace

#setup(
#    ext_modules = cythonize("cython_iterator.pyx"),
#    include_dirs=[np.get_include()]
#)

ext_modules = [
    Extension(
        "cython_iterator",
        ["cython_iterator.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
    )
]

setup(
    name='parallel-game-of-life',
    include_dirs=[np.get_include()],
    ext_modules=cythonize(ext_modules)
)