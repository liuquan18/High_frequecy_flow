#%%
import xarray as xr
import numpy as np
import pandas as pd
from src.prime.prime_data import read_composite_MPI

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

def stat_stab(theta):
	t = theta # ensemble mean of theta
	t_bar = t.mean('lon') # t_bar = theta_bar
	# prepare pressure derivative
	dthdp = t_bar.differentiate('plev',edge_order=2) # dthdp = d(theta_bar)/dp
	dthdp = dthdp.where(dthdp != 0)

	# time mean
	dthdp_mean = dthdp.mean('time')

	return dthdp_mean	


def eff_stat_stab(p, temp, lambda_val=0.6):
    """
    Calculate the effective static stability derived in O'Gorman, JAS, 2011, pages 75-90.

    Parameters:
    p (numpy.ndarray): 1D vertical profile of pressure
    temp (numpy.ndarray): 1D vertical profile of temperature
    lambda_val (float, optional): Asymmetry parameter (default value 0.6)

    Returns:
    dtheta_dp_eff (numpy.ndarray): Effective static stability
    """
    # Constants
    Rd = 287.04  # gas constant for dry air [J/kg/K]
    Rv = 461.5  # gas constant for water vapor [J/kg/K]
    cpd = 1005.7  # specific heat dry air [J/kg/K]
    cpv = 1870  # specific heat water vapor [J/kg/K]
    g = 9.80665  # gravitational acceleration [m/s^2]
    p0 = 1e5  # reference pressure [Pa]
    kappa = Rd / cpd
    gc_ratio = Rd / Rv

    # Saturation vapor pressure [Pa]
    Tc = temp - 273.15
    es = 611.20 * np.exp(17.67 * Tc / (Tc + 243.5))  # Bolton 1980 equation 10

    # Latent heat of condensation [J/kg]
    L = (2.501 - 0.00237 * Tc) * 1e6  # Bolton 1980 equation 2

    # Saturation mixing ratio
    rs = gc_ratio * es / (p - es)

    # Saturation specific humidity
    qs = rs / (1 + rs)

    # Potential temperature
    exponent = kappa * (1 + rs / gc_ratio) / (1 + rs * cpv / cpd)
    theta = temp * (p0 / p) ** exponent

    # Density
    temp_virtual = temp * (1 + rs / gc_ratio) / (1 + rs)
    rho = p / Rd / temp_virtual

    # Moist adiabatic lapse rate
    malr = g / cpd * (1 + rs) / (1 + cpv / cpd * rs) * \
           (1 + L * rs / Rd / temp) / (1 + L ** 2 * rs * (1 + rs / gc_ratio) / (Rv * temp ** 2 * (cpd + rs * cpv)))

    # Derivative of potential temperature wrt pressure along a moist adiabat
    dtemp_dp_ma = malr / g / rho
    dtheta_dp_ma = dtemp_dp_ma * theta / temp - exponent * theta / p

    # Effective static stability following equation 8 of O'Gorman, JAS, 2011
    dtheta_dp_eff = np.gradient(theta, p) - lambda_val * dtheta_dp_ma

    return dtheta_dp_eff

def eff_stat_stab_xr(T):
	if 'time' in T.dims:
		T = T.mean(dim = 'time')
	T = T.mean(dim = ('lon'))
	stat_stability =  xr.apply_ufunc(
		eff_stat_stab,
		T['plev'],
		T,
		input_core_dims=[['plev'], ['plev']],
		output_core_dims=[['plev']],
		vectorize=True,
		dask='allowed',
	)

	return stat_stability

#%%
def plev_to_isentrope(var, theta, var_name = 'F_phi', theta_name = 'theta', t_bins = np.arange(280, 360, 2)):
	"""
	Interpolate the variable to isentropic levels based on the potential temperature.
	Parameters:
	- var: xarray DataArray of the variable to be interpolated.
	- theta: xarray DataArray of potential temperature.
	Returns:
	- var_isentrope: xarray DataArray of the variable interpolated to isentropic levels.
	"""
	# Interpolate to isentropic levels
	ds = xr.Dataset(
		{
			var_name: var,
			theta_name: theta,
		}
	)
	df = ds.to_dataframe().reset_index()
	# Drop NaN values
	df = df.dropna()

	# interpolate
	isen_df = df.groupby(['lat','lon']).apply(
		bin_var_theta,
		var = var_name,
		t_bins = t_bins
	)

	isen_xr = isen_df.to_xarray()
	
	return isen_xr.transpose('theta', 'lat', 'lon')


