"""
    #########################################
    ## 3D CFD Simulation of GLOFs with OpenFOAM ##
    #########################################

    This script is part of Work Package 3 of the project 
    'Future Glacial Lakes in High Mountain Asia – Modeling and Risk Analysis' (GLAMoR).
    It was developed for the main analyses presented in the publication:
    Furian et al. (2025), *Natural Hazards and Earth System Sciences*.

    Author: W. Furian

    This script enables the simulation of glacial lake outburst floods (GLOFs) 
    in high-mountain regions using the three-dimensional CFD software OpenFOAM.

    ----------------------------
    Required input data:
    - A high-resolution digital elevation model (DEM)
    - Spatial data delineating the extent of glacial lakes serving as GLOF sources

    ----------------------------
    Tested software environment:
    - OpenFOAM version 2112 (for hydrodynamic simulation)
    - ParaView version 5.11.0 (for visualization and analysis)
    - Python 3.8 (for pre- and postprocessing routines)
    - C++ (as required by OpenFOAM solvers)

    ----------------------------
    Repository:
    https://github.com/cryotools/GLOF-simulations

    Project information:
    https://hu-berlin.de/glamor

    ----------------------------
    License and usage:
    This script is provided for non-commercial use. Users are free to modify and adapt it, 
    provided appropriate credit is given to the original author. 
    Contributions are welcome—please fork the repository, commit your changes, 
    and submit a pull request.

    Contact: W. Furian (ORDID:0000-0001-7834-2500)
"""
