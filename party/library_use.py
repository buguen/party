#!/usr/bin/python
# coding: utf-8

r"""Unique geometry script generation logic from a JSON parts library file"""

import imp
import logging
import os
import json

from templating import reconstruct_script_code_template, render
from library_checking import check_library_json_rules


logger = logging.getLogger(__name__)


def _scripts_folder(folder_path):
    return os.path.join(folder_path, "scripts")


def _steps_folder(folder_path):
    return os.path.join(folder_path, "steps")


def _stls_folder(folder_path):
    return os.path.join(folder_path, "stls")


def _htmls_folder(folder_path):
    return os.path.join(folder_path, "htmls")


def _create_folder(folder_path):
    r"""Create a folder if it does not exist"""
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)
        logger.info("Creating %s folder" % folder_path)
    else:
        logger.info("Folder %s already exists" % folder_path)


def _generate_script(json_generators, scripts_folder, part_id, context_):
    r"""Generate the Python geometry script for a given part_id

    Parameters
    ----------
    json_generators : dict
        Geometry generation code (key: generator id; value: lines of code)
    scripts_folder : str
        The folder where the script should be written
    part_id : str
        part id
    context_ : dict
        Values linked to the part_id

    Returns
    -------
    str : the path to the created Python geometry file

    """
    with open("tmp.py", "w") as tmp_file:
        tmp_file.write(reconstruct_script_code_template(
            json_generators[context_["generator"]]))

    # Use tmp.py as a template for context_ and write the results to the
    # part script
    py_geometry_file = os.path.join(scripts_folder, "%s.py" % part_id)
    with open(py_geometry_file, 'w') as f:
        f.write(render("tmp.py", context_))
    os.remove("tmp.py")

    return py_geometry_file


def _generate_cad(output_folder, py_geometry_file, output_format):
    if output_format not in ["step", "stl", "html"]:
        raise ValueError
    py_geometry_module = imp.load_source(py_geometry_file, py_geometry_file)
    part = py_geometry_module.part
    part_id = os.path.splitext(os.path.basename(py_geometry_file))[0]
    part_id = str(part_id)  # Keeps the OCC STEP Writer happy !

    if output_format == "step":
        part.to_step(os.path.join(output_folder, "%s.stp" % part_id))
    elif output_format == "stl":
        part.to_stl(os.path.join(output_folder, "%s.stl" % part_id))
    elif output_format == "html":
        part.to_html(os.path.join(output_folder, "%s.html" % part_id))


def generate(json_library_filepath, generate_steps=False, generate_stls=False,
             generate_htmls=False):
    r"""Create a geometry generation script for each part defined
    in the JSON file passed as a parameter

    Parameters
    ----------
    json_library_filepath : str
        The path to the JSON file describing the parts library
    generate_steps : bool
    generate_stls : bool
    generate_htmls : bool

    Raises
    ------
    KeyError

    """
    # Get the path of the JSON file passed as a parameter
    base_folder = os.path.dirname(json_library_filepath)
    scripts_folder = _scripts_folder(folder_path=base_folder)

    _create_folder(scripts_folder)

    # Deal with folder creation only one (i.e. not in the loop)
    if generate_steps:
        steps_folder = _steps_folder(base_folder)
        _create_folder(steps_folder)
    if generate_stls:
        stls_folder = _stls_folder(base_folder)
        _create_folder(stls_folder)
    if generate_htmls:
        htmls_folder = _htmls_folder(base_folder)
        _create_folder(htmls_folder)

    with open(json_library_filepath) as data_file:
        json_file_content = json.load(data_file)

    json_generators = json_file_content["generators"]

    # Check data is not empty
    for part_id, context_ in json_file_content["data"].items():
        py_geometry_file = _generate_script(json_generators, scripts_folder,
                                            part_id, context_)
        if generate_steps:
            _generate_cad(steps_folder, py_geometry_file, output_format="step")
        if generate_stls:
            _generate_cad(stls_folder, py_geometry_file, output_format="stl")
        if generate_htmls:
            _generate_cad(htmls_folder, py_geometry_file, output_format="html")


def generate_all(base_folder, preview=False, generate_steps=False,
                 generate_stls=False):
    r"""For each folder containing a JSON parts library definition:
    - check the JSON file is OK
    - if so, generate the geometry scripts

    Parameters
    ----------
    base_folder : str
        The root folder from which to generate
    preview : bool
        If True, do everything but creating the geometry scripts
        If False, also generate the geometry scripts
    generate_steps : bool
    generate_stls : bool

    """
    for item in os.walk(base_folder):
        if "library.json" in item[2]:
            json_filename_ = os.path.join(item[0], "library.json")
            logger.info("Library filename : %s" % json_filename_)
            logger.info("Checking the rules for the library JSON ...")
            ok, errors = check_library_json_rules(json_filename=json_filename_)
            if ok:
                logger.info("... done. Rules are OK")
                logger.info("Creating the Python scripts from the library "
                            "JSON ...")
                if preview is False:
                    generate(json_library_filepath=json_filename_,
                             generate_steps=generate_steps,
                             generate_stls=generate_stls)
                logger.info("... done")
            else:
                logger.error("The library contains errors, please "
                             "correct these before generating the scripts")
                print(errors)
