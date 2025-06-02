#!/bin/bash
#SBATCH --job-name="OF_SIM"
#SBATCH --qos=short
#SBATCH --account=prime

#SBATCH --ntasks=180
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
 
# cleanup and prep
rm -r processor*
rm -r log.*
cp ./system/decomposeDicts/decomposeParDict_two ./system/decomposeParDict
runApplication -o decomposePar -decomposeParDict system/decomposeParDict -force

# main run
runParallel interFoam -parallel
runApplication reconstructPar
echo "Finished reconstructing timesteps"
rm -r processor*
