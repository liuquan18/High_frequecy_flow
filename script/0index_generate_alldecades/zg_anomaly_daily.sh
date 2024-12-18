#!/bin/bash
#!/bin/bash
#SBATCH --job-name=ano
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=7
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=ano.%j.out

# subtract the ensemble mean of the monthly data from the daily data using cdo monsub
# by doing which a long-term trend and seasonal cycle are removed
module load cdo
module load parallel

# get the ensemble member from the command line
member=$1

# Define file paths for both scenarios
historical_path=/pool/data/CMIP6/data/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r${member}i1p1f1/day/zg/gn/v????????/
ssp585_path=/work/ik1017/CMIP6/data/CMIP6/ScenarioMIP/MPI-M/MPI-ESM1-2-LR/ssp585/r${member}i1p1f1/day/zg/gn/v????????/

zg_ano_save_path=/scratch/m/m300883/zg_day_ano/r${member}i1p1f1/
mkdir -p $zg_ano_save_path
export zg_ano_save_path

# Define function called Anomaly
Anomaly() {
    infile=$1

    year_start=$(cdo showyear $infile | awk '{print $1}')
    year_end=$(cdo showyear $infile | awk '{print $NF}')

    # Get the filename
    filename=$(basename $infile)
    outfile=$zg_ano_save_path${filename%.*}_ano.nc


    # Include month May and September for later rolling window
    cdo -monsub -sellevel,100000,85000,70000,50000,25000 -sellonlatbox,-90,40,20,80 -selmonth,5,6,7,8,9 \
        $infile \
        -selyear,$year_start/$year_end /work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/zg_MJJAS_ensmean/zg_Amon_MPI-ESM1-2-LR_HIST_ssp585_ensmean_MJJAS.nc \
        $outfile
}

export -f Anomaly

# Find files for both scenarios and combine the lists
file_list=$(find $historical_path -name "*.nc" -print; find $ssp585_path -name "*.nc" -print)

# Parallel the data processing on the combined file list
echo "$file_list" | parallel --jobs 7 Anomaly
