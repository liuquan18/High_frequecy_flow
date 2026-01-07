#!/bin/bash

#for loop 1-50
for decade in {1850..2090..10}
do
    echo "Processing decade ${decade}"
    # run the python script
    sbatch wb_fldmean_submit.sh ${decade}
done