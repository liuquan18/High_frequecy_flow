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

NPC(){
    infile=$1
    fname=$(basename ${infile%.nc})

    echo "NPC $fname"

    outfile=$NPCdir$fname.nc

    cdo -P 8 -fldmean -sellonlatbox,290,325,20,60 $infile $outfile  
}

export -f NAL NPC

var=$1
export var


process(){
    member=$1

    basedir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/$var/r${member}i1p1f1/
    NALdir=/scratch/m/m300883/NAL/${var}/r${member}i1p1f1/
    NPCdir=/scratch/m/m300883/NPC/${var}/r${member}i1p1f1/

    export basedir NALdir NPCdir


    mkdir -p $NALdir $NPCdir

    # parallel
    find "$basedir" -name "*.nc" | parallel -j 25 NAL 
    find "$basedir" -name "*.nc" | parallel -j 25 NPC
}

for member in {1..50}
do
    echo $member is processed
    process $member

done