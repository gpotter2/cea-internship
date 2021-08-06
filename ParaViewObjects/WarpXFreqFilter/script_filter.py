"""
The 'Script' parameter of a ProgrammableFilter
"""

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

import numpy as np

input0 = inputs[0]

def apply_log_scale(data, threshold):
    low = data < -threshold
    high = data > threshold
    mid = (data >= -threshold) & (data <= threshold)
    data[low] = -np.log10(-data[low])
    data[high] = np.log10(data[high])
    data[mid] = 0.


dataArray2 = input0.CellData[self.inField2]
dataArray1 = input0.CellData[self.inField1] - dataArray2

apply_log_scale(dataArray2, 1)
apply_log_scale(dataArray1, 1)

output.CellData.append(dataArray1, self.outField)
output.CellData.append(dataArray2, self.inField2)
