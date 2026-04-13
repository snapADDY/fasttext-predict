#!/usr/bin/env python

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

import sys
import os
import sysconfig

from pybind11.setup_helpers import Pybind11Extension, ParallelCompile
from setuptools import setup

ParallelCompile().install()

__version__ = '0.9.2.4'
FASTTEXT_SRC = "src"

WIN = sys.platform.startswith("win32") and "mingw" not in sysconfig.get_platform()

fasttext_src_files = map(str, os.listdir(FASTTEXT_SRC))
fasttext_src_cc = list(filter(lambda x: x.endswith('.cc'), fasttext_src_files))

fasttext_src_cc = list(
    map(lambda x: str(os.path.join(FASTTEXT_SRC, x)), fasttext_src_cc)
)

extra_compile_args = []
if WIN:
    extra_compile_args.append('/DVERSION_INFO=\\"%s\\"' % __version__)
else:
    extra_compile_args.append('-DVERSION_INFO="%s"' % __version__)
    extra_compile_args.extend(["-O3", "-flto"])

setup(
    packages=[
        'fasttext',
    ],
    package_dir={
        '': 'python/fasttext_module'
    },
    zip_safe=False,
    ext_modules=[
        Pybind11Extension(
            "fasttext_pybind",
            ["python/fasttext_module/fasttext/pybind/fasttext_pybind.cc"] + fasttext_src_cc,
            include_dirs=[
                FASTTEXT_SRC,
            ],
            cxx_std=17,
            extra_compile_args=extra_compile_args,
        )
    ],
)
