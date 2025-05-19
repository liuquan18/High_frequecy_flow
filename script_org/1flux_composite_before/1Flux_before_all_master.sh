#!/bin/bash
window=$1


# ua hat
echo "ua hat before $window"
sbatch 1Flux_before_NAO_submit.sh 1850 ua_hat ua $window
sbatch 1Flux_before_NAO_submit.sh 2090 ua_hat ua $window

# va hat
echo "va hat before $window"
sbatch 1Flux_before_NAO_submit.sh 1850 va_hat va $window
sbatch 1Flux_before_NAO_submit.sh 2090 va_hat va $window

# upvp
echo "upvp before $window"
sbatch 1Flux_before_NAO_submit.sh 1850 upvp upvp $window
sbatch 1Flux_before_NAO_submit.sh 2090 upvp upvp $window

# vpetp
echo "vpetp before $window"
sbatch 1Flux_before_NAO_submit.sh 1850 vpetp vpetp $window
sbatch 1Flux_before_NAO_submit.sh 2090 vpetp vpetp $window

# upqp
echo "upqp before $window"
sbatch 1Flux_before_NAO_submit.sh 1850 upqp upqp $window
sbatch 1Flux_before_NAO_submit.sh 2090 upqp upqp $window

# vpqp
echo "vpqp before $window"
sbatch 1Flux_before_NAO_submit.sh 1850 vpqp vpqp $window
sbatch 1Flux_before_NAO_submit.sh 2090 vpqp vpqp $window
