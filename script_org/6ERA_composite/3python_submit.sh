#!/bin/bash
#SBATCH --job-name=python
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=python.%j.out

file=$1 # python file to run
var=${2:-upvp} # variable name, default is 'upvp'
name=${3:-${var}}    # name, default is empty


python -u $file $var $name
