.. _using-pljson-label:

Using parts library JSON (PLJSON) files
***************************************

Now that we have a proper PLJSON file, what can we do with it?

Create library CAD files
========================

The :func:`generate() <party.library_use.generate>` function of the :mod:`party.library_use`
module will create `ccad <https://github.com/guillaume-florent/ccad>`_ scripts and CAD files
(depending on the optional arguments values) in subfolders of
the folder containing the parts library JSON (PLJSON) file.

Formats
-------

From the parts library JSON (PLJSON) file, it is possible to create one CAD file
per entry in the **data** section of the PLJSON file in the following formats:

- STEP (AP203)

- STL

- HTML (to view the part in the browser using X3DOM)


Example
-------

See the :mod:`examples/ISO_4014/use_library_json.py` script for an example of
how to generate the CAD files from the parts library (PLJSON) file.

.. literalinclude:: ../../examples/ISO_4014/use_library_json.py



Create the library documentation
================================

The :func:`generate() <party.library_documentation.create_libraries_sphinx_sources>` function of the :mod:`party.library_documentation`
module will create HTML documentation of the parts library JSON (PLJSON) file in the folder passed as a parameter.

Formats
-------

Currently, only HTML documentation generation is implemented.

Example
-------

See the :mod:`examples/create_documentation_example.py` script for an example of
how to generate the documentation of the parts library (PLJSON) file.

.. literalinclude:: ../../examples/create_documentation_example.py

Use the parts in other projects
===============================

Work in progress to use the parts library JSON (PLJSON) files in:

- a new (in development) CAD project definition structure based on acyclic directed graphs.

- other CAD softwares that offer scripting/plugin capabilities
