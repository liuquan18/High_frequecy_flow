
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

def EP_flux(vptp, upvp, Th_bar):
	'''
	compute the EP_flux following https://github.com/mjucker/aostools
		vptp = v't' [m/s*K]
		upvp = u'v' [m2/s]
		Th_bar = theta_bar [K] ensemble mean of theta
	'''
	a0    = 6371000.  # earth radius in m
	Omega = 7.292e-5 #[1/s]

	# geometry
	coslat = np.cos(np.deg2rad(upvp['lat']))
	sinlat = np.sin(np.deg2rad(upvp['lat']))
	R      = 1./(a0*coslat)
	f      = 2*Omega*sinlat

	dthdp = Theta_P(Th_bar)

	# absolute vorticity
	fhat = f

	# v't'/theta_p
	vertEddy = vptp / dthdp

	# horizontal component
	ep1_cart = -upvp

	# compute vertical component
	ep2_cart = fhat*vertEddy # [1/s*m.hPa/s] = [m.hPa/s2]

	# div1 = 1/(a.cosphi)*d/dphi[a*cosphi*ep1_cart*cosphi]
	# where a*cosphi comes from using cartesian, and cosphi from the derivative
	# With some algebra, we get
	#  div1 = cosphi d/d phi[ep1_cart] - 2 sinphi*ep1_cart
	div1 = coslat*(np.rad2deg(ep1_cart).differentiate('lat',edge_order=2)) \
			- 2*sinlat*ep1_cart
	# Now, we want acceleration, which is div(F)/a.cosphi [m/s2]
	div1 = R*div1 # [m/s2]
	#
	# Similarly, we want acceleration = 1/a.coshpi*a.cosphi*d/dp[ep2_cart] [m/s2]
	div2 = ep2_cart.differentiate('plev',edge_order=2) # [m/s2]
	#
	# convert to m/s/day
	div1 = div1*86400
	div2 = div2*86400

	ep1_cart.name = 'ep1'
	ep2_cart.name = 'ep2'
	div1.name = 'div1'
	div2.name = 'div2'

	return ep1_cart, ep2_cart, div1, div2