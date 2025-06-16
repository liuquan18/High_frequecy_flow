#!/bin/bash

sbatch 5var_NAO_range_distribution_submit.sh 1850 upvp upvp MPI_GE_CMIP6_allplev
sbatch 5var_NAO_range_distribution_submit.sh 2090 upvp upvp MPI_GE_CMIP6_allplev

sbatch 5var_NAO_range_distribution_submit.sh 1850 usvs usvs MPI_GE_CMIP6_allplev
sbatch 5var_NAO_range_distribution_submit.sh 2090 usvs usvs MPI_GE_CMIP6_allplev

sbatch 5var_NAO_range_distribution_submit.sh 1850 vpetp vpetp MPI_GE_CMIP6_allplev #no suffix
sbatch 5var_NAO_range_distribution_submit.sh 2090 vpetp vpetp MPI_GE_CMIP6_allplev 

sbatch 5var_NAO_range_distribution_submit.sh 1850 vsets vsets MPI_GE_CMIP6_allplev #no suffix
sbatch 5var_NAO_range_distribution_submit.sh 2090 vsets vsets MPI_GE_CMIP6_allplev

sbatch 5var_NAO_range_distribution_submit.sh 1850 ta ta MPI_GE_CMIP6_allplev #no suffix
sbatch 5var_NAO_range_distribution_submit.sh 2090 ta ta MPI_GE_CMIP6_allplev

sbatch 5var_NAO_range_distribution_submit.sh 1850 ta_hat ta MPI_GE_CMIP6_allplev #no suffix
sbatch 5var_NAO_range_distribution_submit.sh 2090 ta_hat ta MPI_GE_CMIP6_allplev

sbatch 5var_NAO_range_distribution_submit.sh 1850 M2_prime M2 MPI_GE_CMIP6_allplev #no suffix
sbatch 5var_NAO_range_distribution_submit.sh 2090 M2_prime M2 MPI_GE_CMIP6_allplev

sbatch 5var_NAO_range_distribution_submit.sh 1850 M2_steady M2 MPI_GE_CMIP6_allplev #no suffix
sbatch 5var_NAO_range_distribution_submit.sh 2090 M2_steady M2 MPI_GE_CMIP6_allplev



sbatch ./5var_NAO_range_distribution_submit.sh 1850 Fdiv_p_transient div2 MPI_GE_CMIP6_allplev 85000 
sbatch ./5var_NAO_range_distribution_submit.sh 2090 Fdiv_p_transient div2 MPI_GE_CMIP6_allplev 85000 

sbatch ./5var_NAO_range_distribution_submit.sh 1850 Fdiv_phi_transient div MPI_GE_CMIP6_allplev 25000 
sbatch ./5var_NAO_range_distribution_submit.sh 2090 Fdiv_phi_transient div MPI_GE_CMIP6_allplev 25000 

sbatch ./5var_NAO_range_distribution_submit.sh 1850 Fdiv_p_steady div2 MPI_GE_CMIP6_allplev 85000 
sbatch ./5var_NAO_range_distribution_submit.sh 2090 Fdiv_p_steady div2 MPI_GE_CMIP6_allplev 85000 

sbatch ./5var_NAO_range_distribution_submit.sh 1850 Fdiv_phi_steady div MPI_GE_CMIP6_allplev 25000 
sbatch ./5var_NAO_range_distribution_submit.sh 1850 Fdiv_phi_transient div MPI_GE_CMIP6_allplev 25000 