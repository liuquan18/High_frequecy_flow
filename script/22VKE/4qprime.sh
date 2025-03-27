#!/bin/bash
#SBATCH --job-name=qp
#SBATCH --time=01:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=qp.%j.out

module load cdo
module load parallel

node=$1
member=$node
echo "Ensemble member ${member}"

frequency=${2:-prime} # prime (2-12 days) or high (2-6 days), default prime

q_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r${member}i1p1f1/


if [ "$frequency" == "prime" ]; then
    qp_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_prime_daily/r${member}i1p1f1/
else
    qp_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_prime_high_daily/r${member}i1p1f1/
fi

tmp_dir=/scratch/m/m300883/qp/r${member}i1p1f1/

mkdir -p ${qp_path} ${tmp_dir}


export qp_path member tmp_dir
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

q_prime(){
    dec=$1
    qfile=$(find ${q_path} -name "*${dec}*.nc")
    qfile=$(echo $qfile | tr -d '\n')
    echo "Processing ${qfile}"
    qfile_name=$(basename ${qfile})
    qpfile_name=${qp_path}${qfile_name//hus/hus_prime}

    echo " band filter ${qfile_name}"
    band_filter ${qfile} ${qpfile_name}
}

export -f band_filter
export -f q_prime

parallel -j 5 q_prime ::: {1850..2090..10}

# check completion
for dec in {1850..2090..10}; do
    if [! -f ${qp_path}/*${dec}*.nc]; then
        echo "Decade ${dec} is missing"
        echo "Recalculate decade ${dec}"
        q_prime ${dec}
    fi
done