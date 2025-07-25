#!/bin/bash
#SBATCH --job-name=monmean
#SBATCH --time=01:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=monmean.%j.out

module load cdo/2.5.0-gcc-11.2.0
module load parallel

var=$1
plev=$2

echo "Variable: ${var}, Pressure Level: ${plev}"

# function to calculate monthly mean
monmean(){
    member=$1
    decade=$2
    echo "Ensemble member ${member} of variable ${var} at pressure level ${plev} for decade ${decade}"

    data_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/${var}_daily_ano/r${member}i1p1f1/
    to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/${var}_daily_ano_monmean/r${member}i1p1f1/

    mkdir -p "${to_path}"

    infile=$(find ${data_path} -name "*${decade}*.nc")
    echo "Processing ${infile}"

    outfile=${infile/${var}_daily_ano/${var}_daily_ano_monmean}

    cdo -P 10 -sellevel,${plev} -fldmean -sellonlatbox,-180,180,50,70 ${infile} ${outfile}
}

export -f monmean
export var plev


parallel -j 5 monmean ::: {1..50} ::: 1850 2090

