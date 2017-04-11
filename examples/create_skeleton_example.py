#!/usr/bin/python
# coding: utf-8

r"""Example of initing a parts library project by generating a skeleton"""

import os
import logging

from party.library_creation import create_skeleton

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: '
                           '%(module)20s :: %(lineno)3d :: %(message)s')

create_skeleton(os.path.join(os.path.dirname(__file__), "new_library"))
