import pyvista as pv
import sys
import os
import subprocess

def extrude_stl(input_file, output_folder, elevation):
    # Load the STL file
    surface_mesh = pv.read(input_file)

    # Extrude the surface mesh to the desired elevation
    box = surface_mesh.extrude([0, 0, elevation], capping=False)

    # Add faces for the bottom using the surface mesh
    bottom_faces = surface_mesh.copy()

    # Create top faces by inverting the surface mesh
    inverted_surface_mesh = surface_mesh.copy()
    inverted_surface_mesh.points[:, 2] += elevation
    top_faces = inverted_surface_mesh

    # Export each solid to separate STL files
    box_stl = os.path.join(output_folder, "box.stl")
    top_faces_stl = os.path.join(output_folder, "top_faces.stl")
    bottom_faces_stl = os.path.join(output_folder, "bottom_faces.stl")

    # Save meshes to STL files
    box.save(box_stl, binary=False)  # Save in ASCII mode
    top_faces.save(top_faces_stl, binary=False)  # Save in ASCII mode
    bottom_faces.save(bottom_faces_stl, binary=False)  # Save in ASCII mode

    # Rename solids in STL files
    rename_solid_in_stl(box_stl, "walls")
    rename_solid_in_stl(top_faces_stl, "top_faces")
    rename_solid_in_stl(bottom_faces_stl, "valley")

    return box_stl, top_faces_stl, bottom_faces_stl

def rename_solid_in_stl(stl_file, solid_name):
    
    # Lesen Sie den Inhalt der STL-Datei
    with open(stl_file, 'r') as file:
        content = file.read()

    # Ersetzen Sie den solid-Namen
    new_content = content.replace('Visualization Toolkit generated SLA File', solid_name)

    # Schreiben Sie den modifizierten Inhalt zurück in die Datei
    with open(stl_file, 'w') as file:
        file.write(new_content)


def merge_stl(stl_files, output_stl_file):
    # Combine the contents of all STL files into one
    with open(output_stl_file, 'wb') as out_file:
        for stl_file in stl_files:
            with open(stl_file, 'rb') as in_file:
                out_file.write(in_file.read())

if __name__ == "__main__":
    input_file = "valley.stl"
    output_stl_file = "valley_box.stl"
    elevation = float(10000)

    output_folder = "temp_stl"
    os.makedirs(output_folder, exist_ok=True)

    box_stl, top_faces_stl, bottom_faces_stl = extrude_stl(input_file, output_folder, elevation)

    merge_stl([box_stl, top_faces_stl, bottom_faces_stl], output_stl_file)

    # Clean up temporary STL files
    for stl_file in [box_stl, top_faces_stl, bottom_faces_stl]:
        os.remove(stl_file)

    os.rmdir(output_folder)