def EP_flux(vptp, upvp, dthdp):
	'''
	compute the EP_flux following https://github.com/mjucker/aostools
		vptp = v't' [m/s*K]
		upvp = u'v' [m2/s]
		dthdp = d(theta)/dp [K/Pa]  either from stat_stab() or eff_stat_stab_xr()
	'''
	# check if the 'plev' coordinate is in Pa and convert to hPa
	if 'plev' in vptp.coords and vptp['plev'].max() > 1000:
		vptp = vptp.assign_coords(plev=vptp['plev'] / 100)
	if 'plev' in upvp.coords and upvp['plev'].max() > 1000:
		upvp = upvp.assign_coords(plev=upvp['plev'] / 100)
	if 'plev' in dthdp.coords and dthdp['plev'].max() > 1000:
		dthdp = dthdp.assign_coords(plev=dthdp['plev'] / 100)

	# constants
	a0    = 6371000.  # earth radius in m
	Omega = 7.292e-5 #[1/s]

	# geometry
	coslat = np.cos(np.deg2rad(upvp['lat']))
	sinlat = np.sin(np.deg2rad(upvp['lat']))
	R      = 1./(a0*coslat)
	f      = 2*Omega*sinlat


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
	div = div1 + div2 # divergence

	ep1_cart.name = 'ep1'
	ep2_cart.name = 'ep2'
	div.name = 'div'

	return ep1_cart.transpose('plev','lat','lon'), ep2_cart.transpose('plev','lat','lon'),\
	div.transpose('plev','lat','lon')


