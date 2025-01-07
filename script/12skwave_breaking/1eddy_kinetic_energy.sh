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

node=$1
member=$node
echo "Ensemble member ${member}"

u_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily/r${member}i1p1f1/
v_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily/r${member}i1p1f1/

up_path=/scratch/m/m300883/up/r${member}i1p1f1/
vp_path=/scratch/m/m300883/vp/r${member}i1p1f1/

tmp_dir=/scratch/m/m300883/upvp/r${member}i1p1f1/
eddy_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/eke_daily/r${member}i1p1f1/

mkdir -p ${eddy_path} ${up_path} ${vp_path} ${tmp_dir}

export u_path up_path 
export v_path vp_path 
export eddy_path member tmp_dir

# function to band filter
band_filter(){
    infile=$1
    outfile=$2  
    # basename without .nc
    fname=$(basename ${infile%.nc})

    # split years
    cdo -O -splityear ${infile} ${tmp_dir}${fname}_year
    # band filter, keep 2-12 days 
    year_files=$(ls ${tmp_dir}${fname}_year*)
    cdo -O -mergetime -apply,bandpass,30.5,182.5 [ ${year_files} ] ${outfile}
    # remove temporary files
    rm ${tmp_dir}${fname}_year*
}

# function to eddy kinetic energy
EKE(){
    dec=$1
    ufile=$(find ${u_path} -name "ua*_r${member}i1p1f1_gn_${dec}*.nc")
    vfile=$(find ${v_path} -name "va*_r${member}i1p1f1_gn_${dec}*.nc")
    # basename without .nc
    fname_u=$(basename ${ufile%.nc})
    echo "Filtering ${fname_u}"
    fname_u=${up_path}${fname_u/ua/up}.nc
    band_filter ${ufile} ${fname_u}
    
    fname_v=$(basename ${vfile%.nc})    
    echo "Filtering ${fname_v}"
    fname_v=${vp_path}${fname_v/va/vp}.nc
    band_filter ${vfile} ${fname_v}

    #eddy kinetic energy
    echo "Calculating EKE"
    fname_eddy=$(basename ${ufile%.nc})
    fname_eddy=${eddy_path}${fname_eddy/ua/eke}.nc
    cdo -O -expr,'eke=0.5*(ua*ua+va*va)' -merge ${fname_u} ${fname_v} ${fname_eddy}

    # remove temporary files
    rm ${fname_u} ${fname_v}
}

export -f band_filter EKE
# parallel band filter in to_dir
parallel --jobs 5 EKE ::: {1850..2090..10}

# Check if all required decades are saved
for dec in {1850..2090..10}; do
    if [ ! -f ${eddy_path}eke_day_MPI-ESM1-2-LR_r${member}i1p1f1_gn_${dec}0501-$((dec+9))0930.nc ]; then
        echo "File for decade ${dec} is missing in ${eddy_path}"
    
        # calculate the missing dec
        echo "recalculate ${dec}"
        EKE ${dec}

    fi
done
