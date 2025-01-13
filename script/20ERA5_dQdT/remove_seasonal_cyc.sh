#!/bin/bash
#SBATCH --job-name=cyc
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=25
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=cyc.%j.out

module load cdo
module load parallel

season_cyc=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_monthly_stat/zg_50000_seasonal_cyc_05_09.nc
daily_dir=/pool/data/ERA5/E5/pl/an/1D/129/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_daily_rm_seacyc/
export season_cyc daily_dir to_dir 

Mayfiles=($(find $daily_dir -name "*.grb" -print | grep '\-05_129\.grb$'))
Junfiles=($(find $daily_dir -name "*.grb" -print | grep '\-06_129\.grb$'))
Julfiles=($(find $daily_dir -name "*.grb" -print | grep '\-07_129\.grb$'))
Augfiles=($(find $daily_dir -name "*.grb" -print | grep '\-08_129\.grb$'))
Sepfiles=($(find $daily_dir -name "*.grb" -print | grep '\-09_129\.grb$'))

daily_files=(${Mayfiles[@]} ${Junfiles[@]} ${Julfiles[@]} ${Augfiles[@]} ${Sepfiles[@]})

Remove_seasonal_cyc() {
    infile=$1
    echo Processing $(basename $infile)
    outfile=${to_dir}$(basename $infile .grb)_rm_seacyc.nc
    cdo -f nc -O -P 8 -divc,9.80665 -ymonsub -sellevel,50000 -sellonlatbox,-90,40,20,80 -setgridtype,regular $infile -sellonlatbox,-90,40,20,80 -setgridtype,regular $season_cyc $outfile
}

export -f Remove_seasonal_cyc

parallel --jobs 25 Remove_seasonal_cyc ::: ${daily_files[@]}