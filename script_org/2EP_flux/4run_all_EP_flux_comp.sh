#!/bin/bash

# transient
## pos
sbatch ./4EP_flux_submit.sh pos 1850 transient False
sbatch ./4EP_flux_submit.sh pos 2090 transient False

## neg
sbatch ./4EP_flux_submit.sh neg 1850 transient False
sbatch ./4EP_flux_submit.sh neg 2090 transient False

# steady
## pos
sbatch ./4EP_flux_submit.sh pos 1850 steady False
sbatch ./4EP_flux_submit.sh pos 2090 steady False

## neg
sbatch ./4EP_flux_submit.sh neg 1850 steady False
sbatch ./4EP_flux_submit.sh neg 2090 steady False