#!/bin/bash

# transient
## pos
sbatch ./4EP_flux_isentropes_submit.sh pos 1850 True transient False
sbatch ./4EP_flux_isentropes_submit.sh pos 2090 True transient False

## neg
sbatch ./4EP_flux_isentropes_submit.sh neg 1850 True transient False
sbatch ./4EP_flux_isentropes_submit.sh neg 2090 True transient False

# steady
## pos
sbatch ./4EP_flux_isentropes_submit.sh pos 1850 True steady False
sbatch ./4EP_flux_isentropes_submit.sh pos 2090 True steady False

## neg
sbatch ./4EP_flux_isentropes_submit.sh neg 1850 True steady False
sbatch ./4EP_flux_isentropes_submit.sh neg 2090 True steady False