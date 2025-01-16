#!/bin/bash
#SBATCH --job-name=ratio
#SBATCH --time=03:00:00
#SBATCH --partition=compute
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks=5
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=ratio.%j.out


module load cdo
module load parallel

echo "Number of nodes allocated: $SLURM_NNODES"
echo "Number of tasks per node: $SLURM_NTASKS_PER_NODE"


# get the ensemble member from the command line

CMD_FOUT=12commands.txt


for member in {1..50}; do
    save_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_daily_std/r${member}i1p1f1/
    mkdir -p $save_dir
done




member_start=$1
member_end=$(($member_start+4))
echo "Ensemble member ${member_start} to ${member_end}"
parallel --dryrun -j 5 /work/mh0033/m300883/High_frequecy_flow/script/17moisture/12hus_tas_ratio.sh ::: $(seq ${member_start} ${member_end}) >12commands_${member_start}.txt


CMD_FOUT=12commands_${member_start}.txt


echo $SLURM_NTASKS

while IFS= read -r cmd; do
    srun --exclusive -N1 -n1 $cmd &
done < "$CMD_FOUT"
wait