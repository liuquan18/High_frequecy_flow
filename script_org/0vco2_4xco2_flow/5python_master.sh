#!/bin/bash


var=$1 # variable name

for simulations in 'vco2_4xco2_land' 'vco2_4xco2_all' 'vco2_4xco2_land_mlo' 'vco2_4xco2_ocean'
do
    echo "Simulation ${simulations}"
    # run the python script
    sbatch 5python_submit.sh ${simulations} $var
done