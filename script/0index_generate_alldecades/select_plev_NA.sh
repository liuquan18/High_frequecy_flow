#!/bin/bash
#SBATCH --job-name=selNA
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=5
#SBATCH --ntasks=1250
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=selNA.%j.out

module load cdo
module load parallel

var=zg

base_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_daily_ano/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_NA_daily_ano/

# mkdir for all ensemble r${member}i1p1f1 under to_dir
for member in {1..50}; do
    mkdir -p ${to_dir}r${member}i1p1f1/
done


export base_dir

Select_NA(){
    infile=$1

    # replace 'zg_daily_ano' to 'zg_NA_daily_ano'
    outfile=${infile/zg_daily_ano/zg_NA_daily_ano}

    cdo -sellevel,25000 -sellonlatbox,-90,40,20,80 ${infile} ${outfile}
}

export -f Select_NA

find ${base_dir} -name "${var}_day_MPI-ESM1-2-LR_r*i1p1f1_gn_*.nc" | parallel --jobs 25 Select_NA