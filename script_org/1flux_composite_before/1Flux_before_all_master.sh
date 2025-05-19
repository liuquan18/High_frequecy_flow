#!/bin/bash
window=$1

suffix=$2


# ua hat
echo "ua hat before $window $suffix"
sbatch 1Flux_before_NAO_submit.sh 1850 ua_hat ua $window $suffix
sbatch 1Flux_before_NAO_submit.sh 2090 ua_hat ua $window $suffix

# va hat
echo "va hat before $window $suffix"
sbatch 1Flux_before_NAO_submit.sh 1850 va_hat va $window $suffix
sbatch 1Flux_before_NAO_submit.sh 2090 va_hat va $window $suffix

# upvp
echo "upvp before $window $suffix"
sbatch 1Flux_before_NAO_submit.sh 1850 upvp upvp $window $suffix
sbatch 1Flux_before_NAO_submit.sh 2090 upvp upvp $window $suffix

# vpetp
echo "vpetp before $window $suffix"
sbatch 1Flux_before_NAO_submit.sh 1850 vpetp vpetp $window $suffix
sbatch 1Flux_before_NAO_submit.sh 2090 vpetp vpetp $window $suffix

# upqp
echo "upqp before $window $suffix"
sbatch 1Flux_before_NAO_submit.sh 1850 upqp upqp $window $suffix
sbatch 1Flux_before_NAO_submit.sh 2090 upqp upqp $window $suffix

# vpqp
echo "vpqp before $window $suffix"
sbatch 1Flux_before_NAO_submit.sh 1850 vpqp vpqp $window $suffix
sbatch 1Flux_before_NAO_submit.sh 2090 vpqp vpqp $window $suffix
