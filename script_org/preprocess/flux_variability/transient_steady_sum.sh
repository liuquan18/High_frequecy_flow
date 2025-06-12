#!/bin/bash
#SBATCH --job-name=sum
#SBATCH --time=01:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=sum.%j.out

module load cdo/2.5.0-gcc-11.2.0
module load parallel


member=$1
var1=$2
var2=$3
plev=$4
suffix=$5


var1_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/${var1}_daily${suffix}/r${member}i1p1f1/
var2_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/${var2}_daily${suffix}/r${member}i1p1f1/

var1_no_transient=${var1//transient/}
output_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/${var1}_${var2}_sum_daily${suffix}/r${member}i1p1f1/

echo "Ensemble member ${member}"

mkdir -p ${output_dir}
export var1
export var2
export var1_path
export var2_path
export output_dir
export member

sum(){
    dec=$1
    var1_file=$(find ${var1_path} -name "*${dec}*.nc" | head -n 1)
    var2_file=$(find ${var2_path} -name "*${dec}*.nc" | head -n 1)
    if [ -z "$var1_file" ] || [ -z "$var2_file" ]; then
        echo "Files not found for date: $dec"
        return
    fi
    output_file=${output_dir}${var1}_${var2}_daily_${dec}.nc
    cdo -P 2 -O -add -sellevel,$plev ${var1_file} -sellevel,$plev ${var2_file} ${output_file}
}

export -f sum

parallel --jobs 5 --tmpdir /scratch/m/m300883/parallel sum ::: {1850..2090..10}