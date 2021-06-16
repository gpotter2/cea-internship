"""
A ProgramableSource object to read H5DF files into paraview
"""

# Config

PATH_TO_NPY = "/home/gpotter/pv_work/npy_files/"
PATH_TO_FRAMES = "/home/gpotter/pv_work/process_data/frames/"
ACTIVATE_THIS_ENV = "/home/gpotter/.miniconda3/bin/activate_this.py"

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

from paraview.simple import *
import os
__DIR__ = os.path.abspath(os.path.dirname(__file__))

# Read config
import sys, os
sys.path.append(os.path.join(__DIR__, ".."))
from config import dz, zlength, MAX_TIME, time_drop

HEADER = """
### GENERATED HEADER ###
import os
activate_this="%s"
exec(open(activate_this).read(), dict(__file__=activate_this))

def get_path(name, frames=False):
    if frames:
        return os.path.abspath(os.path.join('%s', name))
    return os.path.abspath(os.path.join('%s', name))

dz = %s
zlength = %s
MAX_TIME = %s
time_drop = %s

### END OF HEADER ###

""" % (
    ACTIVATE_THIS_ENV,
    PATH_TO_FRAMES,
    PATH_TO_NPY,
    dz,
    zlength,
    MAX_TIME,
    time_drop
)

def process(data):
    return HEADER + data

source = ProgrammableSource()
source.OutputDataSetType = 'vtkImageData'
with open(os.path.join(__DIR__, 'script.py')) as fd:
    source.Script = process(fd.read())
with open(os.path.join(__DIR__, 'reqscript.py')) as fd:
    source.ScriptRequestInformation = process(fd.read())
