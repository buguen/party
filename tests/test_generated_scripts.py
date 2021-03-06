#!/usr/bin/python
# coding: utf-8

r"""Test scripts generated by generate.py from the JSON part library definition
"""


import os
# import imp
import json
import pytest

# from ccad.model import Solid

from party.scripts_checking import check_script


def test_generated_scripts_from_scripts_folder_content():
    r"""Test that the scripts generated from the JSON file by generate.py
    can be imported and contain sensible content

    This test only checks that the generated files are a valid Python module
    that crates a part and an anchors variable in their global namespace

    """
    # Find the scripts directories
    test_scripts_folder = os.path.join(os.path.dirname(__file__), "../scripts")
    for item in os.walk(test_scripts_folder):
        # if item[0].endswith("scripts"):
        for f in os.listdir(item[0]):
            if os.path.splitext(f)[-1] == ".py":  # only py extensions
                script_ok, errors = check_script(f)
                assert script_ok is True


@pytest.mark.skip("Unskip when the metric screws are properly implemented")
def test_generated_scripts_from_json():
    r"""Test that the scripts generated from the JSON file by generate.py
    can be imported and contain sensible content

    This is another way to test the generated scripts. This way checks that
    every data entry in the library.JSON has a corresponding script that works

    """
    for item in os.walk(os.path.join(os.path.dirname(__file__), "..")):
        if "library.json" in item[2]:
            with open("%s/%s" % (item[0], "library.json")) as data_file:
                json_file_content = json.load(data_file)

            for name, context_ in json_file_content["data"].items():
                    script_ok, errors = check_script(os.path.join(item[0], "scripts/%s.py" % name))
                    assert script_ok is True
