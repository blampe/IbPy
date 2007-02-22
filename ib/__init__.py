#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# IbPy package root.
#
##

import os


if os.environ.get('IBPY_PSYCO'):
    import psyco
    psyco.full()
del(os)


# these values substituted during release build.
api = "0"
version = "0"
revision = "r0"


