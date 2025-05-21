![GLAMoR](https://cryo-tools.org/wp-content/uploads/2020/07/GLAMoR-LOGO-400px.png)

## Three-Dimensional Simulations of Glacial Lake Outburst Floods Using OpenFOAM

### Overview

This repository contains the workflow developed for the accompanying publication 
in *Natural Hazards and Earth System Sciences* (NHESS) [citation].
It provides users with a framework to apply **OpenFOAM** for:

- generating three-dimensional meshes from digital elevation models (DEMs),
- delineating glacial lakes,
- constructing breach scenarios, and
- setting up and running simulations of glacial lake outburst flood (GLOF) events.

### Required Data

To execute the workflow, the following input data must be downloaded and prepared:

- Digital elevation models (DEMs) with appropriate spatial resolution (e.g., ALOS PALSAR at 12.5 m),
- Vector data delineating the extent of the glacial lake(s), preferably in shapefile format.

### Software Requirements

This workflow has been tested using:

- **OpenFOAM** version 2112 for simulations,
- **ParaView** version 5.11.0 for visualization and analysis,
- **Python** 3.8 for pre- and postprocessing routines,
- **C++** as required for the OpenFOAM solvers.

### Citation

You are welcome to use this code in your own research. 
If you do, please cite the corresponding release. For example, for version v1.0:

> Placeholder, A. (2025): *OpenFOAM GLOF modeling: a three-dimensional flood simulation approach*, 
> v1.0, A Scientific Journal, 8(12).  