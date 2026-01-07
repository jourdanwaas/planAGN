# -*- coding: utf-8 -*-
"""
AGN natural mass range atmospheric-impact model
\
\
This script computes and plots a set of diagnostics for planetary atmospheres exposed to AGN winds across a span of supermassive black hole (SMBH) masses, radiative efficiencies, and wind speeds.
\
\
Original author: Alessandra Ambrifi
\
Revisions: Jourdan Waas, Jackson Kernan, Emily Lohmann
\
Finalized: March 24, 2025
\
\
Requirements:
- numpy
- matplotlib
"""

## import packages

import numpy as np
import matplotlib.pyplot as plt

## define physical constants and standard conversions

c = 299792458.0                  # speed of light [m s^-1]
G = 6.67e-11                     # gravitational constant [m^3 kg^-1 s^-2]
yr_in_days = 365.256             # sidereal year [days]
yr_in_secs = yr_in_days * 24.0 * 3600.0  # seconds in a sidereal year
pc_to_m = 3.09e16                # parsec to meters
kb = 1.38e-23                    # Boltzmann constant [J K^-1]
mp = 1.67e-27                    # proton mass [kg]
SolarMass = 1.9985e30            # Solar mass in kg
m_Earth = 5.973e24               # Earth mass in kg

## planetary and molecular parameters

Rp = [6371000.0, 69911000.0]          # Earth and Jupiter radii [m]
rho_earth_like = 5.5e3                # Earth density [kg m^-3]
ma_earth = 5.1e18                     # Earth atmospheric mass [kg]
mm_mars_atm = 2.5e16                  # Mars atmospheric mass [kg] (unused currently)
m_h2 = 2.02 * 1.66e-27                # molecular hydrogen mass [kg]
m_wat = 18.01 * 1.66e-27              # water molecule mass [kg]
m_n2 = 28.01 * 1.66e-27               # molecular nitrogen mass [kg]
mpart = [m_n2, m_h2]                  # list used for computing thermal velocities
T0 = 273.15                           # base temperature assumption [K]
Cp = [1320.0, 18300.0, 4444.0]        # specific heats (N2, H2, H2O) [J kg^-1 K^-1]

## plotting colors

colors = ['coral', 'deeppink', 'forestgreen', 'dodgerblue', 'darkblue', 'darkorchid']

## parameter grids

# SMBH mass range (in M_sun)
bhm_grid = np.logspace(6, 10, 100)  # 1e6 -> 1e10 M_sun

# radiative efficiency grid (eta)
Eta = np.linspace(0.01, 0.5, num=10)   # radiative efficiency (dimensionless)

# outflow speed grid (vel)
vel = np.linspace(0.01 * c, 0.1 * c, num=10)  # typical UFO speeds range

## 3D matrix of combinations

def make_parameter_matrix(bhm: np.ndarray, eta: np.ndarray, vels: np.ndarray):
    """return a nested-list structure containing [bhm, eta, vel] triples.
    """
    return [[[[b, e, v] for b in bhm] for e in eta] for v in vels]


data_matrix = make_parameter_matrix(bhm_grid, Eta, vel)


def varselect(j: int, k: int, l: int):
    """select (bhm, eta, vel) triple from the nested data_matrix.

    parameters:
        j (int): mass index
        k (int): eta index
        l (int): vel index

    returns:
        list: [bhm, eta, vel]
    """
    return data_matrix[int(l)][int(k)][int(j)]


def rangecreation(start_mass_idx: int, start_eta_idx: int, vel_idx: int, n_eta_out: int, n_mass_out: int):
    """create a list of parameter triples by iterating in mass and eta indices.
    """
    data_points = []
    for i in range(n_eta_out):
        for x in range(n_mass_out):
            variables = varselect(start_mass_idx + x, start_eta_idx + i, vel_idx)
            data_points.append(variables)
    return data_points

# example stored values
stored_vals = rangecreation(0, 0, 0, 1, 100)

# derived SMBH-dependent quantities
# ---------------------------
M_list = []          # SMBH mass in kg
Ledd_list = []       # Eddington luminosity [W]
r_sch_list = []      # Schwarzschild radius [m]
t_salp_list = []     # Salpeter times [s]
t_salp_yr_list = []  # Salpeter times [yr]
bh_m_plot = []       # BH mass in M_sun for plotting

