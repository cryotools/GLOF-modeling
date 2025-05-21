#!/Users/tsauter/anaconda/bin/python
# Purpose: Export 3D objects, build of faces with 3 or 4 vertices, as ASCII or Binary STL file.
# License: MIT License
import os
import struct
import glob
from osgeo.gdalconst import *  
from osgeo import gdal 
from osgeo import ogr
import numpy as np
import optparse
import sys

ASCII_FACET = """facet normal 0 0 0
outer loop
vertex {face[0][0]:.4f} {face[0][1]:.4f} {face[0][2]:.4f}
vertex {face[1][0]:.4f} {face[1][1]:.4f} {face[1][2]:.4f}
vertex {face[2][0]:.4f} {face[2][1]:.4f} {face[2][2]:.4f}
endloop
endfacet
"""


# # Funktion zum Ausführen der Skripte
# def execute_scripts(folder):
#     scripts = ['stlWriter_lake.py', 'stlWriter_valley.py', 'stlExtrude_valley.py', 'stlExtrude_lake.py']
#     for script in scripts:
#         script_path = os.path.join(folder, script)
#         if os.path.exists(script_path):
#             print(f"Ausführen von {script} im Ordner {folder}")
#             try:
#                 with open(script_path, 'r') as f:
#                     script_code = f.read()
#                 exec(script_code)
#             except Exception as e:
#                 print(f"Fehler beim Ausführen von {script}: {e}")
#         else:
#             print(f"Skript {script} nicht gefunden im Ordner {folder}")

# # Hauptfunktion zum Iterieren durch Ordner und Ausführen der Skripte
# def process_folders(root_folder):
#     for root, dirs, files in os.walk(root_folder):
#         if 'terrain' in dirs:
#             terrain_folder = os.path.join(root, 'terrain')
#             execute_scripts(terrain_folder)

# # Hauptprogramm
# if __name__ == "__main__":
#     root_folder = '/data/scratch/furiawil/Dissertation/OpenFOAM/big_runs'
#     process_folders(root_folder)

BINARY_HEADER ="80sI"
BINARY_FACET = "12fH"


class ASCII_STL_Writer:
    """ Export 3D objects build of 3 or 4 vertices as ASCII STL file.
    """
    def __init__(self, stream):
        self.fp = stream
        self._write_header()

    def _write_header(self):
        self.fp.write("solid python\n")

    def close(self):
        self.fp.write("endsolid python\n")

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


def example(DEMfile,maskFile, elevation):

    #---------------------------------------------------
    # Read digital elevation model from file and create
    # plot
    #---------------------------------------------------
    def read_dem(DEMfile, maskFile):

        print ("-------------------------------")
        print ("Reading entire domain")
        print ("-------------------------------\n")
        print ("... %s" % DEMfile)

        # Opening the raster file  
        dataset = gdal.Open(DEMfile, GA_ReadOnly )  
        band = dataset.GetRasterBand(1)  

        # Reading the raster properties  
        projectionfrom = dataset.GetProjection() 
        geotransform = dataset.GetGeoTransform()  
        xsize = band.XSize  
        ysize = band.YSize  
        datatype = band.DataType  

        # Reading the raster values  
        values = band.ReadAsArray()  
        values[values >= 10000] = 0

        # Get extent of the DEM
        extent = (geotransform[0], geotransform[0] + \
                  dataset.RasterXSize * geotransform[1], \
                  geotransform[3] + dataset.RasterYSize * \
                  geotransform[5], geotransform[3])

        print(extent)	
        print ("-------------------------------")
        print ("Reading mask")
        print ("-------------------------------\n")
        print ("... %s" % maskFile)

        # Opening the raster file  
        mask = gdal.Open(maskFile, GA_ReadOnly )  
        bandMask = mask.GetRasterBand(1)  

        # Reading the raster properties  
        projectionfromMask = mask.GetProjection() 
        geotransformMask = mask.GetGeoTransform()  
        xsizeMask = bandMask.XSize  
        ysizeMask = bandMask.YSize  
        datatypeMask = bandMask.DataType  

        # Reading the raster values  
        valuesMask = bandMask.ReadAsArray()  
        valuesMask[valuesMask >= 10000] = 0
        values[values>-99] = elevation

        # Get extent of the DEM
        extentMask = (geotransformMask[0], geotransformMask[0] + \
                      mask.RasterXSize * geotransformMask[1], \
                      geotransformMask[3] + mask.RasterYSize * \
                      geotransformMask[5], geotransformMask[3])

        print(extentMask)	
        print ("... DONE")
        print ("-------------------------------\n")

        #ptDomain = []
        ptMask = []

        for y in range(0,ysize-1):
            for x in range(0,xsize-1):

                p1 = ((x*geotransform[1], ((ysize-1)*abs(geotransform[5]))+
                       y*geotransform[5], values[y,x]))
                p2 = (((x+1)*geotransform[1], ((ysize-1)*abs(geotransform[5]))+
                       y*geotransform[5], values[y,(x+1)]))
                p3 = (((x+1)*geotransform[1], ((ysize-1)*abs(geotransform[5]))+
                       (y+1)*geotransform[5], values[(y+1),(x+1)]))
                p4 = ((x*geotransform[1], ((ysize-1)*abs(geotransform[5]))+
                       (y+1)*geotransform[5], values[(y+1),x]))

                if not (valuesMask[y,x] == 0):
                    ptMask.append([p1,p2,p3,p4])

        return (ptMask)


    def get_cube():
        # cube corner points
        s = 3.
        p1 = (0, 0, 0)
        p2 = (0, 0, s)
        p3 = (0, s, 0)
        p4 = (0, s, s)
        p5 = (s, 0, 0)
        p6 = (s, 0, s)
        p7 = (s, s, 0)
        p8 = (s, s, s)

        # define the 6 cube faces
        # faces just lists of 3 or 4 vertices
        return [
            [p1, p5, p7, p3],
            [p1, p5, p6, p2],
            [p5, p7, p8, p6],
            [p7, p8, p4, p3],
            [p1, p3, p4, p2],
            [p2, p6, p8, p4],
        ]

    subset = read_dem(DEMfile,maskFile) 
    mask = subset


    with open('lake.stl', 'w') as fp:
        writer = ASCII_STL_Writer(fp)
        writer.add_faces(mask)
        writer.close()




if __name__ == '__main__':
    # Finde die DEM-Datei
    DEMfile_candidates = glob.glob("DEM*.tif")

    # Überprüfe, ob mindestens eine passende Datei gefunden wurde
    if not DEMfile_candidates:
        print("Keine passende DEM-Datei gefunden.")
        sys.exit(1)

    # Wähle die erste gefundene Datei aus
    DEMfile = DEMfile_candidates[0]
    maskFile = "lake.tif"
    
    # Lies den Parameter "elevation" aus der Datei "elevation"
    try:
        with open("elevation", "r") as file:
            elevation = int(file.read().strip())
    except FileNotFoundError:
        print("Die Datei 'elevation' wurde nicht gefunden.")
        sys.exit(1)
    except ValueError:
        print("Der Inhalt von 'elevation' ist keine gültige Ganzzahl.")
        sys.exit(1)

    example(DEMfile, maskFile, elevation)

