#!/bin/bash
var=$1
plev=$2
lat_min=$3
lat_max=$4

echo "Processing variable: $var at pressure level: $plev with latitude range: $lat_min to $lat_max"

base_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/${var}_std_decmean/

to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/

mkdir -p $to_path

yearlyfiles=$(ls ${base_path}*.nc)

cdo -O -P 5 -r -sellevel,$plev -fldmean -sellonlatbox,-180,180,$lat_min,$lat_max -mergetime -apply,yearmean [ ${yearlyfiles[@]} ] $to_path${var}_decmean_ensmean_${plev}hPa_lat${lat_min}_${lat_max}.nc
