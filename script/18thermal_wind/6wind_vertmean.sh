#!/bin/bash
moduel load cdo
module load parallel

infile=$1

echo Processing $(basename $infile)

# replace _ano with _ano_lowlevel
outfile=${infile//_ano/_ano_lowlevel}
cdo -P 8 -vertmean -sellevel,100000,85000 $infile $outfile