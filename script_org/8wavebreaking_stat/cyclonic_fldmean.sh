#!/bin/bash
#SBATCH --job-name=cwb
#SBATCH --time=01:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=cwb.%j.out

module load cdo/2.5.0-gcc-11.2.0
module load parallel

fldmean(){
    member=$1
    dec=$2

    echo "Processing member: $member, date: $dec"

    from_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_cyclonic_daily/r${member}i1p1f1/
    to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_cyclonic_fldmean/r${member}i1p1f1/

    mkdir -p ${to_path}

    file=$(find ${from_path} -name "*${dec}*.nc" | head -n 1)
    if [ -z "$file" ]; then
        echo "File not found for member: $member, date: $dec"
        return
    fi
    output_file=${to_path}wb_cyclonic_fldmean_${dec}.nc
    echo "Calculating field mean for member: $member, date: $dec"
    cdo -r -O -fldmean -sellonlatbox,-100,-30,45,75 ${file} ${output_file}
}

export -f fldmean

parallel --jobs 10 fldmean ::: {1..50} ::: {1850..2090..10}
