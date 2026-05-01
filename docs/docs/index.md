# Welcome to the AGN Habitability model documentation!

AGN Habitability is a computational framework designed to model the impact of AGN-driven outflows on planetary atmospheres. The code quantifies how outflow-induced energy deposition alters atmospheric structure through heating, changes in molecular velocity distributions, atmospheric escape, and ozone depletion.

This repository accompanies the study:
“The Impact of Supermassive Black Holes on Exoplanet Habitability: I. Spanning the Natural Mass Range.”

## Overview

Active galactic nuclei (AGN) emit powerful ultrafast outflows (UFOs) that carry significant energy into their host galaxies. These outflows may interact with planetary atmospheres, depositing energy which drives significant increase in atmospheric temperature, enhancing conditions for escape and depletion of ozone.

This code models these processes using parameterizations for AGN outflows and evaluates their effects across a wide range of supermassive black hole (SMBH) masses and galactocentric distances.

## Diagnostic Features

The model focuses on five primary atmospheric diagnostics:

- Atmospheric heating
- Most probable velocity of molecules in the atmosphere
- Atmospheric mass loss
- Percentage of ozone depletion
- Timescale for 90% ozone depletion

These features are contained in plotted outputs.

For any specific galaxy, with a given SMBH mass input, the model computes the following in addition to the above plots:

- Maximum distance of influence where atmospheric escape arises from thermal heating
- Maximum distance of influence for energy-limited hydrodynamic-like escape
- Maximum distance for major ozone depletion (90% loss) due to nitrogen oxide formation

## Commands

The Makefile contains the central entry points for common tasks related to this project.

