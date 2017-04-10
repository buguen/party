#!/usr/bin/python
# coding: utf-8

r"""Example use of the library.json file to create geometry_scripts and
cad files

"""

import logging
import os

from party.library_use import generate


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: '
                           '%(module)20s :: %(lineno)3d :: %(message)s')

generate(json_library_filepath=os.path.join(os.path.dirname(__file__),
                                            "library.json"),
         generate_steps=True, generate_stls=True, generate_htmls=True)
