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


def create_skeleton(base_folder):

    folder_name = os.path.basename(base_folder)

    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)

    generators_folder_path = os.path.join(base_folder, "generators")

    if not os.path.isdir(generators_folder_path):
        os.mkdir(generators_folder_path)

    sample_generator_path = os.path.join(generators_folder_path, "%s.py" % folder_name)
    sample_library_template_path = os.path.join(base_folder, "library_template.json")
    sample_create_path = os.path.join(base_folder, "create_library.py")
    sample_use_path = os.path.join(base_folder, "use_library.py")

    with open(sample_generator_path, 'w') as gen:
        gen.write('r"""Generation script for %s"""\n' % folder_name)
        gen.write("\n")
        gen.write("from ccad.model import cylinder\n")
        gen.write("\n")
        gen.write("radius = {{ radius }}\n")
        gen.write("length = {{ length }}\n")
        gen.write("\n")
        gen.write("part = cylinder(radius, length)\n")
        gen.write('anchors = {1: {"position": (0., 0., 0.), "direction": (0., 0., -1.)},\n')
        gen.write('           2: {"position": (0., 0., length), "direction": (0., 0., 1.)}}\n')

    with open(sample_library_template_path, 'w') as template:
        template.write("{\n")
        template.write('  "metadata":{\n')
        template.write('    "name": "%s",\n' % folder_name)
        template.write('    "description": "<please complete>",\n')
        template.write('    "units": {\n')
        template.write('      "length": ["mm", ["radius", "length"]],\n')
        template.write('      "force": ["N", []],\n')
        template.write('      "weight": ["g", []]\n')
        template.write('    },\n')
        template.write('    "authors": ["<author 1>", "<author 2>"],\n')
        template.write('    "url": "https://github.com/<please complete>",\n')
        template.write('    "license": "GPL v3"\n')
        template.write('  },\n')
        template.write('  "generators":\n')
        template.write('    { {{ generators }} },\n')
        template.write('  "rules": ["radius > 0", "length > 0"],\n')
        template.write('  "aliases": {},\n')
        template.write('  "data":{\n')
        template.write('    "part_id_1": {\n')
        template.write('      "description": "Part number 1",\n')
        template.write('      "generator": "%s",\n' % folder_name)
        template.write('      "radius": 10.0,\n')
        template.write('      "length": 20.0\n')
        template.write('    },\n')
        template.write('    "part_id_2": {\n')
        template.write('      "description": "Part number 2",\n')
        template.write('      "generator": "%s",\n' % folder_name)
        template.write('      "radius": 10.0,\n')
        template.write('      "length": 40.0\n')
        template.write('    }\n')
        template.write('  }\n')
        template.write('}\n')

    with open(sample_create_path, 'w') as create:
        create.write("#!/usr/bin/python\n")
        create.write("# coding: utf-8\n")
        create.write("\n")
        create.write('r"""Script that creates the library.json file for the %s"""\n' % folder_name)
        create.write("\n")
        create.write("import logging\n")
        create.write("\n")
        create.write("from party.library_creation import autocreate_library\n")
        create.write("from party.library_checking import check_all\n")
        create.write("\n")
        create.write("logging.basicConfig(level=logging.DEBUG,\n")
        create.write("                    format='%(asctime)s :: %(levelname)6s :: '\n")
        create.write("                           '%(module)20s :: %(lineno)3d :: %(message)s')\n")
        create.write("\n")
        create.write('autocreate_library("library_template.json")\n')
        create.write('library_ok_list, _ = check_all("library.json")\n')
        create.write("for entry in library_ok_list:\n")
        create.write("    assert entry is True\n")

    with open(sample_use_path, 'w') as use:
        use.write("#!/usr/bin/python\n")
        use.write("# coding: utf-8\n")
        use.write("\n")
        use.write('r"""Example use of the library.json file to create geometry_scripts \n')
        use.write('and cad files"""\n')
        use.write("\n")
        use.write("import logging\n")
        use.write("from os.path import join, dirname\n")
        use.write("\n")
        use.write("from party.library_use import generate\n")
        use.write("\n")
        use.write("\n")
        use.write("logging.basicConfig(level=logging.DEBUG,\n")
        use.write("                    format='%(asctime)s :: %(levelname)6s :: '\n")
        use.write("                           '%(module)20s :: %(lineno)3d :: %(message)s')\n")
        use.write("\n")
        use.write('generate(json_library_filepath=join(dirname(__file__), "library.json"),\n')
        use.write("         generate_steps=True, generate_stls=True, generate_htmls=True)\n")


def _analyze_template(template_file):
    r"""Analyze a parts library template file for certain features and report
    on their presence

    Parameters
    ----------
    template_file : str
        Path to the template file

    Returns
    -------
    dict : keys are features, values are bool (True if feature is present)

    """

    info = {"generators": False, "aliases": False}

    with open(template_file) as f:
        content = f.readlines()

    for line in content:
        if "{{generators}}" in line or "{{ generators }}" in line:
            info["generators"] = True

        if "__alias__" in line:
            info["aliases"] = True

    return info


def autocreate_library(template_file):
    r"""Automated parts library creation from a template file. The template
    processing is automated depending on the presence of certain features in
    the template

    Parameters
    ----------
    template_file : str
        Path to the template file

    """
    info = _analyze_template(template_file)
    logger.info("template file has generators tag : %s" % str(info["generators"]))
    logger.info("template file has aliases : %s" % str(info["aliases"]))

    template_folder = os.path.dirname(template_file)
    tmp_path = os.path.join(template_folder, "tmp.json")
    final_path = os.path.join(template_folder, "library.json")

    if info["generators"] is True:
        # template_handle_generators(template_file, tmp_path)
        if info["aliases"] is True:
            template_handle_generators(template_file, tmp_path)
            template_handle_aliases(tmp_path, final_path)
        else:
            template_handle_generators(template_file, final_path)
    else:
        if info["aliases"] is True:
            template_handle_aliases(template_file, final_path)


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
