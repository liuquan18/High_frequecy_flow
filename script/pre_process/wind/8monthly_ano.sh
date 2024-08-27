#!/bin/bash

module load cdo
module load parallel    

var=$1 # zg, ua, va
# define base path
base_path=/work/ik1017/CMIP6/data/CMIP6/ScenarioMIP/MPI-M/MPI-ESM1-2-LR/ssp585/
to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_monthly_ano/${var}_monthly_ano_last10/
tmp_path=/scratch/m/m300883/${var}_monthly_ano_last10/

ens_file=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_season_global/va_Amon_MPI-ESM1-2-LR_HIST_ensmean_209105-210009.nc

mkdir -p ${to_path} ${tmp_path}
export base_path
export to_path
export ens_file


# Create file lists with ensemble members ranging from 1 to 50
for member in {1..50}; do
    # Use find to resolve the wildcard into real paths
    files1=$(find ${base_path}r${member}i1p1f1/Amon/${var}/gn/ -name ${var}_Amon_MPI-ESM1-2-LR_ssp585_r${member}i1p1f1_gn_207501-209412.nc)
    files2=$(find ${base_path}r${member}i1p1f1/Amon/${var}/gn/ -name ${var}_Amon_MPI-ESM1-2-LR_ssp585_r${member}i1p1f1_gn_209501-210012.nc)
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


Anomaly(){
    file1=$1
    file2=$2

    cdo -selyear,2091/2100 -mergetime -apply,-selmon,5/9 [ $file1 $file2 ] ${tmp_path}$(basename "${file1}" | sed 's/207501-209412.nc/209105-209409_ano.nc/')
    cdo -P 10 -sub ${tmp_path}$(basename "${file1}" | sed 's/207501-209412.nc/209105-209409_ano.nc/') $ens_file ${to_path}$(basename "${file1}" | sed 's/207501-209412.nc/209105-209409_ano.nc/')
    
}

export -f Anomaly



parallel --jobs 20 Anomaly ::: $file_list1 ::: $file_list2