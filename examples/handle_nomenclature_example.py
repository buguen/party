#!/usr/bin/python
# coding: utf-8

r"""
"""

from os.path import join, dirname

from party.library_creation import template_handle_nomenclature

template_handle_nomenclature(join(dirname(__file__), "ISO_4014/library.json"),
                             join(dirname(__file__), "ISO_4014/new_library.json"))
