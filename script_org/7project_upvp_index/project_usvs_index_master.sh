#!/bin/bash
for ens in {1..50}
do
    sbatch project_usvs_index_submit.sh $ens
done