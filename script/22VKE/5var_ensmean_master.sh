#!/bin/bash
var=$1
for decade in {1850..2090..10}
do
    echo "This node is calculating upvp for ${decade} to $((decade+9))"
    sbatch 5var_ensmean.sh $decade $var

done