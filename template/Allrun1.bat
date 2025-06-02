#!/bin/bash

#SBATCH --job-name="MeshPrep"
#SBATCH --qos=short
#SBATCH --ntasks=16
#SBATCH --error=log_pre.err
#SBATCH --output=log_pre.out

# load all the necessary modules according to your server structure
module load intel/2020.2
module load anaconda/2019.07
module load openfoam
source /programs/intel-2020.2/openfoam/2112/OpenFOAM-v2112/etc/bashrc

ulimit -s unlimited
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions 
unset I_MPI_PMI_LIBRARY
export I_MPI_JOB_RESPECT_PROCESS_PLACEMENT=0

# cleanup
rm -r 0
rm -r ./constant/polyMesh
rm -r processor*
rm -r log.*

# prepare run
cp ./system/decomposeDicts/decomposeParDict_one ./system/decomposeParDict

# mesh creation
runApplication blockMesh
runApplication -o decomposePar -decomposeParDict system/decomposeParDict -force
runParallel snappyHexMesh -decomposeParDict system/decomposeParDict -overwrite
reconstructParMesh -constant
rm -r processor*

# mesh refining
renumberMesh -overwrite
topoSet
createBaffles -overwrite
createPatch -overwrite

# create alpha.water
cp -r ./tmp/0.org ./0
runApplication setFields

sbatch Allrun2.bat