#!/bin/bash

for year in {1979..2024}
do

    sbatch 6uhat.sh $year

done