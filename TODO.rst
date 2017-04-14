******** Move generated files tests from 'tests' to a function that can be used by library creators

******** Migrate issues from standard-cad-parts

******** units management : list in units section of JSON

******** Automate library.json generation based on the contents of the input file (contains {{ generators }}, aliases, __alias__

******** STEP, STL and HTML generation should be possible (but not automatic)

-> 'include' library creation mechanism
  impact on the autocreation

library JSON names must be different, yet with a constant (e.g. *_library.json)

Doc !! (preliminary : learn Sphinx)

Nom des caractéristiques ou dessin technique, comment l'utilisateur peut comprendre ce que représente telle ou telle dimension?
  Intégrer les dimensions aux generators

Improve screw geometry generator

create an HTML file that allows querying the library?
  Should we be able to query on the name of alias parameters (e.g. __alias__M1) -> yes -> rename to 'M1' instead of deleting
  The field name should be in the 'infos/dimensionless' section of units

materials

signature

******** Skeleton generation from name : generate folder + 'generators' subfolder + library_template.py

******** Strict nomenclature enforcement : where are we?

******** Clean standard-cad-parts from useless code

More library checks ?
  ******** Metadata is the same for each part (the list of fields is also returned)
  ******** Check units are coherent (every field linked to a unit)

API:
  add field
  remove field

UI standalone parcours librairie
UI web parcours librairies

Questions:
----------

Comment gérer un profilé standard mais de longueur non définie?