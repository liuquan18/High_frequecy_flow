#!/bin/bash
#SBATCH --job-name=absvort
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=5
#SBATCH --ntasks=25
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=absvort.%j.out


mpirun -n 25 python -u 8hus_before_wb.py
