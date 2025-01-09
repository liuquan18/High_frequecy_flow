#!/bin/bash
infile=$1
echo $SLURM_PROCID is Processing ${infile}

# replace 'zg_daily_ano' to 'zg_NA_daily_ano'
outfile=${infile/zg_daily_ano/zg_NA_daily_ano}

cdo -P 10 -sellevel,25000 -sellonlatbox,-90,40,20,80 ${infile} ${outfile}
