#!/bin/bash
#SBATCH --job-name=slope
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=slope.%j.out


python -u 7tangent_line_slope_decade_cal.py $1 # node, var
