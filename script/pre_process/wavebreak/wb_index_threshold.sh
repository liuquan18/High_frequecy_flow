#!/bin/bash
# bandpass filter 2-12 days with cdo
module load cdo
module load parallel

period=first10


wb_index_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wavebreak_index/wb_${period}/

to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wavebreak_events/wave_break_event_threshold/


mkdir -p ${to_path}

files=$(find ${wb_index_path} -name wb_index_*.nc)


cdo -P 10 -ensmean -apply,ydaystd [ ${files} ] ${to_path}wb_index_threshold_cdo.nc