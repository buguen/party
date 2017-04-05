#!/usr/bin/python
# coding: utf-8

r"""Unique geometry script generation logic from a JSON parts library file"""

import logging
import os
import json

from templating import reconstruct_script_code_template, render
from rules_checking import check_library_json


logger = logging.getLogger(__name__)


def generate_scripts(json_library_filepath):
    r"""Create a geometry generation script for each part defined
    in the JSON file passed as a parameter

    Parameters
    ----------
    json_library_filepath : str
        The path to the JSON file describing the parts library

    Raises
    ------
    KeyError

    """
    # Get the path of the JSON file passed as a parameter
    json_file_dir_path = os.path.dirname(json_library_filepath)
    scripts_dir = os.path.join(json_file_dir_path, "scripts")

    if not os.path.isdir(scripts_dir):
        os.mkdir(scripts_dir)
        logger.info("Creating 'scripts' directory in %s" % scripts_dir)
    else:
        logger.info("'scripts' directory already exists in %s" % scripts_dir)

    with open(json_library_filepath) as data_file:
        json_file_content = json.load(data_file)

    json_generators = json_file_content["generators"]
    # json_aliases = json_file_content["aliases"]

    for name, context_ in json_file_content["data"].items():
        with open("tmp.py", "w") as tmp_file:
            tmp_file.write(reconstruct_script_code_template(
                json_generators[context_["generator"]]))

        # Use tmp.py as a template for context_ and write the results to the
        # part script
        py_geometry_file = os.path.join(scripts_dir, "%s.py" % name)
        with open(py_geometry_file, 'w') as f:
            f.write(render("tmp.py", context_))
        os.remove("tmp.py")


def generate_all_scripts(preview=False):
    r"""For each folder containing a JSON parts library definition:
    - check the JSON file is OK
    - if so, generate the geometry scripts

    Parameters
    ----------
    preview : bool
        If True, do everything but creating the geometry scripts
        If False, also generate the geometry scripts

    """
    for item in os.walk(os.path.join(os.path.dirname(__file__), "..")):
        if "library.json" in item[2]:
            json_filename_ = os.path.join(item[0], "library.json")
            logger.info("Library filename : %s" % json_filename_)
            logger.info("Checking the rules for the library JSON ...")
            ok, errors = check_library_json(json_filename=json_filename_)
            if ok:
                logger.info("... done. Rules are OK")
                logger.info("Creating the Python scripts from the library "
                            "JSON ...")
                if preview is False:
                    generate_scripts(json_library_filepath=json_filename_)
                logger.info("... done")
            else:
                logger.error("The library contains errors, please "
                             "correct these before generating the scripts")
                print(errors)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s :: %(levelname)6s :: '
                               '%(module)20s :: %(lineno)3d :: %(message)s')
    generate_all_scripts(preview=False)
