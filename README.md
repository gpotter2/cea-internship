# Visualisation of plasma mirrors

- `convert_hdf5/` contains a util script to convert a custom HDF5 format to Numpy arrays.
- `process_data` contains the pre-processing that propagates the data and creates the frames.
- `sources/`:
  - `paraview_source/` -> NOT IN SITU
    - `main.py`: contains a paraview ProgrammableSource that read frames as files. Those frames
      are generated using the scripts in `process_data`.
    - `debug.py`: contains a paraview ProgrammableSource to be used in Debug mode (set `DEBUG_GAUSSIAN_BEAM`)
      in the config. This displays a gaussian beam (also read from files).
    - `utils.py`: some functions used by the two
    - `internal/`: contains the content of the ProgrammableSource, and the `paraview_ascent_source` linker.
  - `ascent_source/` -> IN SITU
    - `ascent-fft-filter.py`: a python script called using ascent's`add_extracts` that does filters the data
      then displays it.
    - `ascent-paraview-insitu.py`: a python script called by the previous fft-filter script when used in paraview mode
      that displays the data into paraview.
    - `ascent_actions/`: various `ascent_actions.yaml` examples

## How to use (NOT IN SITU)

1. Build the numpy files using the convert hdf5 tools
2. Process the data by calling `process_data/process.py`
3. In paraview, run the `source/__init__.py` script to import the ProgrammableSource.

## How to use (IN SITU)

1. Copy `ascent_source/ascent_actions/ascent_actions_fftfilter.yaml` to your `ascent_actions.yaml`
2. Setup all the paths properly inside the files
3. Run WarpX
