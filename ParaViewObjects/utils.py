"""
Some ParaView util functions
"""

from paraview.simple import *


def showField(source,
              field="By",
              COLOR="Cool to Warm (Extended)",
              OPACITY=1.0,
              CLIM=1,
              THRESHOLD=0.2):
    """
    Configure and return a ParaView view
    """
    view = GetActiveView()
    displayProperties = Show(source, view)
    
    # Display properties
    displayProperties.Representation = 'Volume'

    ColorBy(displayProperties, ("CELLS", field), separate=True)

    # Color table
    byLUT = GetColorTransferFunction(field, displayProperties, separate=True)
    byLUT.ApplyPreset(COLOR)
    byLUT.RescaleTransferFunction(-CLIM, CLIM, True)
    byLUT.AutomaticRescaleRangeMode = 'Never'

    # Opacity map
    byPWF = GetOpacityTransferFunction(field, displayProperties, separate=True)
    byPWF.Points = [
        # format: val, opacity, 0.5, 0.0 (last 2?!)
        -CLIM,      OPACITY, 0.5, 0.,
        -THRESHOLD, OPACITY, 0.5, 0.,
        -THRESHOLD, 0.,      0.5, 0.,
        THRESHOLD,  0.,      0.5, 0.,
        THRESHOLD,  OPACITY, 0.5, 0.,
        CLIM,       OPACITY, 0.5, 0.,
    ]
    byPWF.ScalarRangeInitialized = 1
    
    # Color
    displayProperties.ColorArrayName = field
    displayProperties.LookupTable = byLUT
    
    # Opacity
    displayProperties.OpacityArrayName = field
    displayProperties.ScalarOpacityFunction = byPWF

    # Separate color map
    # displayProperties.UseSeparateColorMap = True

    scalarBar = GetScalarBar(byLUT, view)
    scalarBar.Title = field
    scalarBar.ComponentTitle = ''
    scalarBar.Visibility = 1
    displayProperties.SetScalarBarVisibility(view, True)


def showPoints(source, field="particle_electrons_cpu"):
    view = GetActiveView()
    glyph = Glyph(
        source,
        GlyphType = "Sphere",
        ScaleFactor = 5.753235726125357e-06
    )
    glyph.GlyphType.Radius = 0.05

    displayProperties = Show(glyph, view)
    ColorBy(displayProperties, ("CELLS", field))


def setupView(animated=False):
    view = GetActiveView()

    if animated:
        # Setup animation scene
        animationScene = GetAnimationScene()
        animationScene.PlayMode = 'Snap To TimeSteps'

    # Configure view
    view.ViewSize = [945, 880]
    axesGrid = view.AxesGrid
    axesGrid.Visibility = 1

    # Configure camera
    view.CenterOfRotation = GetActiveCamera().GetFocalPoint()
    #view.CameraPosition = [38.508498092504716, 6.2875904189648475, 22.242265004619007]
    #view.CameraFocalPoint = [7.670000000000014, 7.290000000000007, 11.399999999999999]
    #view.CameraViewUp = [-0.014939444962305284, -0.9986456446556182, -0.04983662703858452]


