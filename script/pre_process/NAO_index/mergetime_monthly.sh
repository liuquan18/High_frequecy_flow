#!/bin/bash
#SBATCH --job-name=mergetime
#SBATCH --time=08:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=mergetime.%j.out


module load cdo
module load parallel

mergetime() {
    member=$1
    echo "Merging time for member ${member}"

    Hist_path=/pool/data/CMIP6/data/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r${member}i1p1f1/Amon/zg/gn/v????????/*.nc
    ssp585_path=/pool/data/CMIP6/data/ScenarioMIP/MPI-M/MPI-ESM1-2-LR/ssp585/r${member}i1p1f1/Amon/zg/gn/v????????/*.nc
    To_path=/scratch/m/m300883/MPI_GE_CMIP6/mergetime/

    cdo -sellevel,100000,85000,70000,50000,25000 -mergetime ${Hist_path[@]} ${ssp585_path[@]} ${To_path}zg_Amon_MPI-ESM1-2-LR_HIST_ssp585_r${member}i1p1f1_gn_185001-210012.nc

    }
    
export -f mergetime 

parallel --jobs 20 mergetime ::: {1..50}