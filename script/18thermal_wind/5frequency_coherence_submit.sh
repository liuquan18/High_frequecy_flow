#!/bin/bash
#SBATCH --job-name=coherence
#SBATCH --time=03:00:00
#SBATCH --partition=compute
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=5
#SBATCH --ntasks=5
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=coherence.%j.out

module load parallel
module load cdo

member_start=$1
var1=$2
var2=$3
split_basin=$4
pixel_wise=$5

member_end=$(($member_start+4))
echo "node $SLURM_NODEID member_start $member_start member_end $member_end"
parallel --dryrun -j 5 python /work/mh0033/m300883/High_frequecy_flow/script/18thermal_wind/5frequency_coherence.py \
    ::: $(seq ${member_start} ${member_end}) ::: ${var1} ::: ${var2} ::: ${split_basin} ::: ${pixel_wise} >5commands_${member_start}.txt


CMD_FOUT=5commands_${member_start}.txt


echo $SLURM_NTASKS

while IFS= read -r cmd; do
    srun --exclusive -N1 -n1 $cmd &
done < "$CMD_FOUT"
wait