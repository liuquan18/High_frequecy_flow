#!/bin/bash
#SBATCH --job-name=basin
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=25
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=basin.%j.out

module load cdo parallel


NAL(){
    infile=$1
    fname=$(basename ${infile%.nc})

    echo "NAL $fname"

    outfile=$NALdir$fname.nc

    cdo -P 8 -fldmean -sellonlatbox,290,325,20,60 $infile $outfile  
}

NPO(){
    infile=$1
    fname=$(basename ${infile%.nc})

    echo "NPO $fname"

    outfile=$NPOdir$fname.nc

    cdo -P 8 -fldmean -sellonlatbox,290,325,20,60 $infile $outfile  
}

export -f NAL NPO

var=$1
export var


process(){
    member=$1

    basedir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/$var/r${member}i1p1f1/
    NALdir=/scratch/m/m300883/NAL/${var}/r${member}i1p1f1/
    NPOdir=/scratch/m/m300883/NPO/${var}/r${member}i1p1f1/

    export basedir NALdir NPOdir


    mkdir -p $NALdir $NPOdir

    # parallel
    find "$basedir" -name "*.nc" | parallel -j 25 NAL 
    find "$basedir" -name "*.nc" | parallel -j 25 NPO
}

for member in {1..50}
do
    echo $member is processed
    process $member

done