#!/bin/bash

# transient
## pos
sbatch ./4EP_flux_submit.sh pos 1850 False transient False
sbatch ./4EP_flux_submit.sh pos 2090 False transient False

## neg
sbatch ./4EP_flux_submit.sh neg 1850 False transient False
sbatch ./4EP_flux_submit.sh neg 2090 False transient False

# steady
## pos
sbatch ./4EP_flux_submit.sh pos 1850 False steady False
sbatch ./4EP_flux_submit.sh pos 2090 False steady False

## neg
sbatch ./4EP_flux_submit.sh neg 1850 False steady False
sbatch ./4EP_flux_submit.sh neg 2090 False steady False