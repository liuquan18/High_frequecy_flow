# ...existing code...
#!/usr/bin/env bash
# var=$1
# BASE_DIR="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_std"
BASE_DIR=$1
missing=0

for i in {1..50}; do
  subdir="${BASE_DIR}/r${i}i1p1f1"
  if [ ! -d "$subdir" ]; then
    echo "Missing folder: r${i}i1p1f1"
    missing=1
  else
    n_files=$(find "$subdir" -type f | wc -l)
    if [ "$n_files" -ne 25 ]; then
      echo "Folder r${i}i1p1f1 has $n_files files, expected 25"
      missing=1
    fi
  fi
done

if [ "$missing" -eq 0 ]; then
  echo "All subfolders have 25 files."
else
  echo "Some subfolders are missing or do not have 25 files."
fi