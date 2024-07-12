#!/bin/bash
module load cdo
module load parallel

# for last10 years


mergetime() {
    base_path="/pool/data/CMIP6/data/ScenarioMIP/MPI-M/MPI-ESM1-2-LR/ssp585/"
    variable="zg"
    timespan1="207501-209412"
    timespan2="209501-210012"

    r=$1
    file1=$(find "$base_path/r${r}i1p1f1/Amon/$variable/gn" -name "${variable}_Amon_MPI-ESM1-2-LR_ssp585_r${r}i1p1f1_gn_${timespan1}.nc")
    file2=$(find "$base_path/r${r}i1p1f1/Amon/$variable/gn" -name "${variable}_Amon_MPI-ESM1-2-LR_ssp585_r${r}i1p1f1_gn_${timespan2}.nc")

    # merege the two files
    cdo -selyear,2091/2100 -mergetime $file1 $file2 "/scratch/m/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_season_global/${variable}_Amon_MPI-ESM1-2-LR_ssp585_r${r}i1p1f1_gn_209101-210012.nc"
}

# parallel mergetime
export -f mergetime
parallel --jobs 10 mergetime ::: {1..50}
