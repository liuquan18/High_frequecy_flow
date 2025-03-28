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

vp_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_prime_daily/r${member}i1p1f1/
thetap_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/theta_prime_daily/r${member}i1p1f1/

flux_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vptp_daily/r${member}i1p1f1/

mkdir -p ${flux_path}

export vp_path thetap_path flux_path member member

flux(){
    dec=$1
    vfile=$(find ${vp_path} -name "*${dec}*.nc")
    tfile=$(find ${thetap_path} -name "*${dec}*.nc")

    vfile_name=$(basename "${vfile}")    
    outfile="${flux_path}${vfile_name//va_prime/vptp}"
    
    echo "Calculating heat flux for ${dec}"
    cdo -r -O -expr,'vptp=va*ta' -merge ${vfile} ${tfile} ${outfile}

}

export -f flux

parallel --jobs 5 flux ::: {1850..2090..10}

# check if all files are created
for dec in {1850..2090..10}; do
    vfile=$(find ${vp_path} -name "*${dec}*.nc")
    tfile=$(find ${thetap_path} -name "*${dec}*.nc")
    outfile="${flux_path}${vfile_name//va_prime/vptp}"
    
    if [ ! -f "${outfile}" ]; then
        echo "Error: ${outfile} not created"
        exit 1
    fi
done