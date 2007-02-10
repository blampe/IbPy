#!/usr/bin/env python
"""IbPy: Interactive Brokers Python API

IbPy is a third-party implementation of the API used for accessing the
Interactive Brokers on-line trading system.  IbPy implements functionality
that the Python programmer can use to connect to IB, request stock ticker
data, submit orders for stocks and options, and more.
"""


classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Office/Business :: Financial
Topic :: Office/Business :: Financial :: Investment
Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
"""


import sys
from distutils.core import setup


if sys.version_info < (2, 3):
    _setup = setup
    def setup(**kwargs):
        if kwargs.has_key('classifiers'):
            del kwargs['classifiers']
        _setup(**kwargs)


doclines = __doc__.split('\n')


setup(
    name = 'IbPy',
    version = '0.6',
    description = doclines[0],
    author = 'Troy Melhase',
    author_email = 'troy@gci.net',
    url = 'http://ibpy.sf.net/',
    license = 'BSD License',
    packages = ['ib', 'ib/client', 'ib/demos', 'ib/lib', 'ib/tests', 'ib/types'],
    classifiers = filter(None, classifiers.split('\n')),
    long_description = '\n'.join(doclines[2:]),
    platforms = ['any'],
    download_url = 'http://sourceforge.net/projects/ibpy/',
)

