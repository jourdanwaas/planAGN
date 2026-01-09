# -*- coding: utf-8 -*-
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

## user inputs

name = "3C 390.3"  #name of the object
M_bh = 2.8e8       #mass ob object in solar masses
save_plots = True

# compute mantissa and exponent for title formatting
mantissa, exponent = f"{M_bh:.1e}".split("e")
mantissa = float(mantissa)
exponent = int(exponent)

## define path to plots directory

plot_dir = Path(__file__).parent.parent.resolve() / 'reports' / 'figures'

## create a subfolder for object

object_dir = plot_dir / name.replace(" ", "_")

## check to make sure it exists

object_dir.mkdir(parents=True, exist_ok=True)

# create a .gitignore in that folder
gitignore_file = object_dir / ".gitignore"
if not gitignore_file.exists():
    gitignore_file.write_text("*\n!.gitignore\n")  # ignore all files except .gitignore itself

## define path to results directory

result_dir = Path(__file__).parent.parent.resolve() / 'reports' / 'results'

## create subfolder for results

output_dir = result_dir / name.replace(" ", "_")

## make sure it exists

output_dir.mkdir(parents=True, exist_ok=True)

# create a .gitignore in that folder
gitignore_file = output_dir / ".gitignore"
if not gitignore_file.exists():
    gitignore_file.write_text("*\n!.gitignore\n")  # ignore all files except .gitignore itself

## create full path for output file

output_file = output_dir / f"results__{name.replace(' ', '_')}.txt"

## formatting for the output file for all printed results
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"Galaxy: {name}\n")
    f.write("Black hole mass: " + f"{mantissa:.1f} × 10^{exponent} M_sun\n")
    f.write("="*50 + "\n\n")

## constants

c = 299792458.                     #m/s
G = 6.67*10**(-11.)                #International System of Units (SI)
yr_in_days = 365.256               #sidereal year
yr_in_secs = yr_in_days * 24. * 60. * 60. #sidereal year in seconds
r_pc = 3.09*10**(16.)              #pc to meter conversion
kb = 1.38 * 10.**(-23.)            #Boltzmann constant (SI)
mp = 1.67 * 10.**(-27.)            #Proton mass (kg)
m_Earth=5.973*10**24.              #Earth mass (kg)
SolarMass = 1.9985*10.**30.        # (SI)
SolarLum = 3.828*10.**26           # in watts
R_kpc = np.arange(0.1,150)          #distance to bh in kpc where the radius is a range
R_cm = np.array(R_kpc)*(3.1*10**21)  #kpc to cm

## BH data

M = M_bh * SolarMass          #mass of BH in kg
Ledd = 3.3e4 * M_bh * SolarLum   #BH Eddington Luminosity (SI)
eta = 0.1                          #radiative efficiency (adimensional)
r_sch=2.*G*M/c**2.                 #Schwarzschild Radius (SI)
t_salp = (M*eta*c**2.) / ((1.-eta)*Ledd)  #Salpeter time (SI)
t_salp_yr = t_salp / yr_in_secs           #Salpeter time (in years)

#Typical values of UFOs and Warm Absorbers' velocities, Tombesi et al. 2013

v = 0.1*c                          #UFOs speed (SI)
v_out=[10.**5,10.**6.]             #WAs speed (SI)

#Planetary and atmospheric parameters

Rp = [6371000. , 69911000.]        #Earth and Jup. radii (SI)
rho=5.5*10.**3.                    #Earth density (SI)
vfug=np.sqrt(2.*G*m_Earth/Rp[0])   #Escape velocity from the Earth (SI)
ma = 5.1*10.**18.                  #Earth atmospheric mass (SI)
mm = 2.5*10.**16.                  #Mars atmospheric mass  (SI)
m_h2 = 2.02 *1.66*10.**(-27)       #molecular hydrogen mass (SI)
m_wat = 18.01 *1.66*10.**(-27)     #water molecule mass (SI)
m_o2 = 5.31 * 10**(-26.)           #molecular oxygen mass (SI)
m_n2=28.01 * 1.66*10.**(-27)       #molecular nitrogen mass (SI)
mpart=[m_n2, m_h2 ]                #list of molecular masses
T0 = 273.15                        #assumed initial temperature for planetary atmosphere (SI)
Cp=[1320,18300,4444]               #specific heat at constant pressure for nitrogen, hydrogen, water ( J/ (kg K) )

