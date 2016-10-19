#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IbPy - Interactive Brokers Python API

IbPy is a third-party implementation of the API used for accessing the
Interactive Brokers on-line trading system.  IbPy implements functionality
that the Python programmer can use to connect to IB, request stock ticker
data, submit orders for stocks and options, and more.
"""
import os
import re
from distutils.core import setup


classifiers = """Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Office/Business :: Financial
Topic :: Office/Business :: Financial :: Investment
Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules"""


doclines = __doc__.split('\n')

# Version Number
with open(os.path.join(os.path.dirname(__file__), 'ib', '__init__.py')) as f:
    version = re.compile(r".*__version__ = '(.*?)'", re.S).match(f.read()).group(1)


try:  # Python 3
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:  # Python 2
    from distutils.command.build_py import build_py

setup(
    cmdclass={'build_py': build_py},
    name='IbPy2',
    version=version,
    description=doclines[0],
    maintainer='Felix Zumstein',
    maintainer_email='felix.zumstein@zoomeranalytics.com',
    url='https://github.com/blampe/IbPy',
    license='BSD License',
    packages=['ib', 'ib/lib', 'ib/ext', 'ib/opt', 'ib/sym'],
    classifiers=classifiers.split('\n'),
    long_description='\n'.join(doclines[2:]),
    platforms=['any']
)
