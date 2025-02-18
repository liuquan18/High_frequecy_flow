function dtemp_dp_ma = calc_malr(p, temp)

% calculates the moist adiabatic lapse rate 
%
% inputs are 1d vertical profiles of pressure and temperature :
% p       pressure (Pa)
% temp    temperature (K)

 % constants
 Rd       = 287.04;      % gas constant for dry air [J/kg/K]
 Rv       = 461.5;       % gas constant for water vapor [J/kg/K]
 cpd      = 1005.7;      % specific heat dry air [J/kg/K]
 cpv      = 1870;        % specific heat water vapor [J/kg/K]
 g        = 9.80665;     % gravitational acceleration [m/s^2]
 p0       = 1e5;         % reference pressure [Pa]
 kappa    = Rd/cpd;
 gc_ratio = Rd/Rv;

 % saturation vapor pressure [Pa]
 Tc = temp-273.15;
 es = 611.20*exp(17.67*Tc./(Tc+243.5)); % Bolton 1980 equation 10

 % latent heat of condensation [J/kg]
 L = (2.501-0.00237*Tc)*1e6; % Bolton 1980 equation 2

 % saturation mixing ratio
 rs = gc_ratio*es./(p-es);

 % density
 temp_virtual = temp.*(1.0+rs/gc_ratio)./(1.0+rs);
 rho          = p/Rd./temp_virtual;
% rho          = p/Rd./temp;

 % moist adiabatic lapse rate
 malr = g/cpd*(1+rs)./(1+cpv/cpd.*rs) ...
        .*(1+L.*rs./Rd./temp)...
        ./(1+L.^2.*rs.*(1+rs/gc_ratio)./(Rv.*temp.^2.*(cpd+rs*cpv)));

 % derivative of potential temperature wrt pressure along a moist adiabat
 % (neglects small contribution from vertical variations of exponent)
 dtemp_dp_ma  = malr/g./rho;

end