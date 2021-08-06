
"""
A ParaView Filter that performs some formatting for WarpX output.

Performs:
    (F1, F2) -> (log10(F1 - F2), log10(F2))
"""

from paraview.simple import *

import sys, os
__DIR__ = os.path.abspath(os.path.dirname(__file__))

def getFormatFilter(Input, inField1, inField2, outField):
    source = ProgrammableFilter(Input=Input, registrationName='DiffAndLogFilter')
    source.OutputDataSetType = 'Same as Input'
    HEADER = """
self.inField1 = "%s"
self.inField2 = "%s"
self.outField = "%s"
    """.strip() % (
        inField1,
        inField2,
        outField,
    )
    with open(os.path.join(__DIR__, 'script_filter.py')) as fd:
        source.Script = "\n".join([HEADER, fd.read()])

    # Trigger RequestInformation
    source.UpdatePipelineInformation()
    return source