for n, sv in enumerate(stored_vals):
    bhm = sv[0]                   # BH mass in solar masses (M_sun)
    eta = sv[1]                   # radiative efficiency (dimensionless)
    # Eddington luminosity: L_Edd ≈ 1.26e31 W per M_sun
    Ledd = bhm * 1.26e31
    Ledd_list.append(Ledd)

    M_kg = bhm * SolarMass
    M_list.append(M_kg)

    r_sch = 2.0 * G * M_kg / c**2  # Schwarzschild radius
    r_sch_list.append(r_sch)

    # Salpeter timescale, Equation 2 (Waas et al. 2025)
    t_salp = (M_kg * eta * c**2) / ((1.0 - eta) * Ledd)
    t_salp_list.append(t_salp)
    t_salp_yr_list.append(t_salp / yr_in_secs)

    bh_m_plot.append(bhm)

# numpy array versions of previous lists (for "vectorized" computations)

M_arr = np.array(M_list)                    # SMBH mass in kg
Ledd_arr = np.array(Ledd_list)              # Eddington luminosity [W]
r_sch_arr = np.array(r_sch_list)            # Schwarzschild radius [m]
t_salp_arr = np.array(t_salp_list)          # Salpeter times [s]
t_salp_yr_arr = np.array(t_salp_yr_list)    # Salpeter times [yr]

# ---------------------------
# typical UFOs and warm absorbers speeds
# ---------------------------
v_out = [1e5, 1e6]  # typical speeds [km s^-1] (Z. Igo et al. 2020)

# ---------------------------
# Ozone-depletion calculation (per Salpeter time)
# ---------------------------
# define coefficients of the quadratic
a = 1.0
b = 10.0

R0 = 9e14 # rate at which the ambient flux of cosmic rays (CRs) generates NO [molecules cm^-2 yr^-1] (Ambrifi et al. 2022)
phi0 = 9e4 # energy flux carried by backround CRs [erg cm^-2 yr^-1] (Ambrifi et al. 2022)
y0 = 3.0 # unperturbed stratospheric NO abundances [ppb] (Ambrifi et al. 2022)
sigmastrat = 5e23 # stratospheric column density [molecules cm^-2] (Ambrifi et al. 2022)

def Oz_dep(x_pc: float, outflow_type_index: int) -> np.ndarray:
    """
    ozone depletion fraction after one Salpeter time, as function of SMBH mass.

    parameters:
        x_pc (float): distance from SMBH in parsecs
        outflow_type_index (int): 0 => energy-driven (0.05 Ledd),
                                  1 => momentum-driven (0.001 Ledd)

    returns:
        y (np.ndarray): ozone depletion fraction array (same length as stored_vals)
    """
 # assign power fraction depending on outflow type
    if outflow_type_index == 0:
        power_frac = 0.05 #energy-driven case (equation 4, Waas et al. 2025)
    else:
        power_frac = 0.001 #momentum-driven case (equation 5, Waas et al. 2025)

    # x is passed in parsecs; convert to meters where necessary

    power = power_frac * Ledd_arr

    # energy flux attributed to AGN wind particles [erg cm^-2 yr^-1] (equation 30, Ambrifi et al. 2022)
    # the extra numerical factors are converting x_pc to cm and the (1e7 / 3.17e-8) converts to erg/yr
    flux = power / (16.0 * np.pi * (x_pc * 3.086e18)**2) * (1e7 / (3.17e-8))

    # cdisc is the constant term (c in quadratic formula) given by equation 27, Ambrifi et al. 2022)
    cdisc = - (R0 * flux / phi0) * ((10 + y0) * t_salp_yr_arr * 1e9 / sigmastrat)

    n = len(stored_vals)
    y1 = np.zeros(n)
    for w in range(n):
        # solve discriminant using the quadratic formula
        disc = b**2 - (4 * a * cdisc[w])
        # Numerical safeguard: ensure discriminant non-negative (set negative to 0)
        if disc < 0:
            disc = 0.0
        y1[w] = (-b + np.sqrt(disc)) / (2 * a)

    # ratio of perturbed and unperturbed NO abundances (equation 29, Ambrifi et al. 2022)
    d_x = (y0 + y1) / y0

    # ratio of stratospheric ozone abundance (equation 28, Ambrifi et al. 2022)
    F_d = (np.sqrt(16 + 9 * d_x**2) - 3 * d_x) / 2

    # fractional ozone depletion (D) (equation 23, Waas et al. 2025)
    y = 1 - F_d

    return y

