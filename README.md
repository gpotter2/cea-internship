# Visualisation of plasma mirrors

- `convert_hdf5/` contains a util script to convert a custom HDF5 format to Numpy arrays.
- `process_data` contains the pre-processing that propagates the data and creates the frames.
- `source/` contains a paraview ProgrammableSource that displays the content of the generated frames.

## How to use:

1. Build the numpy files using the convert hdf5 tools
2. Process the data by calling `process_data/process.py`
3. In paraview, run the `source/__init__.py` script to import the ProgrammableSource.
