"""
The 'Script' parameter of a ProgrammableFilter
"""

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

try:
    import cupy as cp
    import cupyx as cpx
except ImportError:
    raise ImportError("Please install ``cupy`` !")

input0 = inputs[0]

dataArray = input0.CellData[self.inField]

def apply_log_scale(data, threshold):
    low = data < -threshold
    high = data > threshold
    mid = (data >= -threshold) & (data <= threshold)
    data[low] = -np.log10(-data[low])
    data[high] = np.log10(data[high])
    data[mid] = 0.
    
by = cp.asarray(dataArray,
                dtype="float64")
byfft_high = cpx.scipy.fft.fftn(by,
                                axes=(0,1,2),
                                overwrite_x=True)
del by  # free
byfft_low = cp.copy(byfft_high)
byfft_low[self.propag_low] = 0.
byfft_high[self.propag_high] = 0.
byfft_high = cp.real(cpx.scipy.fft.ifftn(byfft_high,
                                         axes=(0,1,2),
                                         overwrite_x=True)).get()
byfft_low = cp.real(cpx.scipy.fft.ifftn(byfft_low,
                                        axes=(0,1,2),
                                        overwrite_x=True)).get()

apply_log_scale(byfft_high, 1)
apply_log_scale(byfft_low, 1)

output.PointData.append(byfft_high, self.outFieldHigh)
output.PointData.append(byfft_low, self.outFieldLow)