# %%
def read_data_all(decade, phase, ano = False, before = '15_5', equiv_theta = False, eddy = 'transient'):
	"""
	theta for interpolation
	steady eddies: usvs
	transient eddies: upvp
	"""
	if eddy == 'transient':
		upvp = read_composite_MPI("upvp", "ua", decade = decade, before = before, return_as=phase, ano=ano, smooth_value=None, remove_zonal=False)
		if equiv_theta:
			vptp = read_composite_MPI("vpetp", "vpetp", decade = decade, before = before, return_as=phase, ano=ano)
			theta_ensmean = xr.open_dataset(
				f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/equiv_theta_monthly_ensmean/equiv_theta_monmean_ensmean_{decade}*.nc").etheta


		else:
			vptp = read_composite_MPI("vptp", "vptp", decade = decade, before = before, return_as=phase, ano=ano)
			theta_ensmean = xr.open_dataset(
				f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/equiv_theta_monthly_ensmean/equiv_theta_monmean_ensmean_{decade}*.nc").theta


	elif eddy == 'steady':
		upvp = read_composite_MPI("usvs", "usvs", decade = decade, before = before, return_as=phase, ano=ano, smooth_value=None, remove_zonal=False)
		if equiv_theta:
			vptp = read_composite_MPI("vsets", "vsets", decade = decade, before = before, return_as=phase, ano=ano)
			theta_ensmean = xr.open_dataset(
				f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/equiv_theta_monthly_ensmean/equiv_theta_monmean_ensmean_{decade}*.nc").etheta

		else:
			vptp = read_composite_MPI("vsts", "vsts", decade = decade, before = before, return_as=phase, ano=ano)
			theta_ensmean = xr.open_dataset(
				f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/equiv_theta_monthly_ensmean/equiv_theta_monmean_ensmean_{decade}*.nc").theta

	else:
		raise ValueError("eddy must be either 'transient' or 'steady'", f"but got {eddy}")


	if 'time' in theta_ensmean.dims:
		theta_ensmean = theta_ensmean.mean(dim = 'time')

	return upvp, vptp, theta_ensmean

def NPC_mean(arr):
    return arr.sel(lon = slice(120, 240)).mean(dim = 'lon')

def NAL_mean(arr):
    return arr.sel(lon = slice(270, 330)).mean(dim = 'lon')

#%%
## helper function: Get actual width and height of axes
def GetAxSize(fig,ax,dpi=False):
	"""get width and height of a given axis.
	   output is in inches if dpi=False, in dpi if dpi=True
	"""
	bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
	width, height = bbox.width, bbox.height
	if dpi:
		width *= fig.dpi
		height *= fig.dpi
	return width, height
#%%
def PlotEPfluxArrows(x,y,ep1,ep2,fig,ax,xlim=None,ylim=None,xscale='linear',yscale='linear',invert_y=True, newax=False, pivot='tail',scale=None,quiv_args=None, draw_key = False, key_loc = (0.6, 0.9)):
	"""Correctly scales the Eliassen-Palm flux vectors for plotting on a latitude-pressure or latitude-height axis.
		x,y,ep1,ep2 assumed to be xarray.DataArrays.

	INPUTS:
		x	: horizontal coordinate, assumed in degrees (latitude) [degrees]
		y	: vertical coordinate, any units, but usually this is pressure or height
		ep1	: horizontal Eliassen-Palm flux component, in [m2/s2]. Typically, this is ep1_cart from
				   ComputeEPfluxDiv()
		ep2	: vertical Eliassen-Palm flux component, in [U.m/s2], where U is the unit of y.
				   Typically, this is ep2_cart from ComputeEPfluxDiv(), in [hPa.m/s2] and y is pressure [hPa].
		fig	: a matplotlib figure object. This figure contains the axes ax.
		ax	: a matplotlib axes object. This is where the arrows will be plotted onto.
		xlim	: axes limits in x-direction. If None, use [min(x),max(x)]. [None]
		ylim	: axes limits in y-direction. If None, use [min(y),max(y)]. [None]
		xscale	: x-axis scaling. currently only 'linear' is supported. ['linear']
		yscale	: y-axis scaling. 'linear' or 'log' ['linear']
		invert_y: invert y-axis (for pressure coordinates). [True]
		newax	: plot on second y-axis. [False]
		pivot	: keyword argument for quiver() ['tail']
		scale	: keyword argument for quiver(). Smaller is longer [None]
				  besides fixing the length, it is also usefull when calling this function inside a
				   script without display as the only way to have a quiverkey on the plot.
               quiv_args: further arguments passed to quiver plot.

	OUTPUTS:
	   Fphi*dx : x-component of properly scaled arrows. Units of [m3.inches]
	   Fp*dy   : y-component of properly scaled arrows. Units of [m3.inches]
	   ax	: secondary y-axis if newax == True
	"""
	import numpy as np
	import matplotlib.pyplot as plt
	#
	def Deltas(z,zlim):
		# if zlim is None:
		return np.max(z)-np.min(z)
		# else:
			# return zlim[1]-zlim[0]
	# Scale EP vector components as in Edmon, Hoskins & McIntyre JAS 1980:
	cosphi = np.cos(np.deg2rad(x))
	a0 = 6376000.0 # Earth radius [m]
	grav = 9.81
	# first scaling: Edmon et al (1980), Eqs. 3.1 & 3.13
	Fphi = 2*np.pi/grav*cosphi**2*a0**2*ep1 # [m3.rad]
	Fp   = 2*np.pi/grav*cosphi**2*a0**3*ep2 # [m3.hPa]
	#
	# Now comes what Edmon et al call "distances occupied by 1 radian of
	#  latitude and 1 [hecto]pascal of pressure on the diagram."
	# These distances depend on figure aspect ratio and axis scale
	#
	# first, get the axis width and height for
	#  correct aspect ratio
	width,height = GetAxSize(fig,ax)
	# we use min(),max(), but note that if the actual axis limits
	#  are different, this will be slightly wrong.
	delta_x = Deltas(x,xlim)
	delta_y = Deltas(y,ylim)
	#
	#scale the x-axis:
	if xscale == 'linear':
		dx = width/delta_x/np.pi*180
	else:
		raise ValueError('ONLY LINEAR X-AXIS IS SUPPORTED AT THE MOMENT')
	#scale the y-axis:
	if invert_y:
		y_sign = -1
	else:
		y_sign = 1
	if yscale == 'linear':
		dy = y_sign*height/delta_y
	elif yscale == 'log':
		dy = y_sign*height/y/np.log(np.max(y)/np.min(y))
	#
	# plot the arrows onto axis
	quivArgs = {'angles':'uv','scale_units':'inches','pivot':pivot}
	if quiv_args is not None:
		for key in quiv_args.keys():
			quivArgs[key] = quiv_args[key]
	if scale is not None:
		quivArgs['scale'] = scale
	if newax:
		ax = ax.twinx()
		ax.set_ylabel('pressure [hPa]')
	try:
		Q = ax.quiver(x,y,Fphi*dx,Fp*dy,**quivArgs)
	except:
		Q = ax.quiver(x,y,dx*Fphi.transpose(),dy*Fp.transpose(),**quivArgs)
	if scale is None:
		fig.canvas.draw() # need to update the plot to get the Q.scale
		U = Q.scale
	else:
		U = scale
	if draw_key: # when running inside a script, the figure might not exist and therefore U is None
		ax.quiverkey(Q, key_loc[0],key_loc[1],U/width,label=r'{0:.1e}$\,m^3$'.format(U),labelpos='E',coordinates='axes')
	if invert_y:
		ax.invert_yaxis()
	if xlim is not None:
		ax.set_xlim(xlim)
	if ylim is not None:
		ax.set_ylim(ylim)
	ax.set_yscale(yscale)
	ax.set_xscale(xscale)
	#
	if newax:
		return Fphi*dx,Fp*dy,ax
	else:
		return Fphi*dx,Fp*dy
#%%
def bin_var_theta(df_all, var="F_phi", t_bins = np.arange(240, 400, 5)):

    var_bined = (
        df_all[[var]]
        .groupby(pd.cut(df_all["etheta"], bins=t_bins), observed=True)
        .mean()
    )
    # add one column called tas_diff, which is the middle value of the bin
    var_bined["theta"] = var_bined.index.map(
        lambda x: x.mid
    )  
    # make the tas_diff as the index
    var_bined = var_bined.set_index("theta")
    return var_bined
