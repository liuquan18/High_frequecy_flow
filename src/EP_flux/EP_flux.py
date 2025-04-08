
#%%
import xarray as xr
import numpy as np
# %%
# constants
kappa 		= 2./7.
L 			= 2.5e6   # J/kg Latent heat of vaporization
cp 			= 1004.67 # J/kg/K Specific heat at constant pressure


#%%
def potential_temperature(t, p = 'plev', p0 = 1e5):

	# theta = T (p0/p)**kappa       (2.44)

    # pressure quanttities
    p0p = (p0/t[p])**kappa

    # potential temperature
    theta = t * p0p
    theta.name = 'theta'
    theta.attrs['units'] = 'K'
    theta.attrs['long_name'] = 'potential temperature'
    theta.attrs['standard_name'] = 'potential_temperature'
    return theta

def equivalent_potential_temperature(t, q, p = 'plev', p0 = 1e5):
	theta = potential_temperature(t, p, p0)
	# equivalent potential temperature
	# theta_e = theta * exp ( (L*qs)/ (cp * T))      (2.70)
	# where qs = q / (1 - q)  saturation mixing ratio
	qs = q / (1 - q)
	ept = theta * np.exp((L*qs)/(cp*t))
	ept.name = 'etheta'
	ept.attrs['units'] = 'K'
	ept.attrs['long_name'] = 'equivalent potential temperature'
	ept.attrs['standard_name'] = 'equivalent_potential_temperature'
	return ept

def Theta_P(theta):
	t = theta # ensemble mean of theta
	t_bar = t.mean('lon') # t_bar = theta_bar
	# prepare pressure derivative
	dthdp = t_bar.differentiate('plev',edge_order=2) # dthdp = d(theta_bar)/dp
	dthdp = dthdp.where(dthdp != 0)

	# time mean
	dthdp_mean = dthdp.mean('time')

	return dthdp_mean	
