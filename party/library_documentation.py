#!/usr/bin/python
# coding: utf-8

r"""library_documentation.py module

Generate the documentation for a parts library JSON file

"""

import json
from os import mkdir, getcwd, chdir, walk
from os.path import isdir, join
import logging

from subprocess import call

from party.library_checking import check_library_fields

logger = logging.getLogger(__name__)


def _create_folder(folder_path):
    r"""Create the folder if it does not exist

    Parameters
    ----------
    folder_path : str
        Path to the folder to create

    """
    if not isdir(folder_path):
        mkdir(folder_path)


def _library_rst(library_json_filepath):
    r"""Create the rst string for a parts library

    Parameters
    ----------
    library_json_filepath : str
        The path to the parts library

    Returns
    -------
    str : rst string for library documentation

    """
    rst_lines = list()

    ok, errors, reference_set_of_fields = \
        check_library_fields(library_json_filepath)
    assert ok is True
    assert len(errors) == 0
    logger.debug("fields are : %s" % str(reference_set_of_fields))

    with open(library_json_filepath) as data_file:
        json_file_content = json.load(data_file)

    rst_lines.append(json_file_content["metadata"]["name"])
    rst_lines.append("="*len(json_file_content["metadata"]["name"]))
    rst_lines.append("")

    max_lengths = dict()
    max_lengths['part_id'] = \
        max([len(part_id) for part_id in json_file_content["data"].keys()])

    for field_name in reference_set_of_fields:
        lengths_list = [len(str(value[field_name]))
                        for value in json_file_content["data"].values()]
        lengths_list.append(len(field_name))
        max_lengths[field_name] = max(lengths_list)

    header_fields = list(reference_set_of_fields)[:]
    header_fields.insert(0, "part_id")

    line_1 = " ".join(["="*(max_lengths[field]) for field in header_fields])
    line_2 = " ".join([field.ljust(max_lengths[field])
                       for field in header_fields])
    line_3 = line_1
    last_line = line_1

    rst_lines.append(line_1)
    rst_lines.append(line_2)
    rst_lines.append(line_3)

    # # Iterate on the parts found in the library JSON file
    # # to fill the table
    for part_id, part_values in json_file_content["data"].items():
        line = part_id.ljust(max_lengths["part_id"]) + " "
        for field in reference_set_of_fields:
            line += str(part_values[field]).ljust(max_lengths[field])
            line += " "
        rst_lines.append(line)

    rst_lines.append(last_line)

    return "\n".join(rst_lines)


def create_libraries_sphinx_sources(libraries_root_folder, doc_folder):
    r"""Create the sphinx files that are common to all libraries

    Parameters
    ----------
    libraries_root_folder : str
        Path to the root folder of libraries
    doc_folder : str
        Path to the folder where the documentation should be generated

    """
    folders = {
        "source": join(doc_folder, "source"),
        "source_static": join(doc_folder, "source/_static"),
        # "source_templates": join(doc_folder, "source/_templates"),
        "build": join(doc_folder, "build")}

    for k, v in folders.items():
        _create_folder(v)

    # create the conf.py file
    with open(join(folders["source"], "conf.py"), 'w') as conf:
        conf.write(CONF_PY)

    # create the index.rst file
    # there will be one index.rst file even if there are many libraries
    # documented
    with open(join(folders["source_static"], "index.rst"), 'w') as index:
        index.write(INDEX_HEADER)

        for root, dirs, files in walk(libraries_root_folder):
            logger.debug("Handling %s" % str(root))

            # it is considered a library if it ends with library.json
            libraries = [f for f in files if f.endswith('library.json')]

            # There should be one and only one library in a given folder
            # TODO : the above assertion is wrong

            if len(libraries) == 1:
                logger.debug("There is 1 library in %s" % str(root))
                logger.info("Found library %s" % str(libraries[0]))

                # read the library JSON file
                json_filename = join(root, libraries[0])

                with open(json_filename) as data_file:
                    json_file_content = json.load(data_file)
                #
                #     # write to library rst file
                with open(join(folders["source"],
                               json_file_content["metadata"]["name"] +
                                       '.rst'), 'w') as library_rst_file:
                    library_rst_file.write(_library_rst(json_filename))

                    index.write("   " + json_file_content["metadata"]["name"] +
                                "\n")

        index.write(INDEX_FOOTER)

    # Run sphinx
    cwd = getcwd()
    chdir(folders["source"])
    call(["ls", "-l"])
    call("sphinx-build -b html %s %s" % (folders["source"], folders["build"]))
    chdir(cwd)

CONF_PY = "#!/usr/bin/env python3\n" \
          "# -*- coding: utf-8 -*-\n" \
          "\n" \
          "extensions = ['sphinx.ext.autodoc', 'sphinx.ext.mathjax', ]\n" \
          "templates_path = ['_templates']\n" \
          "source_suffix = '.rst'\n" \
          "master_doc = 'index'\n" \
          "project = 'sphinx-test'\n" \
          "copyright = '2017, Guillaume Florent'\n" \
          "author = 'Guillaume Florent'\n" \
          "version = '1.0'\n" \
          "release = '1.0'\n" \
          "language = None\n" \
          "exclude_patterns = []\n" \
          "pygments_style = 'sphinx'\n" \
          "todo_include_todos = False\n" \
          "html_theme = 'alabaster'\n" \
          "# html_title = None\n" \
          "# html_short_title = None\n" \
          "# html_logo = None\n" \
          "# html_favicon = None\n" \
          "html_static_path = ['_static']\n" \
          "htmlhelp_basename = 'sphinx-testdoc'\n" \
          "latex_elements = {}\n" \
          "latex_documents = [(master_doc, 'sphinx-test.tex'," \
          " 'sphinx-test Documentation', 'Guillaume Florent', 'manual'), ]\n" \
          "man_pages = [(master_doc, 'sphinx-test'," \
          " 'sphinx-test Documentation', [author], 1)]\n" \
          "texinfo_documents = [(master_doc, 'sphinx-test'," \
          " 'sphinx-test Documentation', author, 'sphinx-test'," \
          " 'One line description of project.', 'Miscellaneous'), ]\n\n"


INDEX_HEADER = "Welcome to the library documentation\n" \
               "====================================\n" \
               "Contents:\n" \
               "\n" \
               ".. toctree::\n" \
               "   :maxdepth: 2\n" \
               "\n"

INDEX_FOOTER = "\n" \
               "\n" \
               "Indices and tables\n" \
               "==================\n" \
               "\n" \
               "* :ref:`genindex`\n" \
               "* :ref:`modindex`\n" \
               "* :ref:`search`\n" \
               "\n"
