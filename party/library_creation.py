#!/usr/bin/python
# coding: utf-8

r"""The library_creation.py module contains standard mechanisms to create a
library.json file from standard templates

Currently implemented:

- alias mechanism : replace aliases by the values they refer to
- generator code : replace the {{ generators }} tag in the template by the code
found in the generators subdirectory

Every function has a file_in and a file_out parameter that can be used by
the specific library.json creation routines as required

"""

import json
import os
import logging

from collections import OrderedDict

from templating import render, to_json_string


logger = logging.getLogger(__name__)


def template_handle_aliases(file_in, file_out):
    r"""Replace aliases found in a template file by the values they refer to

    Parameters
    ----------
    file_in : str
        Path to the input file (i.e. a template using aliases)
    file_out : str
        The output file
        (i.e. a template with replaced aliases or the final file)

    """
    with open(file_in) as fi:
        json_content = json.load(fi, object_pairs_hook=OrderedDict)

    json_aliases = json_content["aliases"]

    # Deal with the aliases
    for name, context_ in json_content["data"].items():
        # modify context with the alias mechanism
        while has_aliases(context_):
            for k, v in context_.items():
                if "__alias__" in str(v):
                    key_in_aliases = str(v).replace("__alias__", "")
                    for alias_key, alias_value in \
                            json_aliases[key_in_aliases].items():
                        context_[alias_key] = alias_value
                    del context_[k]  # do not keep the alias link

    del json_content["aliases"]

    with open(file_out, 'w') as fp:
        json.dump(json_content, fp, sort_keys=False, indent=2)


def template_handle_generators(file_in, file_out):
    r"""Replace the {{ generators }} tag by geometry generation code using
     Python generator files in the generators subdirectory

    Parameters
    ----------
    file_in : str
        Path to the input file
        (i.e. a template containing a {{ generators )} tag)
    file_out : str
        The output file
        (i.e. a template with replaced {{ generators }} tag or the final file)

    """
    # Deal with generator code
    generators = dict()

    # iterate over the files in the templates folder
    for generator_file in os.listdir("generators"):
        # use the file name without extension as the generator id
        generator_id = os.path.splitext(generator_file)[0]

        with open("generators/%s" % generator_file) as gf:
            generators[generator_id] = gf.readlines()

    context = dict()
    context["generators"] = to_json_string(generators)

    with open(file_out, 'w') as fo:
        fo.write(render(file_in, context))


def has_aliases(d):
    r"""Checks if a dictionnary has values with the __alias__ string

    Parameters
    ----------
    d : dict

    Returns
    -------
    bool

    """
    has_alias = False
    for k, v in d.items():
        if "__alias__" in str(v):
            has_alias = True
    return has_alias
