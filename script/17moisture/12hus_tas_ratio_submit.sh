#!/bin/bash
#SBATCH --job-name=vertmean
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=250
#SBATCH --ntasks=1250
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=vertmean.%j.out

module load cdo
module load parallel

echo "Number of nodes allocated: $SLURM_NNODES"
echo "Number of tasks per node: $SLURM_NTASKS_PER_NODE"


# get the ensemble member from the command line

CMD_FOUT=12commands.txt

read_daily_files() {
    local var=$1
    local daily_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_std/r*i1p1f1/
    local daily_file=${var}_day_MPI-ESM1-2-LR_r*i1p1f1_gn_*.nc
    daily_files=($(find $daily_path -name $daily_file -print))
}

# Generate hus daily files
read_daily_files "hus"
hus_daily_files=("${daily_files[@]}")

# Generate tas daily files
read_daily_files "tas"
tas_daily_files=("${daily_files[@]}")

for member in {1..50}; do
    save_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_daily_std/r${member}i1p1f1/
    mkdir -p $save_dir
done




parallel --dryrun -j 25 /work/mh0033/m300883/High_frequecy_flow/script/17moisture/12hus_tas_ratio.sh {1} {2} ::: ${hus_daily_files[@]} ::: ${tas_daily_files[@]} >$CMD_FOUT

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
