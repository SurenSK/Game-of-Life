from distutils.core import setup
from Cython.Build import cythonize
import timeit
import numpy as np

ext_options = {"compiler_directives": {"profile": True}, "annotate": True}
setup(
    ext_modules = cythonize("cython_iterator.pyx", **ext_options),
    include_dirs=[np.get_include()]
)