## heating and most probable velocity

r0 = 100.                          #Minimum distance we consider from the central SMBH (pc)
r1 = 100000.                        #Maximum distance we consider from the central SMBH (pc)
x=np.arange(r0,r1,10.)
kinpow=[0.05 , 0.001]              #fractions of the AGN luminosity to be converted into wind's kinetic power

def Tnew(x,k,j):                   #New atmospheric temperature, depending on the distance from the SMBH (x),
                                   # atmospheric composition (k=0 : nitrogen ; k=1 : hydrogen ; k=2 : water),
                                   # and outflow's kinetic power (j=0 : kinetic power = 5%Ledd ; j=1 : kinetic power = 0.1%Ledd).
    #y=np.zeros((len(x)))
    #for w in range(0,len(x)):
        #y[w]=  (1./(4.*ma*Cp[k]))*(kinpow[j]*Ledd*t_salp)*(Rp[0]/(x[w]*r_pc))**2.
    y = (1./(4.*ma*Cp[k]))*(kinpow[j]*Ledd*t_salp)*(Rp[0]/(x*r_pc))**2.
    return y

fig = plt.figure(facecolor='white', figsize=(7,5))
plt.plot(x/1000.,Tnew(x,0,0) ,'magenta', linestyle='-',  label=r"ed $N_2$")                      #energy driven outflow, atmospheric composition: nitrogen
plt.plot(x/1000.,Tnew(x,1,0) , 'darkorchid', linewidth=1.7, linestyle='--',  label=r"ed $H_2$")  #energy driven outflow, atmospheric composition: hydrogen
plt.plot(x/1000.,Tnew(x,0,1) ,'dodgerblue', linestyle='-',  label=r"md $N_2$")                   #momentum driven outflow, atmospheric composition: nitrogen
plt.plot(x/1000.,Tnew(x,1,1) ,'darkblue', linewidth=1.7, linestyle='--',  label=r"md $H_2$")     #momentum driven outflow, atmospheric composition: hydrogen
plt.xlabel('R [kpc] ', fontsize=20, color='k')
plt.ylabel(r'$\Delta$T [K] ', fontsize=20, color='k')
plt.xscale('log')
plt.yscale('log')
plt.ylim(10**-1, 10**10)
plt.yticks(fontsize=16)
plt.xticks(fontsize=16)
plt.tight_layout()
plt.legend(prop={'size': 12})
plt.title(
    f"{name} " + r"$(%.1f \times 10^{%d}~M_\odot)$" % (mantissa, exponent),
    fontsize=20,
    fontweight='bold')

# define filename and full save path
filename = f"heating__{name.replace(' ', '_')}.png"
save_path = object_dir / filename

if save_plots:
    fig.savefig(save_path, bbox_inches='tight')

#plt.show()

def Vmp(x,k,j):                  # Most probable particles' speed, depending on the amount of heat
                                 # which entered the atmosphere, hence depending on distance from
                                 # the SMBH (x), atmospheric composition (k) and kinetic power (j).
    #y=np.zeros((len(x)))
    #for w in range(0,len(x)):
        #y[w]= np.sqrt((2*kb*(T0+Tnew(x,k,j)[w])) /mpart[k])
    y = np.sqrt((2*kb*(T0+Tnew(x,k,j))) /mpart[k])
    return y

