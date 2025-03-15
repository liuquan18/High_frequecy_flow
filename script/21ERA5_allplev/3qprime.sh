#!/bin/bash
#SBATCH --job-name=qprime
#SBATCH --time=01:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=qprime.%j.out

module load cdo
module load parallel

model=ERA5_ano

q_path=/work/mh0033/m300883/High_frequecy_flow/data/${model}/hus_daily/

qp_path=/work/mh0033/m300883/High_frequecy_flow/data/${model}/hus_prime_daily/


mkdir -p ${qp_path} 

export q_path qp_path



# function to band filter
band_filter(){
    infile=$1
    outfile=$2  
    # basename without .nc
    fname=$(basename ${infile%.nc})

    cdo -O -highpass,36.55 ${infile} ${outfile}

}

perform(){
    year=$1
    husfile=$(find ${q_path} -name "E5pl00_1D_hus_daily_${year}*.nc")

    fname_hus=$(basename ${husfile%.nc})

    huspfile=${qp_path}${fname_hus/hus/hus_prime}.nc


    echo "Filtering ${fname_hus}"
    band_filter ${husfile} ${huspfile}

}

export -f perform

export -f band_filter

parallel --jobs 5 perform ::: {1979..2024}