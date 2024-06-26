#!/bin/bash
#SBATCH --job-name=mergetime
#SBATCH --time=08:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH --output=log.o-%j.out
#SBATCH --error=log.o-%j.out
#SBATCH --account=mh0033
#SBATCH --partition=compute
### SBATCH --mem=400G
#SBATCH --exclusive 




module load cdo
module load parallel



mergetime(){
    member=$1
    scenario=ssp585
    var=zg
    resolution=day
    echo "Merging files for ${scenario} ${member} with historical"
    # list of files to be merged
    HISTdir=/pool/data/CMIP6/data/CMIP/MPI-M/MPI-ESM1-2-LR/historical/
    SCENdir=/pool/data/CMIP6/data/ScenarioMIP/MPI-M/MPI-ESM1-2-LR/

    TO=/scratch/m/m300883/MPI_GE_CMIP6/mergetime/

    Histfiles=${HISTdir}r${member}i1p1f1/${resolution}/${var}/gn/v????????/*.nc
    Scenfiles=${SCENdir}${scenario}/r${member}i1p1f1/${resolution}/${var}/gn/v????????/*.nc
    
    cdo -O -mergetime [ ${Histfiles[@]} ${Scenfiles[@]} ] ${TO}zg_r${member}i1p1f1_day_${scenario}_historical.nc

}

export -f mergetime

parallel --jobs 5 mergetime ::: {1..50}