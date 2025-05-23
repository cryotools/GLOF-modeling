#!/Users/tsauter/anaconda/bin/python
# Purpose: Export 3D objects, build of faces with 3 or 4 vertices, as ASCII or Binary STL file.
# License: MIT License

import struct

from osgeo.gdalconst import *
from osgeo import gdal
import optparse
from tqdm import tqdm


ASCII_FACET = """facet normal 0 0 0
outer loop
vertex {face[0][0]:.4f} {face[0][1]:.4f} {face[0][2]:.4f}
vertex {face[1][0]:.4f} {face[1][1]:.4f} {face[1][2]:.4f}
vertex {face[2][0]:.4f} {face[2][1]:.4f} {face[2][2]:.4f}
endloop
endfacet
"""

BINARY_HEADER = "80sI"
BINARY_FACET = "12fH"

class ASCII_STL_Writer:
    """ Export 3D objects build of 3 or 4 vertices as ASCII STL file.
    """
    def __init__(self, stream):
        self.fp = stream
        self._write_header()

    def _write_header(self):
        self.fp.write("solid valley\n")

    def close(self):
        self.fp.write("endsolid valley\n")

    def _write(self, face):
        self.fp.write(ASCII_FACET.format(face=face))

    def _split(self, face):
        p1, p2, p3, p4 = face
        return (p1, p2, p3), (p3, p4, p1)

    def add_face(self, face):
        """ Add one face with 3 or 4 vertices. """
        if len(face) == 4:
            face1, face2 = self._split(face)
            self._write(face1)
            self._write(face2)
        elif len(face) == 3:
            self._write(face)
        else:
            raise ValueError('only 3 or 4 vertices for each face')

    def add_faces(self, faces):
        """ Add many faces. """
        for face in faces:
            self.add_face(face)

class Binary_STL_Writer(ASCII_STL_Writer):
    """ Export 3D objects build of 3 or 4 vertices as binary STL file.
    """
    def __init__(self, stream):
        self.counter = 0
        super(Binary_STL_Writer, self).__init__(stream)

    def close(self):
        self._write_header()

    def _write_header(self):
        self.fp.seek(0)
        self.fp.write(struct.pack(BINARY_HEADER, b'Python Binary STL Writer', self.counter))

    def _write(self, face):
        self.counter += 1
        data = [
            0., 0., 0.,
            face[0][0], face[0][1], face[0][2],
            face[1][0], face[1][1], face[1][2],
            face[2][0], face[2][1], face[2][2],
            0
        ]
        self.fp.write(struct.pack(BINARY_FACET, *data))

def example():
    def read_mask(maskFile):
        mask = gdal.Open(maskFile, GA_ReadOnly )
        bandMask = mask.GetRasterBand(1)

        # Reading the raster properties  
        projectionfromMask = mask.GetProjection() 
        geotransformMask = mask.GetGeoTransform()
        xsizeMask = bandMask.XSize
        ysizeMask = bandMask.YSize
        datatypeMask = bandMask.DataType

        valuesMask = bandMask.ReadAsArray()
        valuesMask[valuesMask >= 10000] = 0

        extentMask = (geotransformMask[0], geotransformMask[0] + \
                      mask.RasterXSize * geotransformMask[1], \
                      geotransformMask[3] + mask.RasterYSize * \
                      geotransformMask[5], geotransformMask[3])

        print(extentMask)
        print ("... DONE")
        print ("-------------------------------\n")

        ptMask = []

        for y in tqdm(range(0,ysizeMask-1)):
            for x in tqdm(range(0,xsizeMask-1), leave=False):

                p1 = ((x*geotransformMask[1], ((ysizeMask-1)*abs(geotransformMask[5]))+
                       y*geotransformMask[5], valuesMask[y,x]))
                p2 = (((x+1)*geotransformMask[1], ((ysizeMask-1)*abs(geotransformMask[5]))+
                       y*geotransformMask[5], valuesMask[y,(x+1)]))
                p3 = (((x+1)*geotransformMask[1], ((ysizeMask-1)*abs(geotransformMask[5]))+
                       (y+1)*geotransformMask[5], valuesMask[(y+1),(x+1)]))
                p4 = ((x*geotransformMask[1], ((ysizeMask-1)*abs(geotransformMask[5]))+
                       (y+1)*geotransformMask[5], valuesMask[(y+1),x]))

                if not (valuesMask[y,x] == 0):
                    ptMask.append([p1,p2,p3,p4])

        return ptMask

    mask = read_mask("valley.tif")

    with open('valley.stl', 'w') as fp:
        writer = ASCII_STL_Writer(fp)

        for face in mask:
            # Überprüfe, ob alle Punkte der Facette einen Wert ungleich Null haben
            if all(point[2] != 0 for point in face):
                writer.add_face(face)

        writer.close()

if __name__ == '__main__':
    example()
