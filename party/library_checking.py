#!/usr/bin/python
# coding: utf-8

r"""Parts library checks"""

import json
import logging


logger = logging.getLogger(__name__)


def check_library_json_rules(json_filename):
    r"""Check that the entries in the 'data' field of a library respect the
    rules defined in the 'rules' field of the library

    Parameters
    ----------
    json_filename : str
        Path to the JSON file that describes the parts library

    Returns
    -------
    tuple(bool, errors)
        bool : True if the library is OK, False otherwise
        errors : dict (keys: part_identifier, values: list of broken rules)

    Raises
    ------
    NameError if the rules definition contain wrong identifiers
    SyntaxError if there is a syntax error in the rules definition

    """
    with open(json_filename) as data_file:
        json_file_content = json.load(data_file)

    library_ok = True
    errors = dict()

    for part_id, part_values in json_file_content["data"].items():
        # assign the values to a Python variable with the same name
        for dict_entry_key, dict_entry_value in part_values.items():
            if type(dict_entry_value) not in [unicode, str]:
                instruction = "%s = %s" % (dict_entry_key, dict_entry_value)
            else:
                instruction = "%s = '%s'" % (dict_entry_key, dict_entry_value)
            exec instruction

        for rule in json_file_content["rules"]:
            instruction = "bool_ = %s" % rule
            # logger.info("Checking '%s' for part %s" % (rule, part_id))
            exec instruction
            if bool_ is True:
                # logger.info("OK")
                pass
            else:
                library_ok = False
                if part_id not in errors.keys():
                    errors[part_id] = list()
                errors[part_id].append(rule)
                logger.error("Library data definition error")

    return library_ok, errors