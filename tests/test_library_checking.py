#!/usr/bin/python
# coding: utf-8

r"""Tests for rules_checking.py"""

import os
import pytest

from party.library_checking import check_library_json_rules,\
    check_library_units_definition


# Rules checking related tests


def test_rules_checking_happy_path():
    r"""The parts library contains no error"""
    json_file = os.path.join(os.path.dirname(__file__),
                             "./json_files/good_library.json" )
    ok, errors = check_library_json_rules(json_file)
    assert ok is True
    assert errors == {}


def test_rules_checking_negative_weight():
    r"""The parts library file contains a data entry where the weight is
    negative, and this breaks a rule defined in the 'rules'section of the
    library"""
    json_file = os.path.join(os.path.dirname(__file__),
                             "./json_files/library_negative_weight.json")
    ok, errors = check_library_json_rules(json_file)
    assert ok is False
    assert len(errors) == 1
    assert len(errors["608ZZ"]) == 1


def test_rules_checking_negative_weight_s():
    r"""The parts library file contains 2 data entries where the weight is
    negative, and this breaks a rule defined in the 'rules'section of the
    library"""
    json_file = os.path.join(os.path.dirname(__file__),
                             "./json_files/library_negative_weight_s.json")
    ok, errors = check_library_json_rules(json_file)
    assert ok is False
    assert len(errors) == 2
    assert len(errors["624ZZ"]) == 1
    assert len(errors["608ZZ"]) == 1


def test_rules_checking_many_errors():
    r"""608ZZ has a negative weight
    624ZZ has negative weight and an inner diameter that is greater than its
    outer diameter

    """
    json_file = os.path.join(os.path.dirname(__file__),
                             "./json_files/library_many_errors.json")
    ok, errors = check_library_json_rules(json_file)
    assert ok is False
    assert len(errors) == 2
    assert len(errors["624ZZ"]) == 2
    assert len(errors["608ZZ"]) == 1


def test_rules_checking_rules_definition_error():
    r"""The rules contain an identifier that is not used to define parts

    outer_diameter changed to out_diam in library_wrong_rule.json

    """
    json_file = os.path.join(os.path.dirname(__file__),
                             "./json_files/library_wrong_rules.json")
    with pytest.raises(NameError):
        _, _ = check_library_json_rules(json_file)


def test_rules_checking_rules_syntax_error():
    r"""The rules contain a syntax error

    outer_diameter ! inner_diameter in the rules

    """
    json_file = os.path.join(os.path.dirname(__file__),
                             "./json_files/library_wrong_rules_syntax.json")
    with pytest.raises(SyntaxError):
        _, _ = check_library_json_rules(json_file)


# Units related tests


def test_units_ok():
    r"""The parts library file is ok regarding units definition and use"""
    json_file = os.path.join(os.path.dirname(__file__),
                             "./json_files/library_ok_units.json")
    ok, errors = check_library_units_definition(json_file)
    assert ok is True
    assert len(errors) == 0


def test_units_ok():
    r"""'p' is defined twice as a length unit"""
    json_file = os.path.join(os.path.dirname(__file__),
                             "./json_files/library_duplicate_units.json")
    ok, errors = check_library_units_definition(json_file)
    assert ok is False
    assert len(errors) == 1
    assert "units definition" in errors


def test_missing_units_definition():
    r"""One of the data entries contains a 'undefined_field_in_units' field"""
    json_file = os.path.join(os.path.dirname(__file__),
                             "./json_files/library_missing_units_definition.json")
    ok, errors = check_library_units_definition(json_file)
    assert ok is False
    assert len(errors) == 1