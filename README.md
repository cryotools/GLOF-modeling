![GLAMoR](https://cryo-tools.org/wp-content/uploads/2020/07/GLAMoR-LOGO-400px.png)
# 3D CFD Simulations of Glacial Lake Outburst Floods Using OpenFOAM

This document outlines the core elements of the workflow used in **Work Package 3** 
of the project *Future Glacial Lakes in High Mountain Asia – Modeling and Risk Analysis (GLAMoR)*.  
It supports the results presented in:

**Furian and Sauter (2025)**  
*Natural Hazards and Earth System Sciences (NHESS)* [citation pending]

---

## ⚠️ About this Guide

This is not a fully executable, step-by-step script.  
Instead, it provides a structured overview with **code snippets**, **commands**, and **explanatory notes** for key steps involved in:

- Preparing digital elevation data
- Delineating glacial lakes
- Generating 3D meshes
- Defining breach scenarios
- Setting up and running hydrodynamic simulations in OpenFOAM

---

## 🧩 Required Input Data

To apply this workflow, the following input data are required:

- A **digital elevation model (DEM)** with sufficient resolution (e.g., ALOS PALSAR at 12.5 m)
- **Vector outlines** of the glacial lakes (e.g., shapefiles) serving as GLOF origins
- lake bathymetry data (or ice-thickness data for calculating the lake volume)

---

## 🛠 Software Requirements

The following software stack has been tested and is recommended for running the workflow:

| Software     | Version   | Purpose                                 |
|--------------|-----------|------------------------------------------|
| **OpenFOAM** | 2112      | 3D computational fluid dynamics (CFD) simulation |
| **ParaView** | 5.11.0    | Visualization and postprocessing         |
| **Python**   | 3.8       | Preprocessing and postprocessing scripts |
| **C++**      | —         | Required for OpenFOAM solvers            |

> 💡 *The code is written in both Python and C++.*

---

### 💻 System Setup and HPC Access

While small test cases may be run locally, **access to a high-performance computing (HPC) cluster** is highly recommended for full-scale simulations. You can use tools like:

- **PuTTY** – for secure SSH terminal access to remote servers
- **WinSCP** – for file transfer between your local machine and the cluster

Make sure that OpenFOAM is correctly installed and configured on the HPC system or simulation server.

---

## 🗂 Repository

Code and materials are hosted at:  
👉 [https://github.com/cryotools/GLOF-simulations](https://github.com/cryotools/GLOF-simulations)

For background on the overall GLAMoR project, see:  
🌐 [https://hu-berlin.de/glamor](https://hu-berlin.de/glamor)

---

## 📄 Licensing and Contributions

This code is free to use and adapt for **non-commercial purposes**.  
If you use or extend this workflow, please cite the original work (Furian and Sauter, 2025).

You are welcome to contribute:
- Fork the repository
- Commit your modifications
- Submit a pull request

---

## 📬 Contact

For questions or collaboration inquiries, please contact:  
**W. Furian, ORCID: 0000-0001-7834-2500**

---

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
