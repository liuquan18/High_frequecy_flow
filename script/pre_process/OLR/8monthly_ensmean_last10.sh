#!/bin/bash

module load cdo
module load parallel    


# define base path
base_path=/work/ik1017/CMIP6/data/CMIP6/ScenarioMIP/MPI-M/MPI-ESM1-2-LR/ssp585/
to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_season_global/

export base_path
export to_path


# Create file lists with ensemble members ranging from 1 to 50
for member in {1..50}; do
    # Use find to resolve the wildcard into real paths
    files1=$(find ${base_path}r${member}i1p1f1/Amon/rlut/gn/ -name 'rlut_Amon_MPI-ESM1-2-LR_ssp585_r'${member}'i1p1f1_gn_207501-209412.nc')
    files2=$(find ${base_path}r${member}i1p1f1/Amon/rlut/gn/ -name 'rlut_Amon_MPI-ESM1-2-LR_ssp585_r'${member}'i1p1f1_gn_209501-210012.nc')
    for file in $files1; do
        file_list1+="$file "
    done

    for file in $files2; do
        file_list2+="$file "
    done
done

# Remove the trailing space
file_list1=$(echo $file_list1 | sed 's/ $//')
file_list2=$(echo $file_list2 | sed 's/ $//')

cdo -selmon,5/9 -ensmean $file_list1 ${to_path}"rlut_Amon_MPI-ESM1-2-LR_HIST_ensmean_207505-209409.nc"
cdo -selmon,5/9 -ensmean $file_list2 ${to_path}"rlut_Amon_MPI-ESM1-2-LR_HIST_ensmean_209505-210009.nc"