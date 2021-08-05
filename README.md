# Visualisation of plasma mirrors

- `LocalPropagation/`: tools to propagate locally a matrix
  - `process_data` contains the pre-processing that propagates the data and creates the frames.
  - `main.py`: contains a paraview ProgrammableSource that read frames as files. Those frames
    are generated using the scripts in `process_data`.
  - `debug.py`: contains a paraview ProgrammableSource to be used in Debug mode (set `DEBUG_GAUSSIAN_BEAM`)
    in the config. This displays a gaussian beam (also read from files).
- `InSitu/`: Ascent & Paraview tools or scripts
  - `ascent-paraview-insitu.py`: a python script called by the previous fft-filter script when used in paraview mode
    that displays the data into paraview.
  - `ascent_actions/`: various `ascent_actions.yaml` examples
- `ParaViewObjects/`
  - `utils.py`: some functions used by the scripts to display fields or points
  - `ReadImageSource/`: a programmable source that read files exported locally
  - `FFTFilter/`: a programmable filter that performs frequency filtering

## How to use (NOT IN SITU)

1. Build the numpy files using the convert hdf5 tools
2. Process the data by calling `LocalPropagation/process_data/process.py`
3. In paraview, run the `LocalPropagation/main.py` script to import the ProgrammableSources.

## How to use (IN SITU)

1. Copy `InSitu/ascent_actions/ascent_actions_paraview.yaml` to your `ascent_actions.yaml`
2. Setup all the paths properly inside the files
3. Run WarpX
