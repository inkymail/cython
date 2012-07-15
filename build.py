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
import sys
import time
import subprocess
from multiprocessing import cpu_count

def mkdirs(pathname):
    (head, tail) = os.path.split(pathname)
    try:
        # Make sure the path exists
        os.makedirs(head)
    except:
        pass

def run(*args, **kw):
    ignore_errors = kw.get('ignore_errors', False)
    env = {}
    env.update(os.environ)
    if 'env' in kw:
        env.update(kw['env'])

    print "build.py: running command '%s'" % " ".join(args)
    process = subprocess.Popen(args, shell=False, env=env)
    while True:
        process.poll()
        if process.returncode == 0:
            break
        if process.returncode is not None:
            if ignore_errors:
                break
            print "returncode = %s" % process.returncode
            exit(process.returncode)
        time.sleep(0.25)

if __name__ == '__main__':
    arcode_root = subprocess.Popen(["arcode", "-r"], stdout=subprocess.PIPE).communicate()[0].strip()
    platform = subprocess.Popen(["arcode", "-P"], stdout=subprocess.PIPE).communicate()[0].strip()
    env = {}

    if platform == 'osx':
        # This must be set to the lowest OS X version we want to support.
        env.update({ 'MACOSX_DEPLOYMENT_TARGET': '10.6' })

        #
        # We generally want a pure i386 binary for OS X, since Python memory usage is approximately
        # halved with a 32-bit binary and we get no real value out of the 64-bit build. The other
        # options are here for reference.
        #
        env.update({ 'CFLAGS': '-arch i386'})

    os.chdir('cython')

    run('python', './setup.py', 'build')

    print "***************************"
    print "*****    ARCODE NOTE  *****"
    print "***************************"
    print "Make sure you PATH includes %s/deps/thirdparty-cython/cython/bin" % arcode_root
    print "Make sure your PYTHONPATH includes %s/deps/thirdparty-cython/cython" % arcode_root
