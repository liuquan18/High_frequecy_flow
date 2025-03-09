#!/bin/bash
#SBATCH --job-name=VKE
#SBATCH --time=01:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=VKE.%j.out

module load cdo
module load parallel

node=$1
member=$node

echo "Ensemble member ${member}"

eke_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/eke_daily/r${member}i1p1f1/
q_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r${member}i1p1f1/

to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/vke_daily/r${member}i1p1f1/
tmp_dir=/scratch/m/m300883/VKE/r${member}i1p1f1/

mkdir -p ${to_path} ${tmp_dir}

export eke_path q_path to_path member tmp_dir

# function to calculate VKE

VKE(){
    dec=$1
    eke_file=$(find ${eke_path} -name "*${dec}*.nc")
    q_file=$(find ${q_path} -name "*${dec}*.nc")
    # basename without .nc
    fname=$(basename ${eke_file} .nc | sed 's/eke/vke/')
    to_file=${to_path}${fname}.nc

    cdo -O -expr,'vke=hus*hus*eke' -merge ${q_file} ${eke_file} $to_file

}

export -f VKE

# calculate VKE
parallel -j 5 VKE ::: {1850..2090..10}

# check if all files are created
n_files=$(ls ${to_path} | wc -l)
n_files_exp=$(( (2090-1850)/10 + 1 ))
if [ $n_files -ne $n_files_exp ]; then
    echo "Not all files created"

    for dec in {1850..2090..10}; do
        if [ ! -f ${to_path}vke_daily_MPI-GE_*.nc ]; then
            echo "File for ${dec} not created"
            echo "recalculate"
            VKE $dec
        fi
    done

fi
