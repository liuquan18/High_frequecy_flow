#!/bin/bash

for node in {1..5}
do
    echo "This node is calculating IVKE for node ${node}"
    sbatch 5IVKE_submit.sh $node
done