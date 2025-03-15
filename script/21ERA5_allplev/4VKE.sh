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

module load cdo/2.5.0-gcc-11.2.0
module load parallel

eke_path=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/eke_daily/
qp_path=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/hus_prime_daily/

vke_path=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/vke_daily/


mkdir -p ${vke_path} ${tmp_dir}

export eke_path qp_path vke_path

# function to calculate VKE

VKE(){
    year=$1
    echo "Calculating VKE for ${year}"

    eke_file=$(find ${eke_path} -name "*${year}*.nc")
    q_file=$(find ${qp_path} -name "*${year}*.nc")
    # basename without .nc
    fname=$(basename ${eke_file} .nc | sed 's/eke/vke/')
    to_file=${vke_path}${fname}.nc

    cdo -r -O -expr,'vke=var133*var133*eke' -merge ${q_file} ${eke_file} $to_file

}

export -f VKE

start_year=${1:-1979}
end_year=${2:-2024}


# calculate VKE
seq ${start_year} ${end_year} | parallel -j 5 VKE
