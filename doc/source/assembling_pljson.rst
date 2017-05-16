.. _assembling-pljson-label:

Assembling the parts library JSON (PLJSON) files
************************************************

From the previous chapter (:ref:`pljson-file-format-label`), it is obvious that a
PLJSON file contains duplicated information. This is intentional as it greatly simplifies
the exploitation of the PLJSON files.

Though, if we have 200 screws using the same threading, correcting an error for
one of the threading definition values will be a very repetitive task
as it will have to be corrected for each screw.

To simplify the creation of PLJSON files, **party** provides a set of so-called
'standard-mechanisms' ( see :ref:`standard-mechanisms-label`).

Creating a PLJSON file might use any kind of logic and information sources as
long as the resulting PLJSON file conforms to the PLJSON file format (:ref:`pljson-file-format-label`)
but these standard mechanisms are offered as a guided way to create the PLJSON files.

Roles
=====

Library creators
----------------

Parts library creators are expected to know and use the T-PLJSON template files
possibilities and the accompanying :ref:`standard-mechanisms-label`


Library users
-------------

If your intention is only to use a parts library (PLJSON) file for a project,
you do not need to know about what follows.

Template files (T-PLJSON)
=========================

Parts library templates skeleton creation
-----------------------------------------

The :func:`create_skeleton() <party.library_creation.create_skeleton>` function
of the :mod:`party.library_creation` module creates a starting point for a parts library
project based on template files.

.. _standard-mechanisms-label:

Standard mechanisms
-------------------

**party** provides the following mechanisms to create parts library (PLJSON) files from
part library template files:

- geometry and anchors code inclusion

- alias mechanism

- include mechanism (in development)

Geometry and anchors code inclusion
-----------------------------------

This mechanism is handled by the :func:`template_handle_generators() <party.library_creation.template_handle_generators>`
function of the :mod:`party.library_creation` module.

It expects:

- a *{{ generators }}* tag as the value of the 'generators' id in the template file

.. code-block:: json

  {
    "metadata": {...},
    "generators": { {{ generators }} },
    "rules": {...},
    "data": {...}
  }

- the geometry and anchors generation scripts in a *generators* subfolder of the folder containing the template file.

Alias mechanism
---------------

This mechanism is handled by the :func:`template_handle_aliases() <party.library_creation.template_handle_aliases>`
function of the :mod:`party.library_creation` module.

It expects:

- an *alias* entry in the template file where the aliases are defined

.. code-block:: json

  {
    "metadata": {...},
    "generators": { {{ generators }} },
    "rules": {...},
    "aliases": {
        "M1.6_grade_A": {
          "generics": "__alias__M1.6_generics",
          "grade_specifics": "__alias__M1.6_grade_A_specifics"
        },
        "M1.6_grade_B":{
          "generics": "__alias__M1.6_generics",
          "grade_specifics": "__alias__M1.6_grade_B_specifics"
        },
        "M1.6_generics": {
          "p": 0.35,
          "b_ref_b": 9.00,
          "b_ref_c": 15.00,
          "b_ref_d": 28.00,
          "c_max": 0.25,
          "c_min": 0.10,
          "d_a": 2.00,
          "d_s_max": 1.60,
          "l_f_max": 0.60,
          "k_nominal": 1.10,
          "r_min": 0.10,
          "s_max": 3.20
        },
        "M1.6_grade_A_specifics": {
          "d_s_min": 1.46,
          "d_w_min": 2.27,
          "e": 3.41,
          "k_max": 1.225,
          "k_min": 0.975,
          "k_w_e_min": 0.68,
          "s_min": 3.02
        },
        "M1.6_grade_B_specifics": {
          "d_s_min": 1.35,
          "d_w_min": 2.30,
          "e": 3.28,
          "k_max": 1.30,
          "k_min": 0.9,
          "k_w_e_min": 0.63,
          "s_min": 2.90
        },

        "M2_grade_A": {
          "generics": "__alias__M2_generics",
          "grade_specifics": "__alias__M2_grade_A_specifics"
        },
        "M2_grade_B":{
          "generics": "__alias__M2_generics",
          "grade_specifics": "__alias__M2_grade_B_specifics"
        },
        "M2_generics": {
          "p": 0.40,
          "b_ref_b": 10.00,
          "b_ref_c": 16.00,
          "b_ref_d": 29.00,
          "c_max": 0.25,
          "c_min": 0.10,
          "d_a": 2.60,
          "d_s_max": 2.00,
          "l_f_max": 0.80,
          "k_nominal": 1.40,
          "r_min": 0.10,
          "s_max": 4.00
        },
        "M2_grade_A_specifics": {
          "d_s_min": 1.86,
          "d_w_min": 3.07,
          "e": 4.32,
          "k_max": 1.525,
          "k_min": 1.275,
          "k_w_e_min": 0.89,
          "s_min": 3.82
        },
        "M2_grade_B_specifics": {
          "d_s_min": 1.75,
          "d_w_min": 2.95,
          "e": 4.18,
          "k_max": 1.6,
          "k_min": 1.2,
          "k_w_e_min": 0.84,
          "s_min": 3.70
        },
    "data": {...}
  }

As illustrated by the example, aliases can be nested.

- the use of the defined aliases in the **data** section with an '__alias__' prefix.

.. code-block:: json

  {
    "metadata": {...},
    "generators": { {{ generators }} },
    "rules": {...},
    "data": {
        "M1.6x12_A": {
          "description": "M1.6 ISO 4014 screw, 12 mm, grade A",
          "generator": "iso4014_screw",
          "l_min": 11.65,
          "l_max": 12.35,
          "l_s_min": 1.20,
          "l_g_max": 3.00,
          "threading": "__alias__M1.6_grade_A"
      },
      ...
    }
  }

Include mechanism
-----------------

This mechanism is handled by the :func:`template_handle_includes() <party.library_creation.template_handle_includes>`
function of the :mod:`party.library_creation` module.

The include mechanism is currently in development.

Automation
----------

The :func:`template_handle_includes() <party.library_creation.autocreate_library>`
function of the :mod:`party.library_creation` module analyzes the template file and uses the standard
mechanisms in the right order to create the parts library (PLJSON) file.

Checks
======

When the parts library JSON (PLJSON) file has been assembled, the :mod:`party.library_checking` module provides functions
which goal is to check that the PLJSON file complies with the PLJSON file specification and that the data is correct.

Constant data schema
--------------------

The :func:`check_library_fields() <party.library_checking.check_library_fields>` function checks that the metadata for each entry in the
**data** section is the same.

Rules
-----

The :func:`check_library_json_rules() <party.library_checking.check_library_json_rules>` function checks that the rules defined in
the **rules** section are respected in the **data** section of the PLJSON file.

Units definition
----------------

The :func:`check_library_units_definition() <party.library_checking.check_library_units_definition>` function checks that the units defined
in the **metadata/units** are properly defined and that each fields describing a part characteristic are present in the units definition.