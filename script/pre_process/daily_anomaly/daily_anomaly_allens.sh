#!/bin/bash
#SBATCH --job-name=ano
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=50
#SBATCH --ntasks-per-node=1
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=ano.%j.out

var=$1
# #for loop 1-50
# for ens in {1..50}
# do
#     echo "Ensemble member ${ens}"
#     # run the python script
#     sbatch daily_anomaly_single_ensemble.sh ${ens} ${var}
#     # ./daily_anomaly_single_ensemble.sh ${ens} ${var}
# done

module load parallel

parallel --jobs $SLURM_NTASKS srun --nodes=1 --ntasks-per-node=1 --cpus-per-task=5 daily_anomaly_single_ensemble.sh ::: {1..50} ::: $var ::: {0..24}
