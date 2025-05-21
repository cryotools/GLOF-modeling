
## ▶️ Workflow Overview

The general workflow consists of the following steps:

1. **Delineation of glacial lake boundaries**  
   Identify and digitize the extent of the glacial lake using satellite imagery or field data.

2. **Identification of potential breach path**  
   Define the most likely breach location across the moraine, based on topography and geomorphological indicators.

3. **Preparation of the digital elevation model (DEM)**  
   Process and clean the DEM to ensure compatibility with meshing tools.

4. **Conversion of the DEM to STL format**  
   Generate a surface mesh (STL file) to represent the terrain in OpenFOAM.

5. **OpenFOAM simulation setup**  
   - Use `blockMesh` and `snappyHexMesh` to generate the computational mesh  
   - Define the initial water body using `setFields`  
   - Configure and validate boundary conditions  
   - Execute the simulation runs

Each of these steps will be accompanied by explanatory notes and representative code snippets throughout this guide.

