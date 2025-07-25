#!/bin/bash
#SBATCH --job-name=comp_NAO_range
#SBATCH --time=06:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=400G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=composite.%j.out

var=${1:-upvp} # variable name, default is 'upvp'
name=${2:-${var}}    # name, default is empty


python -u 4var_NAO_range.py $var $name
