import pyvista as pv
import sys

def extrude_stl(input_file, output_file, elevation):
    # Load the STL file
    surface_mesh = pv.read(input_file)

    # Extrude the surface mesh to the desired elevation
    box = surface_mesh.extrude([0, 0, elevation], capping=False)  # Explicitly set capping to False

    # Add faces for the top using the surface mesh
    top_faces = surface_mesh.copy()

    # Combine the box and top faces
    combined_mesh = box + top_faces

    # Add faces for the bottom using the inverted surface mesh
    bottom_faces = surface_mesh.copy()
    bottom_faces.translate([0, 0, elevation], inplace=False)  # Explicitly set inplace to False

    # Combine the box, top faces, and bottom faces
    final_mesh = combined_mesh + bottom_faces

    # Save the resulting mesh to an STL file
    final_mesh.save(output_file)

if __name__ == "__main__":
    input_file = "lake.stl"
    output_file = "lake_box.stl"
    # Lies den Parameter "elevation" aus der Datei "elevation"
    try:
        with open("elevation", "r") as file:
            elevation = -(int(file.read().strip()))
    except FileNotFoundError:
        print("Die Datei 'elevation' wurde nicht gefunden.")
        sys.exit(1)
    except ValueError:
        print("Der Inhalt von 'elevation' ist keine gültige Ganzzahl.")
        sys.exit(1)
    extrude_stl(input_file, output_file, elevation)
