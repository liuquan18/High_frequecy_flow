#!/bin/bash
#SBATCH --job-name=Tp
#SBATCH --time=01:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=Tp.%j.out

module load cdo
module load parallel

node=$1
member=$node
echo "Ensemble member ${member}"
var=$2
echo "Variable ${var}"
frequency=${3:-prime} # prime (2-12 days) or high (2-6 days), default prime

var_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily/r${member}i1p1f1/


if [ "$frequency" == "prime" ]; then
    var_p_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_prime_daily/r${member}i1p1f1/
else
    var_p_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_prime_high_daily/r${member}i1p1f1/
fi

tmp_dir=/scratch/m/m300883/${var}/r${member}i1p1f1/

mkdir -p ${var_p_path} ${tmp_dir}


export var_path var_p_path member tmp_dir
export frequency

# function to band filter
band_filter(){
    infile=$1
    outfile=$2  
    # basename without .nc
    fname=$(basename ${infile%.nc})

    # split years
    cdo -O -splityear ${infile} ${tmp_dir}${fname}_year
    # band filter
    year_files=$(ls ${tmp_dir}${fname}_year*)
    if [ "$frequency" == "prime" ]; then
        echo "Filtering 2-12 days"
        # cdo -O -mergetime -apply,bandpass,30.5,182.5 [ ${year_files} ] ${outfile}
        cdo -O -mergetime -apply,highpass,36.5 [ ${year_files} ] ${outfile}
        elif [ "$frequency" == "high" ]; then
        echo "Filtering 2-6 days"
        # cdo -O -mergetime -apply,bandpass,60.8,182.5 [ ${year_files} ] ${outfile}
        cdo -O -mergetime -apply,highpass,36.5 [ ${year_files} ] ${outfile}
    fi
    # remove temporary files
    rm ${tmp_dir}${fname}_year*
}

prime_func(){
    dec=$1
    Tfile=$(find ${var_path} -name "*${dec}*.nc")
    Tfile=$(echo $Tfile | tr -d '\n')
    echo "Processing ${Tfile}"
    Tfile_name=$(basename ${Tfile})
    Tpfile_name=${var_p_path}${Tfile_name//${var}/${var}_prime}

    echo " band filter ${Tfile_name}"
    band_filter ${Tfile} ${Tpfile_name}
}

export -f band_filter
export -f prime_func

parallel -j 5 prime_func ::: {1850..2090..10}

# check completion
for dec in {1850..2090..10}; do
    if [ ! -f ${var_p_path}/*${dec}*.nc ]; then
        echo "Decade ${dec} is missing"
        echo "Recalculate decade ${dec}"
        prime_func ${dec}
    fi
done