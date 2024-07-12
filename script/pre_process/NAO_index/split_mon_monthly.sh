#!/bin/bash
#SBATCH --job-name=split_mon
#SBATCH --time=08:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=splitmon.%j.out

module load cdo
module load parallel

From_path=/scratch/m/m300883/MPI_GE_CMIP6/mergetime/
To_path=/scratch/m/m300883/MPI_GE_CMIP6/splitmon/
COLLECT=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/
VAR=zg

mkdir -p ${COLLECT}${VAR}_Jan
mkdir -p ${COLLECT}${VAR}_Feb
mkdir -p ${COLLECT}${VAR}_Mar
mkdir -p ${COLLECT}${VAR}_Apr
mkdir -p ${COLLECT}${VAR}_May
mkdir -p ${COLLECT}${VAR}_Jun
mkdir -p ${COLLECT}${VAR}_Jul
mkdir -p ${COLLECT}${VAR}_Aug
mkdir -p ${COLLECT}${VAR}_Sep
mkdir -p ${COLLECT}${VAR}_Oct
mkdir -p ${COLLECT}${VAR}_Nov
mkdir -p ${COLLECT}${VAR}_Dec


echo "_______splitting the files_________"

find ${From_path}*.nc | parallel --jobs 20 cdo -O -splitmon -sellonlatbox,-90,40,20,80 {} ${To_path}{/.}_


echo "_______moving the files_________"
# move the files to the appropriate directory
movefile() {
  local file=$1
  # Get the month from the file name
  month="${file%.nc}"  # Remove the .nc extension
  month="${month##*_}"  # Remove everything before the last underscore

  # Move the file to the appropriate directory
  case $month in
    01) mv "$file" ${COLLECT}${VAR}_Jan/ ;;
    02) mv "$file" ${COLLECT}${VAR}_Feb/ ;;
    03) mv "$file" ${COLLECT}${VAR}_Mar/ ;;
    04) mv "$file" ${COLLECT}${VAR}_Apr/ ;;
    05) mv "$file" ${COLLECT}${VAR}_May/ ;;
    06) mv "$file" ${COLLECT}${VAR}_Jun/ ;;
    07) mv "$file" ${COLLECT}${VAR}_Jul/ ;;
    08) mv "$file" ${COLLECT}${VAR}_Aug/ ;;
    09) mv "$file" ${COLLECT}${VAR}_Sep/ ;;
    10) mv "$file" ${COLLECT}${VAR}_Oct/ ;;
    11) mv "$file" ${COLLECT}${VAR}_Nov/ ;;
    12) mv "$file" ${COLLECT}${VAR}_Dec/ ;;
    *) echo "Invalid month: $month" ;;
  esac
}


export COLLECT
export From_path
export To_path
export VAR
export -f movefile

# Move the files with parallel
parallel --jobs 100 movefile ::: ${To_path}*_??.nc
