# state file generated using paraview version 5.9.1-1209-ge0ef3e4

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

# get the material library
materialLibrary1 = GetMaterialLibrary()

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [444, 256]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.CenterOfRotation = [11.461944715734068, 11.63848523809543, 4.0543999999995535]
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [-14.566306453816017, 11.638485238095432, 19.63698006349911]
renderView1.CameraFocalPoint = [11.461944715734065, 11.638485238095432, 4.0543999999995535]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 16.83058747233458
renderView1.BackEnd = 'OSPRay raycaster'
renderView1.OSPRayMaterialLibrary = materialLibrary1

# init the 'GridAxes3DActor' selected for 'AxesGrid'
renderView1.AxesGrid.Visibility = 1

SetActiveView(None)

# ----------------------------------------------------------------
# setup view layouts
# ----------------------------------------------------------------

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.AssignView(0, renderView1)
layout1.SetSize(444, 256)

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView1)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'Programmable Source'
programmableSource1 = ProgrammableSource(registrationName='ProgrammableSource1')
programmableSource1.OutputDataSetType = 'vtkImageData'
programmableSource1.Script = """ 
### GENERATED HEADER ###
import os
activate_this="/home/gpotter/.miniconda3/bin/activate_this.py"
exec(open(activate_this).read(), dict(__file__=activate_this))

def get_path(x, folder=""):
    return os.path.abspath(os.path.join("/mnt/scratch/gpotter/field3d", folder, x))

dz = -10
zlength = -1
MAX_TIME = 100
x_drop = 2
y_drop = 2
time_drop = 8
 
### END OF HEADER ###

\"\"\"
The \'Script\' parameter of a ProgrammableSource
\"\"\"

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

import numpy as np

executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)

# A util to get the current timestamp
def GetUpdateTimestep():
    \"\"\"
    Returns the requested time value, or None if not present
    \"\"\"
    return outInfo.Get(executive.UPDATE_TIME_STEP()) \\
              if outInfo.Has(executive.UPDATE_TIME_STEP()) else None

# Build time index
req_time = int((
    (GetUpdateTimestep() or 0)) / abs(dz)
)

# Configure output
exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
output.SetExtent(exts)

# Get data at specific timeframe
fnpz = np.load(get_path("f%s.npz" % req_time, "frames"))
data = fnpz[\'frame\']
fnpz.close()

# DEBUG: fill space with first plane
# data = data[:,:,0]
# data = np.broadcast_to(data[..., np.newaxis],
#                        data.shape + (self.zlength,))

# Generate points grid (not required on images)
# from vtk.numpy_interface import dataset_adapter as dsa
# pts = vtk.vtkPoints()
# pts.SetData(dsa.numpyTovtkDataArray(self.points, "Points"))

output.PointData.append(data.ravel(order="F"), "By")
output.PointData.SetActiveScalars("By")

# Set current timestamp
output.GetInformation().Set(output.DATA_TIME_STEP(), req_time)
"""
programmableSource1.ScriptRequestInformation = """
### GENERATED HEADER ###
import os
activate_this="/home/gpotter/.miniconda3/bin/activate_this.py"
exec(open(activate_this).read(), dict(__file__=activate_this))

def get_path(x, folder=""):
    return os.path.abspath(os.path.join("/mnt/scratch/gpotter/field3d", folder, x))

dz = -10
zlength = -1
MAX_TIME = 100
x_drop = 2
y_drop = 2
time_drop = 8

### END OF HEADER ###

\"\"\"
The \'RequestInformation Script\' parameter of a ProgrammableSource
\"\"\"

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

import builtins
import glob

import numpy as np

# Configure output
executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)

# Count frames
self.nbframes = builtins.sum(1 for _ in glob.iglob(get_path("*", "frames")))

# Read axis
self.x = np.load(get_path("x.npy", "npy_files"))[::x_drop]
self.y = np.load(get_path("y.npy", "npy_files"))[::y_drop]
self.t = np.load(get_path("t.npy", "npy_files"))[::time_drop]

self.zlength = self.t.shape[0] if zlength < 1 else zlength

## Define re-usable grid
#X, Y, Z = np.meshgrid(self.x, self.y, self.z)
#self.points = algs.make_vector(X.ravel(),
#                               Y.ravel(),
#                               Z.ravel())

# Set boundaries
outInfo.Set(executive.WHOLE_EXTENT(),
    # (xmin, xmax, ymin, ymax, zmin, zmax)
    0, self.x.shape[0] - 1,
    0, self.y.shape[0] - 1,
    0, self.zlength - 1
)
outInfo.Set(vtk.vtkDataObject.SPACING(),
    # (dx, dy, dz)
    self.x[1] - self.x[0],
    self.y[1] - self.y[0],
    self.t[1] - self.t[0]
)

MAX_TIME = builtins.min(self.nbframes, MAX_TIME)

# Set time steps
outInfo.Remove(executive.TIME_STEPS())
for timestep in range(0, MAX_TIME):
    outInfo.Append(executive.TIME_STEPS(), timestep * abs(dz))

outInfo.Remove(executive.TIME_RANGE())
outInfo.Append(executive.TIME_RANGE(), 0)
outInfo.Append(executive.TIME_RANGE(), MAX_TIME)
"""
programmableSource1.PythonPath = ''

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=programmableSource1)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [11.461944715734068, 11.63848523809543, 4.0543999999995535]
slice1.SliceType.Offset = 7.0

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice1.HyperTreeGridSlicer.Origin = [11.461944715734068, 11.63848523809543, 4.0543999999995535]

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from programmableSource1
programmableSource1Display = Show(programmableSource1, renderView1, 'UniformGridRepresentation')