# ---------------------------
# time required for 90% ozone depletion
# ---------------------------

k = (R0 / phi0) * (((1e9) * (10.0 + y0)) / sigmastrat) #defined as the constant in equation 17, Waas et al. 2025


def deltaT(x_pc: float, outflow_type_index: int) -> np.ndarray:
    """
    time (years) required for 90% ozone depletion, as a function of BH mass.
    """
    power_scale = 0.05 if outflow_type_index == 0 else 0.001
    power = power_scale * Ledd_arr
    flux = power / (16 * np.pi * (x_pc * 3.086e18)**2) * (1e7 / (3.17e-8))

    # generalized time interval for D = 0.9 or 90% ozone depletion [yr] (equation 25, Waas et al. 2025)
    time_dep = 1739 / (k * flux)

    return time_dep

# ---------------------------
# heating: atmospheric temperature increase after Salpeter time
# ---------------------------
def Tnew(x_pc: float, composition_index: int, kinpow_index: int) -> np.ndarray:
    """
    compute Delta T (K) added to the atmosphere by deposited kinetic power
    over a Salpeter time.

    parameters:
        x_pc: distance in parsec
        composition_index: 0 -> N2, 1 -> H2, 2 -> H2O
        kinpow_index: 0 -> 5% Ledd (energy-driven), 1 -> 0.1% Ledd (momentum)

    returns:
        y: array of Delta T [K] for each SMBH mass in stored_vals
    """
    # fraction of Ledd converted to wind kinetic power
    if kinpow_index == 0:
        kinpow = 0.05
    elif kinpow_index == 1:
        kinpow = 0.001

    specific_heat = Cp[composition_index]

    # upper bound of atmospheric temperature increase [K] (equation 16, Ambrifi et al. 2022)
    y = ((1 / (4 * ma_earth * specific_heat)) *
        (kinpow * Ledd_arr * t_salp_arr) *
        (Rp[0] / (x_pc * pc_to_m))**2)
    return y

# ---------------------------
# most probable velocity (thermal) after heating
# ---------------------------
def Vmp(x_pc: float, composition_index: int, kinpow_index: int) -> np.ndarray:
    """
    Most probable molecular speed after atmosphere is heated by Delta T.
    Returns speeds in m/s (same units as sqrt).
    """
    m = mpart[composition_index]

    deltaT_vals = Tnew(x_pc, composition_index, kinpow_index)

    y = np.sqrt(2 * kb * (T0 + deltaT_vals) / m) # [m s^-1] (equation 17, Ambrifi et al. 2022)
    return y

# escape velocity for "Earth-like" surface used for plotting
v_esc = 11.2 * np.ones_like(bh_m_plot) # 11.2 km/s

# ---------------------------
# mass loss computations (energy and momentum driven)
# ---------------------------
def mass_lost_energy(x_pc: float) -> np.ndarray:
    """
    mass lost from an atmosphere due to energy-driven outflow interaction.
    """

    # atmospheric mass loss [kg] with power replaced by energy-driven power equation (equation 20, Ambrifi et al. 2022)
    M_lostE = ((3 / (16 * np.pi * G * rho_earth_like)) *
        (0.05 * Ledd_arr * t_salp_arr / (x_pc * pc_to_m)**2))
    return M_lostE


def mass_lost_momentum(x_pc: float) -> np.ndarray:
    """
    mass lost from an atmosphere due to momentum-driven outflow.
    """
    # atmospheric mass loss [kg] with power replaced by momentum-driven power equation (equation 20, Ambrifi et al. 2022)

    M_lostM = ((3 / (8 * np.pi * G * rho_earth_like)) *
        (0.001 * Ledd_arr * t_salp_arr / (x_pc * pc_to_m)**2))
    return M_lostM