fig = plt.figure(facecolor='white', figsize=(7,5))
plt.plot(x/1000.,Vmp(x,0,0)/1000.,'magenta', linestyle='-',  label=r"ed $N_2$")                    #energy driven outflow, atmospheric composition: nitrogen
plt.plot(x/1000.,Vmp(x,1,0)/1000.,'darkorchid', linewidth=1.7, linestyle='--',  label=r"ed $H_2$") #energy driven outflow, atmospheric composition: hydrogen
plt.plot(x/1000.,Vmp(x,0,1)/1000.,'dodgerblue', linestyle='-',  label=r"md $N_2$" )                #momentum driven outflow, atmospheric composition: nitrogen
plt.plot(x/1000.,Vmp(x,1,1)/1000.,'darkblue', linewidth=1.7, linestyle='--',  label=r"md $H_2$")   #momentum driven outflow, atmospheric composition: hydrogen
plt.plot(x/1000., (11.2)*x**0., color='firebrick', linestyle=':', linewidth=3, alpha=0.9,
         label=r'$v_{\mathrm{esc}} = 11.2~\mathrm{km\,s^{-1}}$')

plt.xlabel('R [kpc] ', fontsize=20, color='k')
plt.ylabel(r'$v_{\mathrm{mp}}$ [km s$^{-1}$]', fontsize=18, color='k')
plt.ylim(10**-1, 10**4)
plt.xlim(10**-1, 1.5*10**2)
plt.xscale('log')
plt.yscale('log')
plt.yticks(fontsize=16)
plt.xticks(fontsize=16)
plt.legend(prop={'size': 12})
plt.tight_layout()
plt.title(
    f"{name} " + r"$(%.1f \times 10^{%d}~M_\odot)$" % (mantissa, exponent),
    fontsize=20,
    fontweight='bold')

# define filename and full save path
filename = f"probvel__{name.replace(' ', '_')}.png"
save_path = object_dir / filename

if save_plots:
    fig.savefig(save_path, bbox_inches='tight')

#plt.show()

## distances where the atmospheric escape arising from thermal heating is significant

# determine intersection of v_mp and v_esc

def find_intersection_radius(x, k, j, vfug):
    """Return the radius (in kpc) where Vmp crosses vfug, or None if no intersection."""
    diff = Vmp(x, k, j) - vfug
    idx = np.where(np.diff(np.sign(diff)))[0]
    return x[idx[0]] / 1000 if idx.size > 0 else None

# define the 4 cases

cases = [
    ("energy-driven N2", 0, 0),
    ("energy-driven H2", 1, 0),
    ("momentum-driven N2", 0, 1),
    ("momentum-driven H2", 1, 1)
]

# find results

results = []

for label, k, j in cases:
    r_int = find_intersection_radius(x, k, j, vfug)
    if r_int is not None:
        msg = f"{name}: {label} → R = {r_int:.2f} kpc"
    else:
        msg = f"{name}: {label} → R = N/A kpc"
    #print(msg)
    results.append(msg)

## save to text file

with open(output_file, "a", encoding="utf-8") as f:
    f.write("### Distances where v_mp intersects v_esc (atm escape from thermal heating) ###\n")
    for line in results:
        f.write(line + "\n")
    f.write("\n")

## mass loss

r0 = 10.                          #Minimum distance we consider from the central SMBH (pc)
r1 = 100000.                        #Maximum distance we consider from the central SMBH (pc)
x = np.arange(r0,r1,1.)
kinpow=[0.05 , 0.001]              #fractions of the AGN luminosity to be converted into wind's kinetic power

M_lostE = np.zeros((len(x)))       #Mass lost in the interaction with the outflow in the energy driven (E) case
for i in range(0,len(x)):
    m = (3./(16.*np.pi*G*rho))*(kinpow[0]*Ledd*t_salp/(x[i]*r_pc)**2)
    M_lostE[i]= m

M_lostM = np.zeros((len(x)))     # Mass lost in the interaction with the outflow in the momentum driven (M) case
for i in range(0,len(x)):
    m = (3./(8.*np.pi*G*rho))*(kinpow[1]*Ledd*t_salp/(x[i]*r_pc)**2)
    M_lostM[i]= m

fig = plt.figure(facecolor='white', figsize=(7,5))
plt.plot(x/1000., M_lostE/ma, 'magenta', linestyle='-',
         label=r'$M_{\mathrm{ed}}$')
plt.plot(x/1000., M_lostM/ma, 'dodgerblue', linestyle='-',
         label=r'$M_{\mathrm{md}}$')

