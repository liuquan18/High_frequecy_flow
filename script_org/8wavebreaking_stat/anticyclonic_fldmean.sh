#!/bin/bash
#SBATCH --job-name=awb
#SBATCH --time=01:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=awb.%j.out

module load cdo/2.5.0-gcc-11.2.0
module load parallel

fldmean(){
    member=$1
    dec=$2

    from_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_anticyclonic_daily/r${member}i1p1f1/
    to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_anticyclonic_fldmean/r${member}i1p1f1/

    mkdir -p ${to_path}

    file=$(find ${from_path} -name "*${dec}*.nc" | head -n 1)
    if [ -z "$file" ]; then
        echo "File not found for member: $member, date: $dec"
        return
    fi
    output_file=${to_path}wb_anticyclonic_fldmean_${dec}.nc
    echo "Calculating field mean for member: $member, date: $dec"
    cdo -r -O -fldmean -sellonlatbox,-60,30,30,70 ${file} ${output_file}
}

export -f fldmean

parallel --jobs 10 --bar fldmean ::: {1..50} ::: {1850..2090..10}
