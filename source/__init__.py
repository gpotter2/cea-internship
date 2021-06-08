"""
A ProgramableSource object to read H5DF files into paraview
"""

# Config

PATH_TO_NPY = "/home/gpotter/pv_work/npy_files/"

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

from paraview.simple import *
import os
__DIR__ = os.path.abspath(os.path.dirname(__file__))

HEADER = """
def get_path(name):
    return os.path.abspath(os.path.join('%s', name))
""" % PATH_TO_NPY

def process(data):
    return HEADER + data

source = ProgrammableSource()
source.OutputDataSetType = 'vtkTable'
with open(os.path.join(__DIR__, 'script.py')) as fd:
    source.Script = process(fd.read())
with open(os.path.join(__DIR__, 'reqscript.py')) as fd:
    source.ScriptRequestInformation = process(fd.read())
source.PythonPath = "'/home/gpotter/.python/lib/python3.6/site-packages'"
