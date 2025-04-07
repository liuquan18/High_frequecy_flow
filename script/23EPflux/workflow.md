
# 1. calcute theta
cd /work/mh0033/m300883/High_frequecy_flow/script/23EPflux
conda activate air_sea

## calculate the potential temperature
`./0python_master.sh 1potential_temperature.py`

## calculate the equivalent potential temperature
`./0python_master.sh 2equiv_potential_temperature.py`

--------
# 2. ensemble mean 
cd /work/mh0033/m300883/High_frequecy_flow/script/pre_process/daily_anomaly


## ensemble mean of the potential temperature
`sbatch monmean_ensmean_parallel_srun.sh theta`

## ensemble mean of the equivalent potential temperature
`sbatch monmean_ensmean_parallel_srun.sh equiv_theta`

--------
# 3. calculate the primes
cd /work/mh0033/m300883/High_frequecy_flow/script/pre_process/prime

## theta prime
`./0var_prime_master.sh theta`

## equiv theta prime
`./0var_prime_master.sh equiv_theta`

-------
# 4. calculate the fluxes
cd /work/mh0033/m300883/High_frequecy_flow/script/pre_process/prime

## vptp
`./3eddy_flux_master.sh vptp`

## vpetp
`./3eddy_flux_master.sh vptep`

------
# 5. ensemble mean of the fluxes
cd /work/mh0033/m300883/High_frequecy_flow/script/pre_process/daily_anomaly

## ensemble mean of the vptp
`sbatch monmean_ensmean_parallel_srun.sh vptp`
## ensemble mean of the vptep
`sbatch monmean_ensmean_parallel_srun.sh vptep`
------
# 6. calculate the fluxes anomaly
cd /work/mh0033/m300883/High_frequecy_flow/script/pre_process/daily_anomaly
## calculate the fluxes anomaly
`./daily_anomaly_allens.sh vptp`

`./daily_anomaly_allens.sh vptep`