# plot ozone depletion

def plot_ozone_depletion():
    x_list = [100., 800., 5000., 10000., 15000.]
    # energy-driven (index 0)
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, x_pc in enumerate(x_list):
        plt.plot(bh_m_plot, Oz_dep(x_pc, 0) * 100.0, colors[i], linestyle='-',
                 label=f'R:{x_pc/100:.0f} kpc')
    plt.xlabel(r'Black Hole Mass [$M_{\odot}$]', fontsize=14)
    plt.ylabel('Ozone depletion D [%]', fontsize=14)
    plt.xscale('log')
    plt.legend(title='Energy-Driven', prop={'size': 10})
    plt.tight_layout()
    fig.savefig('plots/ozone depl ed.png')

    # momentum-driven (index 1)
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, x_pc in enumerate(x_list):
        plt.plot(bh_m_plot, Oz_dep(x_pc, 1) * 100.0, colors[i], linestyle='-',
                 label=f'R:{x_pc/100:.0f} kpc')
    plt.xlabel(r'Black Hole Mass [$M_{\odot}$]', fontsize=14)
    plt.ylabel('Ozone depletion D [%]', fontsize=14)
    plt.xscale('log')
    plt.legend(title='Momentum-Driven', prop={'size': 10})
    plt.tight_layout()
    fig.savefig('plots/ozone depl md.png')

# plot timescale for 90% depletion

def plot_deltaT_90pct():
    x_list = [100., 800., 5000., 10000., 15000.]
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, x_pc in enumerate(x_list):
        plt.plot(bh_m_plot, deltaT(x_pc, 0), colors[i], linestyle='-', label=f'R:{x_pc/100:.0f} kpc')
    plt.xlabel(r'Black Hole Mass [$M_{\odot}$]', fontsize=14)
    plt.ylabel(r'$\Delta t$ [yr]', fontsize=14)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(title='Energy-Driven', prop={'size': 10})
    plt.tight_layout()
    fig.savefig('plots/timescale ed.png')

    fig, ax = plt.subplots(figsize=(7, 5))
    for i, x_pc in enumerate(x_list):
        plt.plot(bh_m_plot, deltaT(x_pc, 1), colors[i], linestyle='-', label=f'R:{x_pc/100:.0f} kpc')
    plt.xlabel(r'Black Hole Mass [$M_{\odot}$]', fontsize=14)
    plt.ylabel(r'$\Delta t$ [yr]', fontsize=14)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(title='Momentum-Driven', prop={'size': 10})
    plt.tight_layout()
    fig.savefig('plots/timescale md.png')

# plot heating and most probable velocities

