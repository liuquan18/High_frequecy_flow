#!/bin/bash
infile=$1
outfile=${infile/zg_daily/zg_daily_ano}

# get the decade label from $infile name
decade_label=$(basename "$infile" | cut -d'_' -f 6 | cut -c1-4)
month_ens=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_monthly_ensmean/${var}_monmean_ensmean_${decade_label}05_$((${decade_label}+9))09.nc

cdo -O -ymonsub ${infile} ${month_ens} ${outfile}