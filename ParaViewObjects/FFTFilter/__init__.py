
"""
A ParaView ProgrammableFilter that filters harmonices using FFTs
"""

from paraview.simple import *

import sys, os
__DIR__ = os.path.abspath(os.path.dirname(__file__))

def getFFTFilter(Input, inField):
    source = ProgrammableFilter(Input=Input, registrationName='FFTFilter')
    source.OutputDataSetType = 'Same as Input'
    HEADER = """
self.inField = "%s"
self.outFieldHigh = "%s"
self.outFieldLow = "%s"
    """.strip() % (
        inField,
        inField + "_h",
        inField + "_l",
    )
    with open(os.path.join(__DIR__, 'script_filter.py')) as fd:
        source.Script = "\n".join([HEADER, fd.read()])
    with open(os.path.join(__DIR__, 'reqscript_filter.py')) as fd:
        source.RequestInformationScript = fd.read()

    # Trigger RequestInformation
    source.UpdatePipelineInformation()
    return source
