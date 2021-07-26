"""
Entry point for Ascent Insitu
"""

########################
# CONFIG ! IMPORTANT ! #
########################

# __file__ does not work with ascent so add it manually
__file__ = "/home/gpotter/pv_work/paraview_source/ascent-insitu.py"
# The path to the paraview python module. This must have been compiled with the SAME python version
# as everything else ! watch out
PARAVIEW_SITE_PACKAGES = "/home/gpotter/git/paraview-catalyst-build/lib/python3.9/site-packages"

import sys, os
__DIR__ = os.path.abspath(os.path.dirname(__file__))
sys.path.append(__DIR__)
PLUGIN_PATH = os.path.join(__DIR__, "internal", "paraview_ascent_source.py")

sys.path.append(os.path.join(__DIR__, "internal"))
sys.path.append(PARAVIEW_SITE_PACKAGES)

# See https://ascent.readthedocs.io/en/latest/Actions/ParaViewVisualization.html

# Same Python interpreter for all time steps
# We use count for one time initializations
try:
    count = count + 1
except NameError:
    count = 0

if count == 0:
    # Initialization
    import paraview
    paraview.options.batch = True
    paraview.options.symmetric = True
    from paraview.simple import *
    from paraview_ascent_source import write_vtk
    #from paraview.simple import (
    #    ExtractSelection,
    #    GetProperty,
    #    LoadPlugin,
    #    Render,
    #    SaveScreenshot,
    #    SelectCells,
    #    Show,
    #    GetActiveCamera,
    #)
    LoadPlugin(PLUGIN_PATH, remote=True, ns=globals())

    # Setup source
    ascentSource = AscentSource()

    #sel = SelectCells("vtkGhostType < 1", proxy=ascentSource)
    #ExtractSelection(Selection=sel)

    # Configure View
    from utils import getView
    getView(ascentSource, THRESHOLD=0.5)

# Update data
ascentSource.UpdateAscentData()
ascentSource.UpdatePropertyInformation()

cycle = GetProperty(ascentSource, "Cycle").GetElement(0)
rank = GetProperty(ascentSource, "Rank").GetElement(0)
if (rank == 0):
    print(
        "=======================================Called: {} {} {}".format(
            GetProperty(ascentSource, "TimeStep"),
            GetProperty(ascentSource, "Cycle"),
            GetProperty(ascentSource, "Time")))

#dataName = "paraviewdata_{0:04d}.pvd".format(int(cycle))
imageName = "image_{0:04d}.png".format(int(cycle))

Render()
ResetCamera()

#SaveData(dataName, ascentSource)
SaveScreenshot(imageName, ImageResolution=(1024, 1024))
