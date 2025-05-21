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

- A **digital elevation model (DEM)** with sufficient resolution (e.g., ALOS PALSAR at 12.5 m)
- **Vector outlines** of the glacial lakes (e.g., shapefiles) serving as GLOF origins

---

## 🛠 Software Requirements

The following software stack has been tested and recommended:

| Tool        | Version     | Purpose                         |
|-------------|-------------|----------------------------------|
| OpenFOAM    | 2112        | 3D CFD simulation               |
| ParaView    | 5.11.0      | Visualization and postprocessing |
| Python      | 3.8         | Pre- and postprocessing scripts |
| C++         | —           | Required by OpenFOAM solvers    |

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

## ▶️ First steps

Preparing, preparing

```bash
gdal_translate -of XYZ input_dem.tif output_dem.xyz
