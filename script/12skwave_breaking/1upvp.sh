#!/bin/bash
#SBATCH --job-name=upvp
#SBATCH --time=01:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=upvp.%j.out

module load cdo
module load parallel

node=$1
member=$node
echo "Ensemble member ${member}"

frequency=${2:-prime} # prime (2-12 days) or high (2-6 days), default prime

u_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily/r${member}i1p1f1/
v_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily/r${member}i1p1f1/

if [ "$frequency" == "prime" ]; then
    up_path=/scratch/m/m300883/up/r${member}i1p1f1/
    vp_path=/scratch/m/m300883/vp/r${member}i1p1f1/
    upvp_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/upvp_daily/r${member}i1p1f1/
else
    up_path=/scratch/m/m300883/upp/r${member}i1p1f1/
    vp_path=/scratch/m/m300883/vpp/r${member}i1p1f1/
    upvp_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/upvp_high_daily/r${member}i1p1f1/
fi

tmp_dir=/scratch/m/m300883/upvp/r${member}i1p1f1/

mkdir -p ${upvp_path} ${up_path} ${vp_path} ${tmp_dir}

export u_path up_path 
export v_path vp_path 
export upvp_path member tmp_dir
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
        cdo -O -mergetime -apply,highpass,36.5 [ ${year_files} ] ${outfile}
    fi
    # remove temporary files
    rm ${tmp_dir}${fname}_year*
}

# function to band filter
upvp(){
    dec=$1
    ufile=$(find ${u_path} -name "ua*_r${member}i1p1f1_gn_${dec}*.nc")
    vfile=$(find ${v_path} -name "va*_r${member}i1p1f1_gn_${dec}*.nc")
    # basename without .nc
    fname_u=$(basename ${ufile%.nc})
    echo "Processing ${fname_u}"
    fname_u=${up_path}${fname_u/ua/up}.nc
    band_filter ${ufile} ${fname_u}
    
    fname_v=$(basename ${vfile%.nc})    
    echo "Processing ${fname_v}"
    fname_v=${vp_path}${fname_v/va/vp}.nc
    band_filter ${vfile} ${fname_v}

    #momentum fluxes
    fname_upvp=$(basename ${ufile%.nc})
    fname_upvp=${upvp_path}${fname_upvp/ua/upvp}.nc
    cdo -O -mul ${fname_u} ${fname_v} ${fname_upvp}

    # remove temporary files
    rm ${fname_u} ${fname_v}
}

export -f band_filter upvp
# parallel band filter in to_dir
parallel --jobs 5 upvp ::: {1850..2090..10}

# Check if all required decades are saved
for dec in {1850..2090..10}; do
    if [ ! -f ${upvp_path}upvp_day_MPI-ESM1-2-LR_r${member}i1p1f1_gn_${dec}0501-$((dec+9))0930.nc ]; then
        echo "File for decade ${dec} is missing in ${upvp_path}"
    
        # calculate the missing dec
        echo "recalculate ${dec}"
        upvp ${dec}

    fi
done
