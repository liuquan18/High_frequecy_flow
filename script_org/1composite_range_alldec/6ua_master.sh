#!/bin/bash
var='ua_hat'
var_name='ua'
model_dir='MPI_GE_CMIP6_allplev'
plev=None # all levels


for decade in {1850..2090..10}
do
    echo "submit: $decade"
    sbatch 5var_NAO_range_distribution_submit.sh $decade $var $var_name $model_dir $plev
done