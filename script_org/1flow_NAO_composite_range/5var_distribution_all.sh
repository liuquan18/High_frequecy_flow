#!/bin/bash

sbatch 5var_NAO_range_distribution_submit.sh 1850 vpetp vpetp MPI_GE_CMIP6_allplev #no suffix
sbatch 5var_NAO_range_distribution_submit.sh 2090 vpetp vpetp MPI_GE_CMIP6_allplev 

sbatch 5var_NAO_range_distribution_submit.sh 1850 vsets vsets MPI_GE_CMIP6_allplev #no suffix
sbatch 5var_NAO_range_distribution_submit.sh 2090 vsets vsets MPI_GE_CMIP6_allplev

sbatch 5var_NAO_range_distribution_submit.sh 1850 ta ta MPI_GE_CMIP6_allplev #no suffix
sbatch 5var_NAO_range_distribution_submit.sh 2090 ta ta MPI_GE_CMIP6_allplev

sbatch 5var_NAO_range_distribution_submit.sh 1850 M2_prime M2 MPI_GE_CMIP6_allplev #no suffix
sbatch 5var_NAO_range_distribution_submit.sh 2090 M2_prime M2 MPI_GE_CMIP6_allplev

sbatch 5var_NAO_range_distribution_submit.sh 1850 M2_steady M2 MPI_GE_CMIP6_allplev #no suffix
sbatch 5var_NAO_range_distribution_submit.sh 2090 M2_steady M2 MPI_GE_CMIP6_allplev