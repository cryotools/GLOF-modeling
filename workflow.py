"""
    #############################
    ## 3D CFD GLOF simulations ##
    #############################

    This is the main code file of the third work package of the project
    'Future glacial lakes in High Mountain Asia - Modeling and Risk Analysis' (GLAMoR).
    It was used for the main analyses of the Natural Hazards and Earth System Sciences publication by Furian et al. (2025).
    The script was written by W. Furian.

    With this script, it is possible to use the three-dimensional CFD software OpenFOAM to simulate GLOF events in high-mountain areas.

    In order to run properly, this script requires different datasets to be downloaded:
    - a DEM with a sufficiently high resolution
    - information on the spatial extent of the glacial lakes that the GLOFs will originate from

    This workflow has been tested using:
    - OpenFOAM version 2112 for simulations,
    - ParaView version 5.11.0 for visualization and analysis,
    - Python 3.8 for pre- and postprocessing routines,
    - C++ as required for the OpenFOAM solvers.

    This code is available on github at https://github.com/cryotools/GLOF-simulations
    For more information on this work package see the README.
    For more information on the project as a whole see https://hu-berlin.de/glamor.

    You are allowed to use and modify this code in a noncommercial manner and by
    appropriately citing the above mentioned developer. If you would like to share your own improvements,
    please fork the repository on GitHub, commit your changes, and file a merge request.

    Correspondence: wilhelm.furian.1@geo.hu-berlin.de
"""
# imports