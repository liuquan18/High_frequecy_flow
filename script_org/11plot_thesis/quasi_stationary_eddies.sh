#!/bin/bash
#SBATCH --job-name=zg_hat
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=46
#SBATCH --ntasks=46
#SBATCH --cpus-per-task=8
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=zg_hat.%j.out


module load cdo/2.5.0-gcc-11.2.0
module load parallel

infile=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_monthly_stat/zg_50000_monthly_05_09.nc

tmpfile=/scratch/m/m300883/zg_50000_monthly_05_09_detrend.nc
outfile=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_monthly_stat/zg_50000_monthly_05_09_zonalano.nc


# detrend data
cdo -r -O -P 8 -detrend $infile $tmpfile

cdo -P 8 -r -sub ${tmpfile} -enlarge,${tmpfile} -zonmean ${tmpfile} ${outfile}