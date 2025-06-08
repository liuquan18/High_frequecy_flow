#%%
import xarray as xr
import numpy as np
import pandas as pd
from src.data_helper.read_composite import read_comp_var
import glob
from metpy.units import units
import metpy.calc as mpcalc
import logging
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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


def EP_flux(vptp, upvp, dthdp):
	'''
	compute the EP_flux following https://github.com/mjucker/aostools
		vptp = v't' [m/s*K]
		upvp = u'v' [m2/s]
		dthdp = d(theta)/dp [K/Pa]  either from stat_stab() or eff_stat_stab_xr()
	'''

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
	

	ep1_cart.name = 'ep1'
	ep2_cart.name = 'ep2'
	div1.name = 'div'
	div1.attrs['units'] = 'm/s/day'
	div1.attrs['long_name'] = 'divergence of Horizonaltal component of Eliassen-Palm flux'

	div2.name = 'div2'
	div2.attrs['units'] = 'm/s/day'
	div2.attrs['long_name'] = 'divergence of Vertical component of Eliassen-Palm flux'

	return ep1_cart.transpose('plev','lat','lon'), ep2_cart.transpose('plev','lat','lon'),\
			div1.transpose('plev','lat','lon'), div2.transpose('plev','lat','lon')



# %%
def read_data_all(decade, phase, equiv_theta = True, time_window = (-10, 5), eddy = 'transient'):
	"""
	theta for interpolation
	steady eddies: usvs
	transient eddies: upvp
	"""
	if eddy == 'transient':
		upvp = read_comp_var(
			var = "upvp",phase = phase, decade = decade, name = "upvp", suffix = "", model_dir = 'MPI_GE_CMIP6_allplev',
			time_window = time_window, method = "mean", erase_zero_line = True,
		)
		
		if equiv_theta:
			vptp = read_comp_var(
				var = "vpetp", phase = phase, decade = decade, name = "vpetp", suffix = "", model_dir = 'MPI_GE_CMIP6_allplev',
				time_window = time_window, method = "mean", erase_zero_line = True,
			)
			

		else:
			vptp = read_comp_var(
				var = "vptp", phase = phase, decade = decade, name = "vptp", suffix = "", model_dir = 'MPI_GE_CMIP6_allplev',
				time_window = time_window, method = "mean", erase_zero_line = True,
			)
		
		# read temperature to compute static stability
		# transient the original 
		ta = read_comp_var(
			var = "ta", phase = phase, decade = decade, name = "ta", suffix = "", model_dir = 'MPI_GE_CMIP6_allplev',
			time_window = time_window, method = "mean", erase_zero_line = True,
		)
	
	elif eddy == 'steady':
		upvp = read_comp_var(
			var = "usvs", phase = phase, decade = decade, name = "usvs", suffix = "", model_dir = 'MPI_GE_CMIP6_allplev',
			time_window = time_window, method = "mean", erase_zero_line = True,
		)
		if equiv_theta:
			vptp = read_comp_var(
				var = "vsets", phase = phase, decade = decade, name = "vsets", suffix = "", model_dir = 'MPI_GE_CMIP6_allplev',
				time_window = time_window, method = "mean", erase_zero_line = True,
			)
			
		
		else:
			vptp = read_comp_var(
				var = "vsts", phase = phase, decade = decade, name = "vsts", suffix = "", model_dir = 'MPI_GE_CMIP6_allplev',
				time_window = time_window, method = "mean", erase_zero_line = True,
			)

		# read temperature to compute static stability
		# ta_hat
		ta = read_comp_var(
			var = "ta_hat", phase = phase, decade = decade, name = "ta", suffix = "", model_dir = 'MPI_GE_CMIP6_allplev',
			time_window = time_window, method = "mean", erase_zero_line = True,
		)

	else:
		raise ValueError("eddy must be either 'transient' or 'steady'", f"but got {eddy}")


	return upvp, vptp, ta


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
		ax.quiverkey(Q, key_loc[0],key_loc[1],U/width,label=r'{0:.1e}'.format(U),labelpos='E',coordinates='axes')
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
def E_div(M2, upvp):

    """
    M2: v'^2 - u'^2 [m^2/s^2]
    upvp: u'v' [m^2/s^2]
    """	
    upvp = -1 * upvp  
    M2 = M2.metpy.assign_crs(
        grid_mapping_name='latitude_longitude',
        earth_radius=6371229.0
    )
    upvp = upvp.metpy.assign_crs(
        grid_mapping_name='latitude_longitude',
        earth_radius=6371229.0
    )
    M2 = M2 * units('m^2/s^2')
    upvp = upvp * units('m^2/s^2')

    # calculate the divergence
    dM2dx, dupvpdy = mpcalc.vector_derivative(
        M2, upvp, return_only=('du/dx', 'dv/dy')
    )

    # convet to xarray DataArray
    dM2dx = xr.DataArray(
        dM2dx,
        coords=M2.coords,
        dims=M2.dims,
        attrs=M2.attrs
    )
    dupvpdy = xr.DataArray(
        dupvpdy,
        coords=upvp.coords,
        dims=upvp.dims,
        attrs=upvp.attrs
    )

    # conver to m/s/day
    dM2dx = dM2dx * 86400  # seconds in a day
    dupvpdy = dupvpdy * 86400  # seconds in a day

    # add attributes
    dM2dx.attrs['units'] = 'm/s/day'
    dupvpdy.attrs['units'] = 'm/s/day'
    dM2dx.attrs['long_name'] = 'x divergence (2M)'
    dupvpdy.attrs['long_name'] = 'y divergence (N)'

    dM2dx = dM2dx.metpy.dequantify()
    dupvpdy = dupvpdy.metpy.dequantify()

	# drop variable 'metpy_crs'
    if 'metpy_crs' in dM2dx.coords:
        dM2dx = dM2dx.drop_vars('metpy_crs')
    if 'metpy_crs' in dupvpdy.coords:
        dupvpdy = dupvpdy.drop_vars('metpy_crs')
    return dM2dx, dupvpdy
