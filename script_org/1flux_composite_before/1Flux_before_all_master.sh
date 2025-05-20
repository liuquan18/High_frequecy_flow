#!/bin/bash
window=$1

suffix=$2


# # ua
echo "ua hat before $window $suffix"
sbatch 1Flux_before_NAO_submit.sh 1850 ua ua $window # no '_ano'
sbatch 1Flux_before_NAO_submit.sh 2090 ua ua $window 

# va
echo "va hat before $window $suffix"
sbatch 1Flux_before_NAO_submit.sh 1850 va va $window
sbatch 1Flux_before_NAO_submit.sh 2090 va va $window 

# # zg
# echo "zg before $window $suffix"
# sbatch 1Flux_before_NAO_submit.sh 1850 zg zg $window $suffix 
# sbatch 1Flux_before_NAO_submit.sh 2090 zg zg $window $suffix

# theta
echo "theta before $window $suffix"
sbatch 1Flux_before_NAO_submit.sh 1850 theta theta $window # no '_ano'
sbatch 1Flux_before_NAO_submit.sh 2090 theta theta $window 

# # etheta
# echo "etheta before $window $suffix"
# sbatch 1Flux_before_NAO_submit.sh 1850 equiv_theta etheta $window 
# sbatch 1Flux_before_NAO_submit.sh 2090 equiv_theta etheta $window 


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
