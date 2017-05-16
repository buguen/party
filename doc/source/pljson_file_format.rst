.. _pljson-file-format-label:

Parts libraries JSON format
***************************

We must distinguish:

- the final parts library JSON files, that are to be publicly released for use in open hardware projects (PLJSON)

- the 'template' files (T-PLJSON) that are used to create PLJSON files. These 'template' files are only precursors for the PLJSON files.

The 'template' T-PLJSON files (see :ref:`assembling-pljson-label`) are used to make maintenance easier by:

- avoiding duplicated information

- allowing to keep the geometry and anchors creation logic in a separate Python file (more readable and easier to debug)


This paragraph describes the PLJSON file format.

General
=======

A PLJSON file is made of 4 sections:

- the **metadata** section;

- the **generators** section;

- the **rules** section;

- the **data** section.

.. code-block:: json

  {
    "metadata": {},
    "generators": {},
    "rules": {},
    "data": {}
  }

The metadata section
====================

The metadata section must contain the following entries:

- **name** : the name of the parts library, without spaces (i.e. 'iso4014-screws-library' is ok, 'iso4014 screws library' is not). The characters used must be valid file name characters for the OS.

- **description** : a plain text description of the library. Spaces, punctuation marks and special characters (outside of JSON specific characters) are allowed.

- **units** : for each type of unit, the unit and the variables in that unit are defined:

For example:

.. code-block:: json

  {
    "metadata": {
      "units": {
        "length": ["mm", ["p", "b_ref_b", "b_ref_c", "b_ref_d", "c_max"....]],
        "force": ["N", []],
        "weight": ["g", []],
        "dimensionless": ["", ["threading", "generics", "grade_specifics"]]
      },
    ....
    }
  }

defines 'p' as a length in mm (millimeters). 'threading' is data without a dimension nor a unit. A forces would be in newtons if one was defined, but none is.

- **authors** defines the list of library authors.

.. code-block:: json

  {
    "metadata": {
      ...
      "authors": ["Guillaume Florent", "Thomas Paviot", "Bernard Uguen"],
      ...
    }
  }

- **url** : url is the well ... the url from which the file was downloaded

- **license** : license is the short name of the license of the library (e.g. GPLv3)

The metadata section may contain the following entries:

- **nomenclature** : the naming convention for the parts defined in the **data** section. The naming convention is defined as a Python expression that evaluates to a string.

For example (threading and l_max are parts data definition identifiers):

.. code-block:: json

  {
    "metadata": {
      ...
      "nomenclature": "'ISO4014_' + threading + 'x' + str(int(l_max))",
      ...
      }
      ...
  }

The nomenclature can be used to check that every entry in the **data** section has an id that respects the nomenclature.



The generators section
======================

The **generators** section contains one entry per potential geometry and anchors generator (every entry in the
data section is linked to a generator by its 'generator' field).

The value of each entry is a list a Python instructions using the ccad package. Library creators are not expected to
directly write the Python instructions in the PLJSON file. Instead, the templates mechanism allows including a Python script in the final PLJSON file)

Here is an example generators section:

.. code-block:: json

  {
    ...
    "generators": {
      "iso4014_screw": [
        "r'''Generation script for ISO 4014 screw'''",
        "",
        "from ccad.model import prism, filling, ngon, cylinder, translated",
        "",
        "k_max = {{ k_max }}",
        "s_max = {{ s_max }}",
        "l_g_max = {{ l_g_max }}",
        "d_s_max = {{ d_s_max }}",
        "d_s_min = {{ d_s_min }}",
        "l_max = {{ l_max }}",
        "",
        "head = translated(prism(filling(ngon(2 / 3**.5 * s_max / 2., 6)), (0, 0, k_max)), (0., 0., -k_max))",
        "",
        "threaded = cylinder(d_s_min / 2., l_max)",
        "unthreaded = cylinder(d_s_max / 2., l_g_max)",
        "",
        "part = head + threaded + unthreaded",
        "anchors = {1: {'position': (0., 0., 0.),",
        "               'direction': (0., 0., -1.),",
        "               'dimension': d_s_max,",
        "               'description': 'screw head on plane'}}"
      ]
    },
  ...
  }

Values in double curly bracket (e.g. {{ k_max }}) are placeholders for the values defined in each entry of the **data** section.

The rules section
=================

The **rules** section contain a list of Python expressions that must all evaluate to True for
each entry of the **data** section  for the PLJSON file to be considered correct.

Here is an example **rules** section:

.. code-block:: json

  {
    ...
    "rules": ["c_max > c_min", "d_a_max > d_a_min", "m_max > m_min", "s_max > s_min"],
    ...
  }

The first rule in this example states that c_max must be strictly superior to c_min in each entry of the **data** section.

Any Python expression that evaluates to a boolean can be used.

The data section
================

The **data** section defines the possible values for each part contained in the parts library.

Every entry must contain the same set of fields. If this is not possible, another parts library must be created.

2 fields are compulsory : 'generator' (and its value must be in the ids defined in the **generators** section) and description.

The other fields are application/standard dependant.

.. code-block:: json

  {
    ...
    "data": {
      "ISO4014_M1.6_grade_Ax12": {
        "description": "M1.6 ISO 4014 screw, 12 mm, grade A",
        "generator": "iso4014_screw",
        "l_min": 11.65,
        "l_max": 12.35,
        "l_s_min": 1.2,
        "l_g_max": 3.0,
        "threading": "M1.6_grade_A",
        "generics": "M1.6_generics",
        "grade_specifics": "M1.6_grade_A_specifics",
        "p": 0.35,
        "b_ref_b": 9.0,
        "b_ref_c": 15.0,
        "b_ref_d": 28.0,
        "c_max": 0.25,
        "c_min": 0.1,
        "d_a": 2.0,
        "d_s_max": 1.6,
        "l_f_max": 0.6,
        "k_nominal": 1.1,
        "r_min": 0.1,
        "s_max": 3.2,
        "d_s_min": 1.46,
        "d_w_min": 2.27,
        "e": 3.41,
        "k_max": 1.225,
        "k_min": 0.975,
        "k_w_e_min": 0.68,
        "s_min": 3.02
      },
      "ISO4014_M1.6_grade_Ax16": {
        "description": "M1.6 ISO 4014 screw, 16 mm, grade A",
        "generator": "iso4014_screw",
        "l_min": 15.65,
        "l_max": 16.35,
        "l_s_min": 5.2,
        "l_g_max": 7.0,
        "threading": "M1.6_grade_A",
        "generics": "M1.6_generics",
        "grade_specifics": "M1.6_grade_A_specifics",
        "p": 0.35,
        "b_ref_b": 9.0,
        "b_ref_c": 15.0,
        "b_ref_d": 28.0,
        "c_max": 0.25,
        "c_min": 0.1,
        "d_a": 2.0,
        "d_s_max": 1.6,
        "l_f_max": 0.6,
        "k_nominal": 1.1,
        "r_min": 0.1,
        "s_max": 3.2,
        "d_s_min": 1.46,
        "d_w_min": 2.27,
        "e": 3.41,
        "k_max": 1.225,
        "k_min": 0.975,
        "k_w_e_min": 0.68,
        "s_min": 3.02
      },
      ...
    }
  }