plt.plot(x/1000.,3.*x**0.,'k', linestyle=':', linewidth=1)
plt.plot(x/1000.,1.*x**0., 'k', linestyle=':', linewidth=1)
plt.plot(x/1000.,0.3*x**0., 'k',linestyle=':', linewidth=1)
plt.plot(x/1000.,0.05*x**0., 'k', linestyle=':', linewidth=1)
plt.annotate(r'3',
                 ((r1-1000)/1000.,3+1),
                 textcoords="offset points",
                 xytext=(0,0),
                 fontsize=14,
                 ha='right')
plt.annotate(r'1',
                 ((r1-1000)/1000.,1+0.2),
                 textcoords="offset points",
                 xytext=(0,0),
                 fontsize=14,
                 ha='right')
plt.annotate(r'0.3',
                 ((r1-1000)/1000.,0.3+0.1),
                 textcoords="offset points",
                 xytext=(0,0),
                 fontsize=14,
                 ha='right')
plt.annotate(r'0.05',
                 ((r1-1000)/1000.,0.05+0.02),
                 textcoords="offset points",
                 xytext=(0,0),
                 fontsize=14,
                 ha='right')
plt.yscale('log')
plt.ylim(10**-2, 10**2)
plt.xscale('log')
plt.xlim(10**-2, 10**2)
plt.yticks(fontsize=16)
plt.xticks(fontsize=16)
plt.legend(prop={'size': 14})
plt.xlabel('R [kpc] ', fontsize=20, color='k')
plt.ylabel(r'$M_{\mathrm{lost}}/M_{\mathrm{atm,\oplus}}$', fontsize=18, color='k') #in terrestrial atmospheres
plt.tight_layout()
plt.title(
    f"{name} " + r"$(%.1f \times 10^{%d}~M_\odot)$" % (mantissa, exponent),
    fontsize=20,
    fontweight='bold')

# define filename and full save path
filename = f"massloss__{name.replace(' ', '_')}.png"
save_path = object_dir / filename

if save_plots:
    fig.savefig(save_path, bbox_inches='tight')

#plt.show()

## distances where the energy-limited hydrodynamic-like atm escape is significant

# find the index where the difference between M_lostE/ma and 1 changes sign
diff_M_lostE = M_lostE / ma - 1
idx_intersect_M_lostE = np.where(np.diff(np.sign(diff_M_lostE)))[0][0]

# find the index where the difference between M_lostM/ma and 1 changes sign
diff_M_lostM = M_lostM / ma - 1
idx_intersect_M_lostM = np.where(np.diff(np.sign(diff_M_lostM)))[0][0]

# get the R values at these intersection indices
r_intersect_M_lostE = x[idx_intersect_M_lostE]
r_intersect_M_lostM = x[idx_intersect_M_lostM]

# append mass-loss results to text file
with open(output_file, "a", encoding="utf-8") as f:
    f.write("### Distance where M_lost/M_atm intersect 1 (energy-limited hydrodynamic-like atm escape) ###\n")
    f.write(f"For energy-driven: R = {r_intersect_M_lostE/1000:.2f} kpc\n")
    f.write(f"For momentum-driven: R = {r_intersect_M_lostM/1000:.2f} kpc\n\n")

## dependence of ozone depletion on radial distance

ed_power = 0.05*Ledd    #in J/s
md_power = 0.001*Ledd     #in J/s
#converting the power to erg/yr
ed_power_conv = ed_power * ((10**7) / (3.17*10**(-8)))
md_power_conv = md_power * ((10**7) / (3.17*10**(-8)))
#flux in units of erg cm^-2 yr^-1
ed_flux = ed_power_conv / ((16*np.pi)*(R_cm**2))
md_flux = md_power_conv / (16*np.pi*R_cm**2)

# energy-driven NO concentration (y) in ppb
R0 = 9*10**14     #in molec cm^-2 yr^-1
Phi0 = 9*10**4    #in erg cm^-2 yr^-1
y0 = 3            #in ppb
sigma_strat = 5*10**23  #in molec cm^-2

# Compute the constant term (c in quadratic formula)
c = - (R0 * ed_flux / Phi0) * ((10 + y0) * t_salp_yr * 10**9 / sigma_strat)

