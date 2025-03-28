
#%%
import xarray as xr
import numpy as np
# %%
# constants
kappa = 2./7.


#%%
def potential_temperature(t, p = 'plev', p0 = 1e6):

    # pressure quanttities
    p0p = (p0/t[p])**kappa

    # potential temperature
    theta = t * p0p
    theta.name = 'theta'
    theta.attrs['units'] = 'K'
    theta.attrs['long_name'] = 'potential temperature'
    theta.attrs['standard_name'] = 'potential_temperature'
    return theta

#%%
def static_stability (t, p = 'plev', p0 = 1e6, lon = 'lon'):
    """ Computes the potential temperature from temperature and pressure.
        INPUTS:
            t    - temperature, xr.DataArray
            p    - name of pressure
            p0   - reference pressure for potential temperature
            lon  - name of longitude
        OUPUTS:
            dthdp - static stability, xr.DataArray
			(theta_dp) - static stability, xr.DataArray
        
    """
    #
    # some constants
    # from .constants import kappa
    kappa = 2./7.
    #
    pp0 = (p0/t[p])**kappa
    t = t*pp0 # t_p = theta_p
	
    t_bar = t.mean(lon) # t_bar = theta_bar
    # prepare pressure derivative
    dthdp = t_bar.differentiate(p,edge_order=2) # dthdp = d(theta_bar)/dp
    dthdp = dthdp.where(dthdp != 0)
    # time mean of d(theta_bar)/dp
    if 'time' in dthdp.dims:
        dthdp = dthdp.mean('time')

    return dthdp


def cal_VertEddy(vp, tp, Theta_p):
	"""
	vp: v_prime (along time)
	tp: theta_prime (along time)
	static_stability: Theta_p (static stability)
	"""
	vert_eddy = vp * tp / Theta_p
	return vert_eddy
	
	


def ComputeVertEddyXr(v,t,p='level',p0=1e3,lon='lon',time='time',ref='mean',wave=0):
	""" Computes the vertical eddy components of the residual circulation,
		bar(v'Theta'/Theta_p).
		Output units are [v_bar] = [v], [t_bar] = [v*p]

		INPUTS:
			v    - meridional wind, xr.DataArray
			t    - temperature, xr.DataArray
			p    - name of pressure
			p0   - reference pressure for potential temperature
			lon  - name of longitude
			time - name of time field in t
			ref  - how to treat dTheta/dp:
			       - 'rolling-X' : centered rolling mean over X days
			       - 'mean'	     : full time mean
                               - 'instant'   : no time operation
			wave - wave number: if == 0, return total. else passed to GetWavesXr()
		OUPUTS:
			v_bar - zonal mean meridional wind [v]
			t_bar - zonal mean vertical eddy component <v'Theta'/Theta_p> [v*p]
	"""
	#
	# some constants
	# from .constants import kappa
	kappa = 2./7.
	#
	# pressure quantitites
	pp0 = (p0/t[p])**kappa
	# convert to potential temperature
	t = t*pp0 # t = theta
	# zonal means
	v_bar = v.mean(lon)
	t_bar = t.mean(lon) # t_bar = theta_bar
	# prepare pressure derivative
	dthdp = t_bar.differentiate(p,edge_order=2) # dthdp = d(theta_bar)/dp
	dthdp = dthdp.where(dthdp != 0)
	# time mean of d(theta_bar)/dp
	if time in dthdp.dims:
		if 'rolling' in ref:
			r = int(ref.split('-')[-1])
			dthdp = dthdp.rolling(dim={time:r},min_periods=1,center=True).mean()
		elif ref == 'mean':
			dthdp = dthdp.mean(time)
		elif ref == 'instant':
			dthdp = dthdp

	vpTp = (v - v_bar)*(t - t_bar)
	vpTp = vpTp.mean(lon)  # vpTp = bar(v'Th')
	t_bar = vpTp/dthdp # t_bar = bar(v'Th')/(dTh_bar/dp)
	#
	return v_bar,t_bar