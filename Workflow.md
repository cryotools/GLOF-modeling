
## ▶️ Workflow Overview

The general workflow consists of the following steps:

1. **Delineation of glacial lake boundaries**  
   Identify and digitize the extent of the glacial lake using satellite imagery or field data.

2. **Identification of potential breach path**  
   Define the most likely breach location across the moraine, based on topography and geomorphological indicators.

3. **Preparation of the digital elevation model (DEM)**  
   Integrate lake and breach morphologies into the DEM.

4. **Conversion of the DEM to STL format**  
   Generate a surface mesh (STL file) to represent the terrain in OpenFOAM.

5. **OpenFOAM simulation setup**  
   - Use `blockMesh` and `snappyHexMesh` to generate the computational mesh  
   - Define the initial water body using `setFields`  
   - Configure and validate boundary conditions  
   - Define baffles for dam break simulations
   - Execute the simulation runs

Each of these steps will be accompanied by the following notes and representative code snippets.

## Part 1 – Glacial Lake Delineation

In this workflow, glacial lake outlines are required as input. 
We used previously published extents from [Furian et al. (2021)](https://doi.org/10.1017/jog.2021.18), 
but other sources or manually digitized outlines are equally valid.

In addition to the lake boundary (typically provided as a shapefile), two additional inputs are needed:
- the **lake bed morphology**, and  
- the **lake surface elevation**.

For **future glacial lakes**, the lake bed topography can be approximated by subtracting glacier ice thickness from the underlying DEM.  
For **existing lakes**, the lake bottom must be estimated—commonly using empirical relationships between lake area and volume, 
as outlined, for example, in [Cook and Quincey (2015)](https://doi.org/10.5194/esurfd-3-909-2015).

Finally, a raster file (`lake.tif`) needs to be created from the lake basin morphology. 

---

## Part 2 – Moraine Breach Definition

Delineating potential breach paths through the moraine is a non-trivial step and should be guided by:
- geomorphological interpretation,
- remote sensing imagery, and
- insights from previous field-based or modeling studies.

To capture uncertainty and assess sensitivity, we recommend generating **multiple breach scenarios** of varying sizes. 
Each breach should be integrated into a separate DEM to allow testing of different failure types.

---

## Part 3 – DEM Finalization

Both the lake basin and the moraine breach must be incorporated into the original DEM using GIS software. 
This results in a set of DEMs, each representing a specific combination of lake volume and breach geometry.

Once the lake basin has been merged with the DEM, it is useful to:
1. Apply a *Fill* algorithm to estimate the maximum water level,
2. Subtract a **freeboard value** (e.g., 5 m or 10 m) from this level to set the actual lake surface elevation.

Next, delineate the **downstream valley extent** as a separate shapefile and use it to clip the DEM. 
This clipped output serves as the simulation domain.

⚠️ **Important:**  
The raster representing the valley extent (`valley.tif`) must have the **same extent and alignment** as the DEM (`DEM.tif`). This can be ensured by using ArcGIS tools such as:

- **Raster Calculator**:  
  ``
  SetNull("valley.tif" < 0, "DEM.tif")  
  ``  
with the following adjustments in the Environment settings:
  - Set *Extent* and *Snap Raster* to the extent of the original DEM

---

## Part 4 – STL File Generation

STL files representing the valley and lake surfaces are generated using the Python scripts provided in the `code` folder.  
These scripts require slight adjustment depending on the actual file paths and data used for your specific site.

In particular:

- For the **valley STL**, the script requires a single raster file (e.g., `valley.tif`) as input.
- For the **lake STL**, the surface elevation of the water body must also be provided.  
  This can be passed either via the command line or by placing a plain text file containing the elevation value (in meters) in the working directory. The file should be named `elevation`.

Example commands:

```bash
# Generate STL for the valley:
python3 stlWriter_valley.py valley.tif

# Generate STL for the lake:
python3 stlWriter_lake.py lake.tif
```
The resulting STL files represent only the surface geometry. In order to be used for mesh generation in OpenFOAM,
these surfaces must be extruded into 3D volumes:

The valley surface can be extruded using `code/stlExtrude_valley.py`, 
which produces a box-shaped mesh with vertical sidewalls that follow the valley's outline.

The lake surface is processed using `code/stlExtrude_lake.py`. 
This script uses the specified lake surface elevation to fill the lake basin and 
generate a volumetric representation of the lake. Therefore, the surface elevation as well as the
extents of the main raster and the lake raster need to be adjusted accordingly in the script.

These extruded STL volumes will later be imported into OpenFOAM during the mesh generation process, 
ensuring that both the valley topography and the lake body are correctly integrated into the simulation domain.

---

## Part 5 – OpenFOAM Setup and Simulation Execution

This section assumes prior familiarity with OpenFOAM. For background on solver configuration, meshing workflows, and case structure,  
we recommend consulting the official [OpenFOAM documentation](https://www.openfoam.com/documentation/) and available community tutorials.

For the simulation of GLOFs, the `interFoam` solver is used. It simulates incompressible, isothermal two-phase flow (typically air and water), making it suitable for modeling flood waves with a free surface.

### 📁 Recommended Folder Structure

A **template case directory** is provided in this repository. It contains a complete folder structure,  
which you can adapt to your specific simulation scenario.

```text
template/
├── constant/
│   ├── polyMesh/             ← Mesh files (generated by blockMesh and snappyHexMesh)
│   ├── triSurface/           ← STL files for terrain and lake geometries
│   ├── transportProperties   ← Fluid properties (e.g., viscosity, density)
│   └── turbulenceProperties  ← Turbulence model settings (e.g., type, intensity)
│
├── system/
│   ├── controlDict           ← Runtime control (start/end time, write intervals, etc.)
│   ├── fvSchemes             ← Numerical discretization schemes
│   ├── fvSolution            ← Solver and algorithm settings
│   ├── blockMeshDict         ← Definition of the background mesh domain
│   ├── snappyHexMeshDict     ← Configuration for STL-based mesh refinement
│   ├── createBafflesDict     ← Defines internal faces to be converted into baffles
│   ├── createPatchDict       ← Used to define and merge patches after meshing
│   ├── decomposeParDict      ← Parallelization settings: domain decomposition for multi-core computation
│   ├── topoSetDict           ← Defines subsets of the mesh for subsequent baffle generation
│   └── setFieldsDict         ← Defines initial field values for selected regions (e.i., setting the initial water body)
│
├── 0.org/                    ← Initial and boundary conditions (e.g., p_rgh, U, alpha.water)
│
├── terrain/                  ← Folder for input raster files and STL generation scripts
├── custom_name.foam          ← Empty file for ParaView to recognize the case

```

### 🧱 Mesh Generation 🔷 blockMesh

The first step is to define a background mesh box that encloses your terrain and lake geometries.
This is done in the `blockMeshDict` file inside the system/ folder.

You need to extract the minimum and maximum X, Y, and Z coordinates from your STL valley file 
to define the bounding box for blockMesh. This can be done in two ways:

- Select the STL file in ParaView, go to the Information tab, and note the bounds (min/max for X, Y, Z).

- Use the `numpy-stl` package in Python to print the values:

```python
import numpy
from stl import mesh
mesh = mesh.Mesh.from_file("path/to/domain.stl")
print("X:", mesh.x.min(), mesh.x.max())
print("Y:", mesh.y.min(), mesh.y.max())
print("Z:", mesh.z.min(), mesh.z.max())
```
> ⚠️ Depending on the size of the STL file, this may take a while.  

Once you have the coordinate bounds, insert them into the vertices section of the `blockMeshDict` according to the following example:
```cpp
vertices  
(
    ( 0 0 0)
    ( 154775 0 0)
    ( 154775 164888 0)
    ( 0 164888 0)
    ( 0 0 7500)
    ( 154775 0 7500)
    ( 154775 164888 7500)
    ( 0 164888 7500)
);
```
The mesh resolution is defined in the blocks section, 
where each value corresponds to the number of cells along the X, Y, and Z axes.
OpenFOAM will divide the bounding box by these values to create the base mesh. 

```cpp
blocks
(
    hex (0 1 2 3 4 5 6 7) (240 260 14)  simpleGrading (1 1 1)
);
```
(240 260 14) indicates the number of cells in X, Y, and Z directions.
simpleGrading defines uniform cell size distribution.  
For GLOF simulations, a base resolution between 1 km and 500 m per cell is often a good starting point. 
`snappyHexMesh` will then refine this further.

Once everything is set, you can generate the background mesh in OpenFOAM by running the following terminal command 
from your case directory (where the system/ folder is located):
```bash
blockMesh
```
The generated mesh will be stored in the constant/polyMesh/ folder and can be checked in ParaView or by 
running OpenFOAM’s internal mesh check:
```bash
checkMesh
```

### 🧱 Mesh Generation 🔷 snappyHexMesh

`snappyHexMesh` fits the initial mesh block to the STL file and increases the resolution 
in three steps (due to the large size of the domain, 
we refrained from using the `addLayers` functionality, but feel free to enable this step if it fits your case):
```cpp
castellatedMesh true;
snap            true;
addLayers       false;
```
🗂️ The `geometry` section lets you define the necessary inputs or searchable boxes for mesh refinement steps.

🧱 `castellatedMesh` generates the initial mesh by subdividing the background mesh based on the STL geometry, 
then cutting cells along the surfaces defined in constant/triSurface/ and 
refining regions near important features (e.g., the moraine breach or the surroundings of the lake).  
The outcome resembles the STL shape, but still has a sharp, blocky geometry.

🧲 `snap` snaps the castellated mesh onto the STL surface. It moves mesh points so that they lie on the actual STL geometry and
improves the geometric accuracy of the surfaces. 

📚 The `addLayers` step can add boundary layers to the mesh, growing outward from selected surfaces. 
These layers usually have a higher resolution, improve near-wall flow behaviour and can be used to improve 
the accuracy of the model. However, due to the higher resolution, the compulational time will increase tremendously.

#### 🗂️ snappyHexMeshDict - `geometry`
`snappyHexMeshDict` gives you detailed control over each step. First, under `geometry`, you define the desired geometries, 
either by providing an STL file or by defining an area in the mesh. In this case, the domain is provided by the STL box, 
the valley is represented by the valley STL file, as is the lake by the lake STL.  
The area around the moraine dam has no related STL file and thus needs to be defined by a searchableBox. 
The parameters for this can be extracted from ParaView: After an initial run of `snappyHexMesh`, load the mesh into 
ParaView (as a surface with edges), identify the location of the moraine breach you want to receive a higher resolution and extract the
edge coordinates by hovering on them with the "Hover Points" functionality activated.
```cpp
geometry
{
    domain
    {
        type distributedTriSurfaceMesh;
        file "valley_box.stl"; 
    }
    valley_stl
    {
        type distributedTriSurfaceMesh;
        file "valley.stl";
    }
    lake
    {
        type distributedTriSurfaceMesh;
        file "lake.stl";
    }
    dam_box
    {
    type searchableBox;
        min (120963 120470 4400);
        max (120963.5 120540 4550);
    }
};
```
#### 🧱 snappyHexMeshDict - `castellatedMeshControls`
Under `castellatedMeshControls`, you adjust the regions and surfaces for which the resolution 
should be increased.
```cpp
castellatedMeshControls
{
    maxLocalCells           10000000; 
    maxGlobalCells          50000000; 
    minRefinementCells      10;
    maxLoadUnbalance        0.10;
    nCellsBetweenLevels     3; 

    features
    (
    );

    refinementSurfaces
    {
        domain
        {
            level (0 0);
            regions
            {
                walls
                {
                  level (0 0);
                }
                valley
                {
                  level (5 5);
                }
            }
        }
    }
    resolveFeatureAngle 60;
```
`refinementSurfaces` controls how different parts of the STL are refined. 
Each level increases mesh resolution by a factor of 2 per axis.
For example:
- Level 0: original cell size 
- Level 1: 2× more cells per direction
- Level 2: 4× more cells → cell size = ¼
- Level 5: 32× more → very fine mesh in that region

The `refinementRegions` entry defines volumetric refinement zones around certain STL geometries. 
These are used to increase mesh resolution not only on surfaces, but also in the surrounding volume, 
```cpp
    refinementRegions 
    {
        valley_stl
        {
            mode    distance;
            levels  ((40 5));
        }
        lake
        {
            mode     distance;
            levels   ((150 5));
        }
        dam_box
        {
            mode     distance;
            levels   ((20 6));
        }
    }

    locationInMesh (120970 120470 4480);
    allowFreeStandingZoneFaces true;
};
```
Each entry refers to an object from the geometry section.  
`mode distance` tells `snappyHexMesh` to refine cells within a certain distance from the geometry surface.  
In `levels ((distance refinementLevel))`, each entry is a tuple:
- The first value is the distance from the surface (in meters). 
- The second value is the refinement level to apply within that range.

`locationInMesh` defines a point inside the mesh domain of the valley box. 
This is required by `snappyHexMesh` to determine 
what is "inside" and what is "outside" the mesh boundaries.

#### 🧱 snappyHexMeshDict - `addLayersControls`
With the `addLayersControls`, you can define which surface should receive the additional layers, 
their initial and final thickness as well as further details. However, since it is not used in this approach
due to the increased computational demands, it is not discussed here further.

### Lake initialization

The `stlWriter_lake.py`-script generated an STL-file representing the lake as a box reaching from 
0 meters of elevation to the defined lake surface elevation. This `lake_box.stl` needs to be moved to the
`triSurface`-folder in /constant, where it can be found by the `setFieldsDict`. 
This functionality uses the following code to initialize cells as "water":
```cpp
regions
(
    surfaceToCell
    {
	name	lake;
	file	"./constant/triSurface/lake_box.stl";
	filetype stl;
	outsidePoints
	(
		(120958 120370 4550)
	);
	includeCut	true;
	includeInside	true;
	includeOutside	false;
	nearDistance	-1;
	curvature	-100;
        fieldValues
        (
            volScalarFieldValue alpha.water 1.0
        );
    }
);
```
> ⚠️ The `outsidePoints` need to be outside the lake volume, but inside the atmosphere mesh.

