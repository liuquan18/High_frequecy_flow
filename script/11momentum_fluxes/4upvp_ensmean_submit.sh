#!/bin/bash

for decade in {1850..2090..10}
do
    echo "This node is calculating upvp for ${decade} to $((decade+9))"
    sbatch 4upvp_ensmean.sh $decade 

done