# get color transfer function/color map for 'By'
byLUT = GetColorTransferFunction('By')
byLUT.AutomaticRescaleRangeMode = 'Never'
byLUT.EnableOpacityMapping = 1
byLUT.RGBPoints = [-0.009310164488852024, 0.231373, 0.298039, 0.752941, -0.0024102458264678717, 0.5058823529411764, 0.6431372549019608, 0.984313725490196, 0.0, 0.865003, 0.865003, 0.865003, 0.0010869731195271015, 0.8352941176470589, 0.3137254901960784, 0.25882352941176473, 0.009310164488852024, 0.705882, 0.0156863, 0.14902]
byLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'By'
byPWF = GetOpacityTransferFunction('By')
byPWF.Points = [-0.009310164488852024, 1.0, 0.5, 0.0, -0.00311914156191051, 1.0, 0.5, 0.0, -0.0014177918201312423, 0.0, 0.5, 0.0, 4.725941107608378e-05, 0.0, 0.5, 0.0, 0.0008506745798513293, 0.0, 0.5, 0.0, 0.0012760120443999767, 1.0, 0.5, 0.0, 0.009310164488852024, 1.0, 0.5, 0.0]
byPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
programmableSource1Display.Representation = 'Volume'
programmableSource1Display.ColorArrayName = ['POINTS', 'By']
programmableSource1Display.LookupTable = byLUT
programmableSource1Display.SelectTCoordArray = 'None'
programmableSource1Display.SelectNormalArray = 'None'
programmableSource1Display.SelectTangentArray = 'None'
programmableSource1Display.OSPRayScaleArray = 'By'
programmableSource1Display.OSPRayScaleFunction = 'PiecewiseFunction'
programmableSource1Display.SelectOrientationVectors = 'None'
programmableSource1Display.ScaleFactor = 2.327697047619086
programmableSource1Display.SelectScaleArray = 'By'
programmableSource1Display.GlyphType = 'Arrow'
programmableSource1Display.GlyphTableIndexArray = 'By'
programmableSource1Display.GaussianRadius = 0.1163848523809543
programmableSource1Display.SetScaleArray = ['POINTS', 'By']
programmableSource1Display.ScaleTransferFunction = 'PiecewiseFunction'
programmableSource1Display.OpacityArray = ['POINTS', 'By']
programmableSource1Display.OpacityTransferFunction = 'PiecewiseFunction'
programmableSource1Display.DataAxesGrid = 'GridAxesRepresentation'
programmableSource1Display.PolarAxes = 'PolarAxesRepresentation'
programmableSource1Display.ScalarOpacityUnitDistance = 0.06772190769700204
programmableSource1Display.ScalarOpacityFunction = byPWF
programmableSource1Display.OpacityArrayName = ['POINTS', 'By']
programmableSource1Display.IsosurfaceValues = [-0.002422813093289733]
programmableSource1Display.SliceFunction = 'Plane'
programmableSource1Display.Slice = 90

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
programmableSource1Display.ScaleTransferFunction.Points = [-0.009310164488852024, 0.0, 0.5, 0.0, 0.004464538302272558, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
programmableSource1Display.OpacityTransferFunction.Points = [-0.009310164488852024, 0.0, 0.5, 0.0, 0.004464538302272558, 1.0, 0.5, 0.0]

# init the 'Plane' selected for 'SliceFunction'
programmableSource1Display.SliceFunction.Origin = [11.461944715734068, 11.63848523809543, 4.0543999999995535]

# show data from slice1
slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')

# get separate color transfer function/color map for 'By'
separate_slice1Display_ByLUT = GetColorTransferFunction('By', slice1Display, separate=True)
separate_slice1Display_ByLUT.AutomaticRescaleRangeMode = 'Never'
separate_slice1Display_ByLUT.RGBPoints = [-9.742920519784093e-05, 0.231373, 0.298039, 0.752941, 0.0, 0.865003, 0.865003, 0.865003, 9.742920519784093e-05, 0.705882, 0.0156863, 0.14902]
separate_slice1Display_ByLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['POINTS', 'By']
slice1Display.LookupTable = separate_slice1Display_ByLUT
slice1Display.SelectTCoordArray = 'None'
slice1Display.SelectNormalArray = 'None'
slice1Display.SelectTangentArray = 'None'
slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice1Display.SelectOrientationVectors = 'None'
slice1Display.ScaleFactor = -2.0000000000000002e+298
slice1Display.SelectScaleArray = 'None'
slice1Display.GlyphType = 'Arrow'
slice1Display.GlyphTableIndexArray = 'None'
slice1Display.GaussianRadius = -1e+297
slice1Display.SetScaleArray = [None, '']
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityArray = [None, '']
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'
slice1Display.DataAxesGrid = 'GridAxesRepresentation'
slice1Display.PolarAxes = 'PolarAxesRepresentation'

# set separate color map
slice1Display.UseSeparateColorMap = True

# setup the color legend parameters for each legend in this view

# get color legend/bar for byLUT in view renderView1
byLUTColorBar = GetScalarBar(byLUT, renderView1)
byLUTColorBar.WindowLocation = 'AnyLocation'
byLUTColorBar.Position = [0.8744588744588745, 0.023076923076923078]
byLUTColorBar.Title = 'By'
byLUTColorBar.ComponentTitle = ''
byLUTColorBar.ScalarBarLength = 0.32999999999999996

# set color bar visibility
byLUTColorBar.Visibility = 1

# get color legend/bar for separate_slice1Display_ByLUT in view renderView1
separate_slice1Display_ByLUTColorBar = GetScalarBar(separate_slice1Display_ByLUT, renderView1)
separate_slice1Display_ByLUTColorBar.Title = 'By'
separate_slice1Display_ByLUTColorBar.ComponentTitle = ''

# set color bar visibility
separate_slice1Display_ByLUTColorBar.Visibility = 1

# show color legend
programmableSource1Display.SetScalarBarVisibility(renderView1, True)

# show color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get separate opacity transfer function/opacity map for 'By'
separate_slice1Display_ByPWF = GetOpacityTransferFunction('By', slice1Display, separate=True)
separate_slice1Display_ByPWF.Points = [-9.742920519784093e-05, 1.0, 0.5, 0.0, -1.4836941437355595e-06, 0.0, 0.5, 0.0, 9.742920519784093e-05, 1.0, 0.5, 0.0]
separate_slice1Display_ByPWF.ScalarRangeInitialized = 1

# ----------------------------------------------------------------
# restore active source
SetActiveSource(slice1)
# ----------------------------------------------------------------


if __name__ == '__main__':
    # generate extracts
    SaveExtracts(ExtractsOutputDirectory='extracts')