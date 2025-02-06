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

frequency=${2:-prime} # prime (2-12 days) or high (2-6 days), default prime

echo "Ensemble member ${member}"

u_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily/r${member}i1p1f1/
v_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily/r${member}i1p1f1/

# save path
if [ "$frequency" == "prime" ]; then
    up_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/up/r${member}i1p1f1/
    vp_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vp/r${member}i1p1f1/
else
    up_path=/scratch/m/m300883/upp/r${member}i1p1f1/
    vp_path=/scratch/m/m300883/vpp/r${member}i1p1f1/
fi

tmp_dir=/scratch/m/m300883/upvp/r${member}i1p1f1/

mkdir -p ${eddy_path} ${up_path} ${vp_path} ${tmp_dir}

export u_path up_path 
export v_path vp_path 
export eddy_path member tmp_dir
export frequency

# function to band filter
band_filter(){
    infile=$1
    outfile=$2  
    # basename without .nc
    fname=$(basename ${infile%.nc})

    # split years
    cdo -O -splityear ${infile} ${tmp_dir}${fname}_year
    # band filter
    year_files=$(ls ${tmp_dir}${fname}_year*)
    if [ "$frequency" == "prime" ]; then
        echo "Filtering 2-12 days"
        # cdo -O -mergetime -apply,bandpass,30.5,182.5 [ ${year_files} ] ${outfile}
        cdo -O -mergetime -apply,highpass,36.5 [ ${year_files} ] ${outfile}
    elif [ "$frequency" == "high" ]; then
        echo "Filtering 2-6 days"
        # cdo -O -mergetime -apply,bandpass,60.8,182.5 [ ${year_files} ] ${outfile}
        cdo -O -mergetime -apply,highpass,72 [ ${year_files} ] ${outfile}  # use highpass instead of bandpass
    fi
    # remove temporary files
    rm ${tmp_dir}${fname}_year*
}

# function to eddy kinetic energy
up_vp(){
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

}

export -f band_filter up_vp
# parallel band filter in to_dir
parallel --jobs 5 up_vp ::: {1850..2090..10}

# check completeness
for dec in {1850..2090..10}; do

    ufile=$(find ${u_path} -name "ua*_r${member}i1p1f1_gn_${dec}*.nc")
    vfile=$(find ${v_path} -name "va*_r${member}i1p1f1_gn_${dec}*.nc")
    # basename without .nc
    fname_u=$(basename ${ufile%.nc})
    fname_u=${up_path}${fname_u/ua/up}.nc
    if [ ! -f ${fname_u} ]; then
        echo "Missing ${fname_u}, reprocessing"
        band_filter ${ufile} ${fname_u}
    fi

    
    fname_v=$(basename ${vfile%.nc})    
    echo "Filtering ${fname_v}"
    fname_v=${vp_path}${fname_v/va/vp}.nc
    if [ ! -f ${fname_v} ]; then
        echo "Missing ${fname_v}, reprocessing"
        band_filter ${vfile} ${fname_v}

done