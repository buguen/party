#!/usr/bin/python
# coding: utf-8

r"""Parts library documentation creation example"""

from os.path import dirname, join
import logging

from party.library_documentation import create_libraries_sphinx_sources


def main():
    r"""Main function for the parts library documentation example"""
    create_libraries_sphinx_sources(join(dirname(__file__), "../examples"),
                                    join(dirname(__file__), "../examples/doc"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s :: %(levelname)6s :: '
                               '%(module)20s :: %(lineno)3d :: %(message)s')

    main()
