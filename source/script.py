"""
The 'Script' parameter of a ProgrammableSource
"""

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

from vtk.numpy_interface import algorithms as algs
from vtk.numpy_interface import dataset_adapter as dsa

def GetUpdateTimestep(algorithm):
    """
    Returns the requested time value, or None if not present
    """
    executive = algorithm.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    return outInfo.Get(executive.UPDATE_TIME_STEP()) \
              if outInfo.Has(executive.UPDATE_TIME_STEP()) else None

req_time = GetUpdateTimestep(self)

output.GetInformation().Set(output.DATA_TIME_STEP(), req_time)
