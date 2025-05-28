#!/bin/bash
# decade
decade=$1
# sbatch 4var_NAO_range_submit.sh $decade wb_anticyclonic flag MPI_GE_CMIP6_allplev
# sbatch 4var_NAO_range_submit.sh $decade wb_cyclonic flag MPI_GE_CMIP6_allplev

sbatch 4var_NAO_range_submit.sh $decade upvp upvp MPI_GE_CMIP6_allplev
sbatch 4var_NAO_range_submit.sh $decade vpetp vpetp MPI_GE_CMIP6_allplev
# sbatch 4var_NAO_range_submit.sh $decade upqp upqp MPI_GE_CMIP6_allplev
# sbatch 4var_NAO_range_submit.sh $decade vpqp vpqp MPI_GE_CMIP6_allplev

sbatch 4var_NAO_range_submit.sh $decade usvs usvs MPI_GE_CMIP6_allplev
sbatch 4var_NAO_range_submit.sh $decade vsets vsets MPI_GE_CMIP6_allplev
