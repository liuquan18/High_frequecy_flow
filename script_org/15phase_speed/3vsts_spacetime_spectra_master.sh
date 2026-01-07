#!/bin/bash
#for loop 1-50
for ens in {1..50}
do
    # run the python script
    sbatch 3vsts_spacetime_spectra_run.sh ${ens}
done