#!/bin/bash
#SBATCH --job-name=jet_clim
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=jet_clim.%j.out


python -u jet_stream_climatology.py $1 $2
# python -u hello0index_generator.py $1 $2 $3