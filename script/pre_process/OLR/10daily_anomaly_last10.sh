#!/bin/bash
module load cdo
module load parallel

# lists
base_dir=/work/ik1017/CMIP6/data/CMIP6/ScenarioMIP/MPI-M/MPI-ESM1-2-LR/ssp585/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/last10_OLR_daily_ano/
tmp_dir=/scratch/m/m300883/OLR/



export to_dir base_dir tmp_dir

# define the function
Anomaly() {

    infile=$1
    monthfile=$2
    savedir=$3
    outfile=${savedir}$(basename ${infile})
    # include month Mayb and september for later rolling window
    cdo -monsub -selmon,5/9 -sellonlatbox,-180,180,-30,30 ${infile} -sellonlatbox,-180,180,-30,30 ${monthfile} ${outfile}
}

export -f Anomaly

for member in {1..50}
do
    infile_list1=$(find ${base_dir}r${member}i1p1f1/day/ -name 'rlut_day_MPI-ESM1-2-LR_ssp585_r'${member}'i1p1f1_gn_20750101-20941231.nc')
    infile_list2=$(find ${base_dir}r${member}i1p1f1/day/ -name 'rlut_day_MPI-ESM1-2-LR_ssp585_r'${member}'i1p1f1_gn_20950101-21001231.nc')
    for infile in $infile_list1
    do
        daily_list1+="$infile "
    done
    for infile in $infile_list2
    do
        daily_list2+="$infile "
    done
done

# Remove the trailing space
daily_list1=$(echo $daily_list1 | sed 's/ $//')
daily_list2=$(echo $daily_list2 | sed 's/ $//')

month_ens1=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_season_global/rlut_Amon_MPI-ESM1-2-LR_HIST_ensmean_207505-209409.nc
month_ens2=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_season_global/rlut_Amon_MPI-ESM1-2-LR_HIST_ensmean_209505-210009.nc

savedir1=${tmp_dir}list1/
savedir2=${tmp_dir}list2/


parallel --jobs 20 Anomaly ::: ${daily_list1} ::: ${month_ens1} ::: ${savedir1}

parallel --jobs 20 Anomaly ::: ${daily_list2} ::: ${month_ens2} ::: ${savedir2}


