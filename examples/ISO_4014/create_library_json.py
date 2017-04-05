#!/usr/bin/python
# coding: utf-8

r"""Script that creates the library.json file for the ISO 4014 standard"""


import logging
from party.library_creation import template_handle_generators, \
    template_handle_aliases
from party.rules_checking import check_library_json

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s :: %(levelname)6s :: '
                               '%(module)20s :: %(lineno)3d :: %(message)s')

    logger.info("Creating the library JSON from its template ...")

    template_handle_generators(file_in='library_template.json',
                               file_out='library_template_.json')

    logger.info("... done")

    logger.info("Handling aliases in JSON template")

    template_handle_aliases(file_in='library_template_.json',
                            file_out='library.json')

    logger.info("... done")

    logger.info("Checking the rules for the library JSON ...")
    ok, errors = check_library_json(json_filename='library.json')
    if ok:
        logger.info("... done. Rules are OK")
    else:
        logger.error("The library contains errors, please correct these before "
                     "generating the scripts")
        print(errors)