# Quadratic coefficients
a = 1  # Coefficient of y^2
b = 10  # Coefficient of y

# Solve using the quadratic formula
discriminant = b**2 - 4*a*c

"""if discriminant >= 0:
    y1_ed = (-b + np.sqrt(discriminant)) / (2*a)
    y2 = (-b - np.sqrt(discriminant)) / (2*a)
    print(f"Solutions for y: {y1_ed}, {y2}")
else:
    print("No real solutions (discriminant < 0)")"""

# Iterate through each element of the discriminant array
y1_ed = []  # Store solutions for y1_ed
y2_ed = []
for disc in discriminant:
    if disc >= 0:
        y1_ed.append((-b + np.sqrt(disc)) / (2*a))
        y2_ed.append((-b - np.sqrt(disc)) / (2*a))
    else:
        # Handle cases where discriminant is negative (e.g., append NaN)
        y1_ed.append(np.nan)
        y2_ed.append(np.nan)
        #print("No real solutions (discriminant < 0)")

y1_ed = np.array(y1_ed) # Convert the list of solutions to an array
y2_ed = np.array(y2_ed)

#momentum-driven NO concentration (y) in ppb
# Compute the constant term (c in quadratic formula)
c = - (R0 * md_flux / Phi0) * ((10 + y0) * t_salp_yr * 10**9 / sigma_strat)

# Quadratic coefficients
a = 1  # Coefficient of y^2
b = 10  # Coefficient of y

# Solve using the quadratic formula
discriminant = b**2 - 4*a*c

"""if discriminant >= 0:
    y1_md = (-b + np.sqrt(discriminant)) / (2*a)
    y2 = (-b - np.sqrt(discriminant)) / (2*a)
    print(f"Solutions for y: {y1_md}, {y2}")
else:
    print("No real solutions (discriminant < 0)")"""

# Iterate through each element of the discriminant array
y1_md = []  # Store solutions for y1_md
y2_md = []  # Store solutions for y2_md
for disc in discriminant:
    if disc >= 0:
        y1_md.append((-b + np.sqrt(disc)) / (2*a))
        y2_md.append((-b - np.sqrt(disc)) / (2*a))
    else:
        # Handle cases where discriminant is negative (e.g., append NaN)
        y1_md.append(np.nan)
        y2_md.append(np.nan)
        #print("No real solutions (discriminant < 0)")

y1_md = np.array(y1_md)  # Convert the list of solutions to an array
y2_md = np.array(y2_md)  # Convert the list of solutions to an array

#ratios of perturbed and unperturbed NO abundances
ed_x = ((3+ y1_ed)/3)
md_x = ((3+y1_md)/3)
#print(ed_x)
#print(md_x)

#ratio of stratospheric ozone abundance
F_ed = (np.sqrt(16+9*ed_x**2) - 3*ed_x)/2
F_md = (np.sqrt(16+9*md_x**2) - 3*md_x)/2

#fractional ozone depletion
D_ed = 1 - F_ed
D_md = 1 - F_md
#print(D_ed)
#print(D_md)

## ozone depletion in a Salpeter time (t = t_salp)

#define k
k = (R0/Phi0) * (((10**9)*(10+y0))/sigma_strat)

#define new value for y
y = 37     #in ppb

time_dep_ed = (1739)/(k*ed_flux)
time_dep_md = (1739)/(k*md_flux)
#print(time_dep_ed)
#print(time_dep_md)

## plot
## Ozone Depletion in Salpeter Time
fig = plt.figure(facecolor='white', figsize=(7,5))
fig, ax = plt.subplots()
ax.set_ylabel('D [%]',fontsize=20, color='k')
ax.set_xlabel('R [kpc]',fontsize=20, color='k')
ax.plot(R_kpc, D_ed, 'magenta', linestyle='-',
        label=r'$D_{\mathrm{ed}}$')     # Ozone depletion, energy-driven
ax.plot(R_kpc, D_md, 'dodgerblue', linestyle='-',
        label=r'$D_{\mathrm{md}}$')     # Ozone depletion, momentum-driven

