#!/usr/bin/env bash

BASE_DIR=$1
var=$2
missing=0

# Check subfolders
for i in {1..50}; do
  dir="r${i}i1p1f1"
  if [ ! -d "${BASE_DIR}/${dir}" ]; then
    echo "Missing subfolder: ${dir}"
    missing=1
    continue
  fi

  # Check 25 files for each folder
  for ((dec=1850; dec<=2090; dec+=10)); do
    next=$((dec + 9))
    fname="${var}_day_MPI-ESM1-2-LR_r${i}i1p1f1_gn_${dec}0501-${next}0930"
    if [ ! -f "${BASE_DIR}/${dir}/${fname}.nc" ] && [ ! -f "${BASE_DIR}/${dir}/${fname}_ano.nc" ]; then
      echo "Missing file: ${dir}/${fname}.nc or ${dir}/${fname}.ano.nc"
      missing=1
    fi
  done
done

if [ $missing -eq 0 ]; then
  echo "All files are present."
else
  echo "Some files are missing."
fi