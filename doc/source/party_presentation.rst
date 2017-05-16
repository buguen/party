party
*****

What is party ?
===============

**party** is a Python package that handles parts libraries creation and use.

Parts libraries creation
========================

A parts library might contain a lot of duplicated information (e.g. all the M3 screws will have the data defined for their threading).
**party** provides standard mechanisms to avoid this duplication and to create the parts libraries JSON files from **template** files
where no data is duplicated.

The parts library files must also contain the part geometry creation logic. **party** deals with inserting the geometry creation defined
in a Python script into the parts library JSON file. As we will see, the geometry creation logic can also define **anchors** that allow to attach
the parts from the library in a wider project.

Parts libraries use
===================

**party** can generate CAD files from the parts library JSON file (PLJSON)
and documentation in several formats for the parts library (HTML, PDF, ePub, Latex..) using Sphinx.

Dependencies
============

**party** depends on:

- ccad (which itself depends on PythonOCC)

- jinja2
