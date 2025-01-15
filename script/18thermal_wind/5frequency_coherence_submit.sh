#!/bin/bash
#SBATCH --job-name=coherence
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=5
#SBATCH --ntasks=50
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=coherence.%j.out




parallel --dryrun python /work/mh0033/m300883/High_frequecy_flow/script/18thermal_wind/5frequency_coherence.py ::: {1..50} >5commands.txt

# run parallel for each node
driver_fn () {
    echo "$SLURM_NODEID"

    cat $CMD_FOUT | \
    awk -v NNODE="$SLURM_NNODES" -v NODEID="$SLURM_NODEID" 'NR % NNODE == NODEID' | \
    parallel -j $SLURM_NTASKS_PER_NODE {}
}

export -f driver_fn
# the script will be executed ${SLURM_NTASKS} times
echo $SLURM_NTASKS
srun --ntasks=$SLURM_JOB_NUM_NODES bash -c "$(declare -p CMD_FOUT); driver_fn"
