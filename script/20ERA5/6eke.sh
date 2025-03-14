#!/bin/bash
#SBATCH --job-name=eddy
#SBATCH --time=01:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=eddy.%j.out

module load cdo
module load parallel

u_path=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/ua_daily/
v_path=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/va_daily/

up_path=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/up_daily/
vp_path=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/vp_daily/

tmp_dir=/scratch/m/m300883/ERA5/upvp/
eddy_path=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/eke_daily/
upvp_path=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/upvp_daily/

mkdir -p ${eddy_path} ${up_path} ${vp_path} ${tmp_dir} ${upvp_path}

export u_path up_path
export v_path vp_path
export eddy_path tmp_dir upvp_path



# function to band filter
band_filter(){
    infile=$1
    outfile=$2  
    # basename without .nc
    fname=$(basename ${infile%.nc})

    cdo -O -bandpass,30.5,182.5 ${infile} ${outfile}
}

EKE(){
    year=$1
    ufile=$(find ${u_path} -name "E5pl00_1D_ua_daily_${year}*.nc")
    vfile=$(find ${v_path} -name "E5pl00_1D_va_daily_${year}*.nc")

    fname_u=$(basename ${ufile%.nc})
    fname_v=$(basename ${vfile%.nc})

    upfile=${up_path}${fname_u/ua/up}.nc
    vpfile=${vp_path}${fname_v/va/vp}.nc

    eddyfile=${eddy_path}E5pl00_1D_eke_daily_${year}.nc
    upvpfile=${upvp_path}${fname_u/ua/upvp}.nc
    

    echo "Filtering ${fname_u}"
    band_filter ${ufile} ${upfile}

    echo "Filtering ${fname_v}"
    band_filter ${vfile} ${vpfile}

    echo "Calculating EKE"
    cdo -O -expr,'eke=0.5*(var131*var131 + var132*var132)' -merge ${upfile} ${vpfile} ${eddyfile}

    echo "Calculating upvp"
    cdo -O  -mul ${upfile} ${vpfile} ${upvpfile}
}

export -f EKE
export -f band_filter

parallel --jobs 5 EKE ::: {1979..2024}