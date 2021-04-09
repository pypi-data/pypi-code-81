"""
Cratering functions for planetary science
"""

# Load Python dependencies
import numpy as np

#############
# Constants #
#############

# Pi
pi = np.pi

################
# craterVolume #
################
def craterVolume(D, beta):
    """Volume of a crater with diameter D and depth/diameter ratio beta.
    
    **The crater is assumed to be a spherical section**
    (i.e., 'spherical cap') with radius D/2
    """
    V = pi * beta * D**3/6 * (3/4 + beta**2)
    
    return V

###################
# ejectaThickness #
###################
def ejectaThickness(D, beta, r, B=3):
    """
    Ejecta thickness at given distance from the center of a crater.
    Assumes power-law decay of thickness vs. distance, 
    h(r) = h(D/2)*(2r/D)**-B
    with the crater excavation volume that of a spherical cap.
    [cf. Melosh (1989), Impact Cratering: A Geologic Process, p. 90]
    
    Parameters
    ----------
    D : float
        Crater diameter [meters]
    beta : float
        Crater depth/diameter ratio
    r : np.array(float)
        Distance from center of crater [meters]
    B : float
        Power-law exponent in 
    
    Returns
    -------
    np.array(float)
        Ejecta thickness [meters]
    """
    R = D/2 # Crater radius
    h0 = (2/3) * R *(B-2)*beta*(3/4 - beta**2) # h(r/R), i.e. at rim
    h = np.array(h0 * (r/R)**-B)
    h[np.abs(r)<R] = 0 # thickness inside crater is zero
    
    return h

###########################
# transientCraterDiameter #
###########################
def transientCraterDiameter(Dp, vp, thetap, rhop, rhot, g, target='rock'):
    """
    Transient crater diameter for given projectile and target properties.
    Scaling law from Collins et al. (2005), Meteor. Planet. Sci. 40, #6, 817--840
    Assumes simple craters.
    Note: all quantities are in SI units.
    
    Parameters
    ----------
    Dp : float
        Projectile diameter [m]
    vp : float
        Impact velocity [m.s-1]
    thetap : float
        Impact angle [rad]
        Measured from horizontal
    rhop : float
        Projectile density [kg.m-3]
    rhot : float
        Target density [kg.m-3]
    g : float
        Surface gravity [m.s-2]
    target : string
        Target material type, either 'rock' or 'ice'
        
    Returns
    -------
    float
        Diameter of the transient crater [m]
    """
    if target=='rock' or target=='granite' or target=='dunite' \
            or target=='iron' or target=='aluminum':
        C = 1.61
    elif target=='ice':
        C = 1.365
    else:
        raise Exception('Invalid material type. Allowed types are: \
                        granite, dunite, iron, aluminum, ice, rock.')
    
    Dtc = C * (rhop/rhot)**(1/3) * Dp**0.78 * vp**0.44 * g**-0.22 * np.sin(thetap)
    
    return Dtc

#######################
# finalCraterDiameter #
#######################
def finalCraterDiameter(Dp, vp, thetap, rhop, rhot, g, target='rock'):
    """
    Final crater diameter for given projectile and target properties
    Scaling law from Collins et al. (2005), Meteor. Planet. Sci. 40, #6, 817--840
    Assumes simple craters.
    Note: all quantities are in SI units.
    
    Parameters
    ----------
    Dp : float
        Projectile diameter [m]
    vp : float
        Impact velocity [m.s-1]
    thetap : float
        Impact angle [rad]
        Measured from horizontal
    rhop : float
        Projectile density [kg.m-3]
    rhot : float
        Target density [kg.m-3]
    g : float
        Surface gravity [m.s-2]
    target : string
        Target material type, either 'rock' or 'ice'
        
    Returns
    -------
    float
        Diameter of the final crater [m]
    """
    A = 1.25 # Pre-factor from Collins et al. (2005)
    Dfr = A * transientCraterDiameter(Dp, vp, thetap, rhop, rhot, 
                                      g, target=target)
    return Dfr

######################
# projectileDiameter #
######################
def projectileDiameter(Dc, vp, thetap, rhop, rhot, g, target='rock'):
    """
    Estimate projectile diameter based on measured final crater diameter.
    Scaling law from Collins et al. (2005), Meteor. Planet. Sci. 40, #6, 817--840
    Assumes simple craters.
    Note: all quantities are in SI units.
    
    Parameters
    ----------
    Dc : float
        Final crater diameter [m]
    vp : float
        Impact velocity [m.s-1]
    thetap : float
        Impact angle [rad]
        Measured from horizontal
    rhop : float
        Projectile density [kg.m-3]
    rhot : float
        Target density [kg.m-3]
    g : float
        Surface gravity [m.s-2]
    target : string
        Target material type, either 'rock' or 'ice'
        
    Returns
    -------
    float
        Diameter of the projectile [m]
    """
    dD = Dc/1e3 # precision of diameter estimate [m]
    D_min = Dc/100 # minimum projectile diameter to try [m]
    D_max = Dc # maximum projectile diameter to try [m]
    Dp_arr = np.arange(D_min, D_max, dD) # possible values [m]
    
    # Create array of crater diameters
    Dc_arr = finalCraterDiameter(Dp_arr, vp, thetap, rhop, rhot, g, target=target)
    
    # Interpolate to find best value for projectile diameter
    Dp = np.interp(Dc, Dc_arr, Dp_arr)
    
    return Dp

####################
# impactMeltVolume #
####################
def impactMeltVolume(Dp, vp, thetap, target='granite'):
    """
    Volume of impact melt produced based on projectile energy and 
    target properties.
    See: Collins et al. (2005), Meteor. Planet. Sci. 40, #6, 817--840
    and: Pierazzo et al. (1997), Icarus, 127, 408–423
    Note: all quantities are SI units
    
    Parameters
    ----------
    Dp : float
        Projectile diameter [m]
    vp : float
        Impact velocity [m.s-1]
    thetap : float
        Impact angle [rad]
        Measured from horizontal
    target : string
        Target material type can be 'granite', 'dunite', 'iron', 'aluminum', 'ice'
        Used to determine specific energy based on EOS (see Pierazzo et al.)
        
    Returns
    -------
    float
        Impact melt volume [m3]
    """
    # Error checking
    if thetap<0 or thetap>(np.pi/2):
        raise Exception('Invalid impact angle; valid range 0 to pi [radians].')
    vmin = 1.2e4 # minimum impact velocity to produce melt (Melosh, 2012)
    if vp<vmin:
        print('No melt produced, v < {:.2g} m/s'.format(vmin))
        return 0.0
    
    # Target type
    if target=='granite' or target=='rock':
        Emelt = 5.2e6
    elif target=='dunite':
        Emelt = 9.0e6
    elif target=='iron':
        Emelt = 1.0e6
    elif target=='aluminum':
        Emelt = 7.2e6
    elif target=='ice':
        Emelt = 0.8e6
    else:
        raise Exception('Invalid material type. Allowed types are: \
                        granite, dunite, iron, aluminum, ice, rock.')
    
    Vp = (4/3)*np.pi*(Dp/2)**3 # projectile volume
    Vmelt = 0.25 * vp**2 * Vp / Emelt * np.sin(thetap)
    
    return Vmelt