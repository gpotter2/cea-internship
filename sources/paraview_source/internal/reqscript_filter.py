"""
The 'RequestInformation Script' parameter of a ProgrammableFilter
"""

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

import numpy as np

import vtk

def build_grid_params(xsize, xpad,
                      ysize, ypad,
                      zsize, zpad):
    # Build frequences grid
    freqx = np.fft.fftfreq(xsize, d=xpad)
    freqy = np.fft.fftfreq(ysize, d=ypad)
    freqz = np.fft.fftfreq(zsize, d=zpad)

    KX, KY, KZ = np.meshgrid(freqx, freqy, freqz, indexing='ij')
    return KX, KY, KZ


# Get output
executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)

whole_extent = outInfo.Get(executive.WHOLE_EXTENT())
spacing = outInfo.Get(vtk.vtkDataObject.SPACING())

KX, KY, KZ = build_grid_params(
    whole_extent[1] - whole_extent[0] + 1, spacing[0],
    whole_extent[3] - whole_extent[2] + 1, spacing[1],
    whole_extent[5] - whole_extent[4] + 1, spacing[2],
)
W = np.sqrt(KX**2 + KY**2 + KZ**2)
L = np.max(W)
self.propag_high = (W < L//2).ravel()
self.propag_low = (W > L//4).ravel()
