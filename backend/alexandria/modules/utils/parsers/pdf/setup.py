from __future__ import print_function

import sys
from distutils.core import setup, Extension

try:
    from Cython.Build import cythonize

except ImportError:
    print('You need to install cython first - sudo pip install cython', file=sys.stderr)
    sys.exit(1)

poppler_ext = Extension('poppler', ['poppler.pyx'], language='c++',
                        extra_compile_args=[],
                        include_dirs=[
                            "/usr/include/poppler",
                        ],
                        libraries=['poppler'])
setup(name='poppler',
      version='0.2',
      ext_modules=cythonize(poppler_ext))