def plot_heating_and_velocities():
    x_list = [100., 800., 5000., 10000., 15000.]
    # energy-driven heating
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, x_pc in enumerate(x_list):
        plt.plot(bh_m_plot, Tnew(x_pc, 0, 0), colors[i], linestyle='-', label=f'R:{x_pc/100:.0f} kpc - $N_2$')
        plt.plot(bh_m_plot, Tnew(x_pc, 1, 0), colors[i], linewidth=1.7, linestyle='--',
                 label=f'R:{x_pc/100:.0f} kpc - $H_2$')
    plt.xlabel(r'Black Hole Mass [$M_{\odot}$]', fontsize=14)
    plt.ylabel(r'$\Delta T$ [K]', fontsize=14)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(title='Energy-Driven', prop={'size': 9})
    plt.tight_layout()
    fig.savefig('plots/heating ed.png')

    # momentum-driven heating
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, x_pc in enumerate(x_list):
        plt.plot(bh_m_plot, Tnew(x_pc, 0, 1), colors[i], linestyle='-', label=f'R:{x_pc/100:.0f} kpc - $N_2$')
        plt.plot(bh_m_plot, Tnew(x_pc, 1, 1), colors[i], linewidth=1.7, linestyle='--',
                 label=f'R:{x_pc/100:.0f} kpc - $H_2$')
    plt.xlabel(r'Black Hole Mass [$M_{\odot}$]', fontsize=14)
    plt.ylabel(r'$\Delta T$ [K]', fontsize=14)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(title='Momentum-Driven', prop={'size': 9})
    plt.tight_layout()
    fig.savefig('plots/heating md.png')

    # energy-driven most probable velocities
    fig, ax = plt.subplots(figsize=(7, 5))
    # plot escape velocity (converted to km/s)
    plt.plot(bh_m_plot, v_esc, 'firebrick', linestyle=':', linewidth=3, alpha=0.9,
             label=r'$v_{\text{esc}} = 11.2~\mathrm{km\,s^{-1}}$')
    for i, x_pc in enumerate(x_list):
        plt.plot(bh_m_plot, Vmp(x_pc, 0, 0) / 1000.0, colors[i], linestyle='-', label=f'R:{x_pc/100:.0f} kpc - $N_2$')
        plt.plot(bh_m_plot, Vmp(x_pc, 1, 0) / 1000.0, colors[i], linewidth=1.7, linestyle='--',
                 label=f'R:{x_pc/100:.0f} kpc - $H_2$')
    plt.xlabel(r'Black Hole Mass [$M_{\odot}$]', fontsize=14)
    plt.ylabel(r'$v_{\mathrm{mp}}$ [km s$^{-1}$]', fontsize=14)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(title='Energy-Driven', prop={'size': 9})
    plt.tight_layout()
    fig.savefig('plots/prob vel ed.png')

    # momentum-driven most probable velocities
    fig, ax = plt.subplots(figsize=(7, 5))
    # plot escape velocity (converted to km/s)
    plt.plot(bh_m_plot, v_esc, 'firebrick', linestyle=':', linewidth=3, alpha=0.9,
         label=r'$v_{\text{esc}} = 11.2~\mathrm{km\,s^{-1}}$')

    for i, x_pc in enumerate(x_list):
        plt.plot(bh_m_plot, Vmp(x_pc, 0, 1) / 1000.0, colors[i], linestyle='-',
                 label=f'R:{x_pc/100:.0f} kpc - $N_2$')
        plt.plot(bh_m_plot, Vmp(x_pc, 1, 1) / 1000.0, colors[i], linewidth=1.7, linestyle='--',
                 label=f'R:{x_pc/100:.0f} kpc - $H_2$')

    plt.xlabel(r'Black Hole Mass [$M_{\odot}$]', fontsize=14)
    plt.ylabel(r'$v_{\mathrm{mp}}$ [km s$^{-1}$]', fontsize=14)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(title='Momentum-Driven', prop={'size': 9})
    plt.tight_layout()
    fig.savefig('plots/prob vel md.png')

# plot mass loss

def plot_mass_loss():
    x_list = [100., 800., 5000., 10000., 15000.]
    fig, ax = plt.subplots(figsize=(7, 5))
    for n, x_pc in enumerate(x_list):
        plt.plot(bh_m_plot, mass_lost_energy(x_pc) / ma_earth, colors[n], linewidth=1.7,
                 linestyle='-', label=f'R:{x_pc/100:.0f} kpc')
    plt.xlabel(r'Black Hole Mass [$M_{\odot}$]', fontsize=14)
    plt.ylabel(r'$M_{\mathrm{lost}}/M_{\mathrm{atm,\oplus}}$', fontsize=14)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(title='Energy-Driven', prop={'size': 9})
    plt.tight_layout()
    fig.savefig('plots/mass loss ed.png')

    fig, ax = plt.subplots(figsize=(7, 5))
    for n, x_pc in enumerate(x_list):
        plt.plot(bh_m_plot, mass_lost_momentum(x_pc) / ma_earth, colors[n], linewidth=1.7,
                 linestyle='-', label=f'R:{x_pc/100:.0f} kpc')
    plt.xlabel(r'Black Hole Mass [$M_{\odot}$]', fontsize=14)
    plt.ylabel(r'$M_{\mathrm{lost}}/M_{\mathrm{atm,\oplus}}$', fontsize=14)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(title='Momentum-Driven', prop={'size': 9})
    plt.tight_layout()
    fig.savefig('plots/mass loss md.png')

# ---------------------------
# convenience main
# ---------------------------
def main():
    """run all plotting functions"""
    plot_ozone_depletion()
    plot_deltaT_90pct()
    plot_heating_and_velocities()
    plot_mass_loss()


if __name__ == "__main__":
    main()



