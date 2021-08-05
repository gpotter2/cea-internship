"""
CLI tool to convert a .npy 3D matrix into a vtkImageData openable by paraview
"""

import argparse
import sys

import vtk
import numpy as np
from vtk.util import numpy_support

parser = argparse.ArgumentParser(description='Convert NPY to vtkImageData')
parser.add_argument('src', type=str, nargs=1,
                    help='the file to convert')
parser.add_argument('dst', type=str, nargs=1,
                    help='the destination file')
args = parser.parse_args()

if args.dst[0][-4:] != ".vti":
    print("Destination file must have .vti format !")
    sys.exit(1)

# Based on https://stackoverflow.com/a/61563445
def numpy_array_as_vtk_image_data(source_numpy_array):
    """
    :param source_numpy_array: source array with 2-3 dimensions.
    :type source_numpy_array: np.ndarray
    :return: vtk-compatible image, if conversion is successful. Raises exception otherwise
    :rtype vtk.vtkImageData
    """

    output_vtk_image = vtk.vtkImageData()
    output_vtk_image.SetDimensions(source_numpy_array.shape[0], source_numpy_array.shape[1], source_numpy_array.shape[2])

    vtk_type_by_numpy_type = {
        np.bool_: vtk.VTK_UNSIGNED_CHAR,
        np.uint8: vtk.VTK_UNSIGNED_CHAR,
        np.uint16: vtk.VTK_UNSIGNED_SHORT,
        np.uint32: vtk.VTK_UNSIGNED_INT,
        np.uint64: vtk.VTK_UNSIGNED_LONG if vtk.VTK_SIZEOF_LONG == 64 else vtk.VTK_UNSIGNED_LONG_LONG,
        np.int8: vtk.VTK_CHAR,
        np.int16: vtk.VTK_SHORT,
        np.int32: vtk.VTK_INT,
        np.int64: vtk.VTK_LONG if vtk.VTK_SIZEOF_LONG == 64 else vtk.VTK_LONG_LONG,
        np.float32: vtk.VTK_FLOAT,
        np.float64: vtk.VTK_DOUBLE
    }
    vtk_datatype = vtk_type_by_numpy_type[source_numpy_array.dtype.type]

    depth_array = numpy_support.numpy_to_vtk(source_numpy_array.ravel(order="F"), deep=True, array_type = vtk_datatype)
    output_vtk_image.SetSpacing([1, 1, 1])
    output_vtk_image.SetOrigin([-1, -1, -1])
    output_vtk_image.GetPointData().SetScalars(depth_array)

    output_vtk_image.Modified()
    return output_vtk_image

ndarray = np.load(args.src[0])
image_data = numpy_array_as_vtk_image_data(ndarray)

writer = vtk.vtkXMLImageDataWriter()
writer.SetInputData(image_data)
writer.SetFileName(args.dst[0])
writer.Write()
print("File written...")
