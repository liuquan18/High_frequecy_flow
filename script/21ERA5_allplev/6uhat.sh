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

u_path=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/ua_daily/

uhat_path=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/ua_hat_daily/


mkdir -p ${uhat_path} 

export u_path uhat_path



# function to band filter
band_filter(){
    infile=$1
    outfile=$2  
    # basename without .nc
    fname=$(basename ${infile%.nc})

    cdo -O -lowpass,30.5 ${infile} ${outfile}

}

perform(){
    year=$1
    ufile=$(find ${u_path} -name "E5pl00_1D_ua_daily_${year}*.nc")

    fname_u=$(basename ${ufile%.nc})

    fname_uhat=${uhat_path}${fname_u/ua/ua_hat}.nc


    echo "Filtering ${fname_u}"
    band_filter ${ufile} ${fname_uhat}

}

export -f perform

export -f band_filter

parallel --jobs 5 perform ::: {1979..2024}