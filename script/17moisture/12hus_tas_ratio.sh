#!/bin/bash
moduel load cdo
module load parallel

husfile=$1
tasfile=$2


echo Processing $(basename $infile)

# replace _ano with _ano_lowlevel
outfile=${husfile//hus/hus_tas}
cdo -P 10 div $husfile $tasfile $outfile