#!/bin/bash


file=$1 # python file to run

for simulations in 'vco2_4xco2_land' 'vco2_4xco2_all' 'vco2_4xco2_land_mlo' #  'vco2_4xco2_ocean'
do
    echo "Simulation ${simulations}"
    # run the python script
    sbatch 3python_submit.sh $file ${simulations}
done