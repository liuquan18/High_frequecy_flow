#!/bin/bash
#SBATCH --job-name=ano
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=7
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=ano.%j.out

module load cdo
module load parallel

# get the ensemble member from the command line
member=$1
var=$2
echo "Ensemble member ${member}"


# vt daily
vt_daily_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily/r${member}i1p1f1/
vt_daily_file=${var}_day_MPI-ESM1-2-LR_r${member}i1p1f1_gn_*.nc
daily_files=($(find $vt_daily_path -name $vt_daily_file -print))


savedir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_ano/r${member}i1p1f1/
mkdir -p $savedir

export savedir

# define the function
Anomaly() {

    infile=$1
    month_ens=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_monthly_ensmean/first10_${var}_monthly_ymonmean_ensmean.nc

    cdo -ymonsub ${infile} ${month_ens} ${savedir}$(basename ${infile} .nc)_ano.nc
}


export -f Anomaly
parallel --jobs 10 Anomaly ::: ${daily_files[@]}