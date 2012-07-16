#!/usr/bin/env python
# -*- mode: Python; fill-column: 100; -*-
#
# Simple script to build cython, setting various args for Arcode.
#
# This deals with platform-specific nonsense (e.g., building i386 on an x86_64 Mac).
#
# dmb - July 2012 - Copyright (C) 2012 Arcode Corporation
#
import os
from build_utils import *

if __name__ == '__main__':
    # Parse command line args
    results = make_arg_parser_and_parse("build Cython")

    chdir('cython')
    run('python', './setup.py', 'clean')
    run('python', './setup.py', 'build')

    print "**************************"
    print "*****  NOTE YE WELL  *****"
    print "**************************"
    print "Make sure you PATH includes %s/deps/thirdparty-cython/cython/bin" % get_root()
    print "Make sure your PYTHONPATH includes %s/deps/thirdparty-cython/cython" % get_root()