yvals = ax.get_yticks()
#ax.set_yticklabels(["{:,.1%}".format(y) for y in yvals], fontsize=16)
plt.ylim(0.995, 1.001)
plt.xlim(10**-1, 1.5*10**2)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
ax.set_xscale('log')
plt.tight_layout()
plt.legend(prop={'size': 14}, loc='lower left')
plt.title(
    f"{name} " + r"$(%.1f \times 10^{%d}~M_\odot)$" % (mantissa, exponent),
    fontsize=20,
    fontweight='bold')

# define filename and full save path
filename = f"ozonedepl__{name.replace(' ', '_')}.png"
save_path = object_dir / filename

if save_plots:
    fig.savefig(save_path, bbox_inches='tight')

#plt.show()

## required time for 90% ozone depletion

## plot
## 90% Ozone Depletion
fig = plt.figure(facecolor='white', figsize=(7,5))
plt.plot(R_kpc, time_dep_ed, 'magenta', linestyle='-',
         label=r'$\Delta t_{\mathrm{ed}}$')    # Energy-driven case
plt.plot(R_kpc, time_dep_md, 'dodgerblue', linestyle='-',
         label=r'$\Delta t_{\mathrm{md}}$')    # Momentum-driven case

plt.plot(8,time_dep_ed[8],'ro')
plt.plot(8,time_dep_md[8],'ro')
plt.axvline(x=8, color='firebrick', linestyle=':', linewidth=2.5, alpha=0.9,
            label=r'$R = 8~\mathrm{kpc}$')
#plt.annotate(r'$R = 8kpc$',
                 #(15,0.0002),
                 #textcoords="offset points",
                 #xytext=(0,0),
                 #fontsize=12,
                 #rotation=90,
                 #ha='right')
#plt.axhline(4, color='gray', linestyle='--', linewidth=1)
#plt.annotate(r'$\Delta t = 4$ yr',
             #xy=(0.1, 4), xycoords='data',  # Adjust x position as needed
             #xytext=(10, 5), textcoords='offset points',
             #fontsize=12, color='black')
plt.xscale('log')
plt.yscale('log')
plt.ylim(10**-3, 10**6)
plt.legend(prop={'size': 14}, loc='upper left')
plt.xlabel('R [kpc] ', fontsize=20, color='k')
plt.ylabel(r'$\Delta t$ [yr]', fontsize=20, color='k')
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
plt.title(
    f"{name} " + r"$(%.1f \times 10^{%d}~M_\odot)$" % (mantissa, exponent),
    fontsize=20,
    fontweight='bold')

# define filename and full save path
filename = f"90percent__{name.replace(' ', '_')}.png"
save_path = object_dir / filename

if save_plots:
    fig.savefig(save_path, bbox_inches='tight')

#plt.show()

## distances where major ozone depletion (90% loss) due to NO formation is significant

def find_intersection_radius_ozone(x, y, value):
    """Return the radius (in kpc) where y crosses 'value', using linear interpolation."""
    diff = y - value
    idx = np.where(np.diff(np.sign(diff)))[0]
    if len(idx) == 0:
        return None
    i = idx[0]
    # Linear interpolation for better precision
    x0, x1 = x[i], x[i+1]
    y0, y1 = y[i], y[i+1]
    return x0 + (value - y0) * (x1 - x0) / (y1 - y0)

# define ozone depletion cases
cases_ozone = [
    ("energy-driven", R_kpc, time_dep_ed),
    ("momentum-driven", R_kpc, time_dep_md)
]

# collect results
ozone_results = []

for label, x_vals, y_vals in cases_ozone:
    r_int = find_intersection_radius_ozone(x_vals, y_vals, 4)  # Δt = 4 yr threshold
    if r_int is not None:
        msg = f"{name}: {label} → Δt = 4 yr at R = {r_int:.2f} kpc"
    else:
        msg = f"{name}: {label} → No intersection found"
    #print(msg)
    ozone_results.append(msg)

# append to output file
with open(output_file, "a", encoding="utf-8") as f:
    f.write("### Distances of Major Ozone Depletion (Δt = 4 yr) ###\n")
    for line in ozone_results:
        f.write(line + "\n")
    f.write("\n")
