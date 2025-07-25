#!/bin/bash
infile=$1
echo $SLURM_PROCID is Processing ${infile}

tmp_dir=/scratch/m/m300883/zg/

# replace 'zg_daily_ano' to 'zg_NA_daily_ano'
outfile=${infile/zg_daily/zg_NA_daily_ano}

tmpfile=${tmp_dir}$(basename ${outfile})

# select region and plev, filterout day-to-day variability
cdo -P 10 -lowpass,183 -sellevel,50000 -sellonlatbox,-90,40,20,80 ${infile} ${tmpfile}

# daily anomaly
cdo -P 10 -ydaysub ${tmpfile} -ydaymean ${tmpfile} ${outfile}