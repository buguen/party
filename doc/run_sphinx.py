#!/usr/bin/python
# coding: utf-8

r"""Generate the sphinx documentation"""

from os.path import join, dirname
from os import getcwd, chdir
from subprocess import call


folders = {"source": join(dirname(__file__), "source"),
           "build": join(dirname(__file__), "build")}

# Run sphinx
cwd = getcwd()
chdir(folders["source"])
call(["ls", "-l"])
call("sphinx-apidoc -f -o ./ %s" % join(dirname(__file__), "../party/party"))
call("sphinx-build -b html %s %s" % (folders["source"], folders["build"]))
chdir(cwd)
