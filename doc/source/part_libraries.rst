Part libraries
**************

The need for part libraries
===========================

Any hardware design project is expected to use an important number of standardized parts (screws, bolts, washers, bearings ...) and
of catalog/off-the-self components. The designer should not have to redesign these kinds of components that should be available and
chosen from part libraries.
Industrial CAD softwares include such libraries but unfortunately they are very expensive and not open source.

The problems
============

Part libraries, when available, are offered under a variety of neutral formats (STEP, IGES ...) and proprietary formats.
These files are usually heavyweight and not always in the format expected by the designer.
Moreover, these files contain no design intent information nor any means to functionally link them to other
parts, assemblies or systems in the project.

Lightweight and self-contained part libraries
=============================================

The **party** package aims at providing a way to define parts libraries in text files, as well as the tools to use these text files
to generate the geometry and the means to attach the parts (anchors/constraints) in a hardware design project.
**party** can also generate the documentation in various formats for the parts libraries.
The parts library JSON files created and used by **party** are self-contained: all the required information, including the geometry and
'anchoring' logic is defined in the JSON file.

Definition of a parts library
=============================

In the context of the **party** Python package, a parts library is a JSON file where every part
can be defined by using the same set of fields.
