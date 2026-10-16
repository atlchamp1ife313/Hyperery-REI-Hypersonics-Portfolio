"""
Hyperery REI (Hypersonics ReImagined)
Plume Ionization & Molecular Dissociation Modeling Module
Calculates thermal dissociation and electron density (Saha ionization) along the exhaust centerline.
"""

import numpy as np
import matplotlib.pyplot as plt

def calculate_plasma_and_dissociation():
    # 1. Downrange distance vector (km)
    x = np.linspace(0.0, 30.0, 300)
    
    # 2. Plume Core Temperature Profile (Kelvin)
    # Highest at nozzle exit (X=0, ~3500 K), dropping downstream as it expands and cools
    T_exit = 3500.0
    T_ambient = 300.0
    T_core = T_ambient + (T_exit - T_ambient) * np.exp(-0.15 * x)
    
    # 3. Molecular Dissociation Fraction (e.g., CO2 / H2O / O2 splitting)
    # Modeled via a sigmoidal thermal threshold activation
    # Below ~1500K dissociation is minimal; above ~2500K it spikes significantly.
    dissociation_fraction = 1.0 / (1.0 + np.exp((2200.0 - T_core) / 200.0))
    
    # 4. Plasma Ionization Calculation (Simplified Saha-like thermal ionization model)
    # Ionization energy threshold for typical exhaust species / air components (~12-15 eV)
    # Produces free electron density n_e (m^-3)
    k_B = 1.380649e-23  # Boltzmann constant (J/K)
    ionization_potential_eV = 13.6  # eV (approx for atomic species/air)
    eV_to_Joules = 1.60218e-19
    E_ion = ionization_potential_eV * eV_to_Joules
    
    # Pre-exponential scaling factor for plasma density
    n_0 = 1e18  # Reference particle density (m^-3)
    # Saha-like temperature dependency factor
    electron_density = n_0 * np.power(T_core / 300.0, 1.5) * np.exp(-E_ion / (k_B * T_core))
    
    # Ensure physical lower bounds
    electron_density = np.maximum(electron_density, 0.0)

    # 5. High-Resolution Plotting for Repository Documentation
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), dpi=300)
    
    # Plot 1: Core Temperature & Molecular Dissociation
    color = 'tab:red'
    ax1.set_xlabel('Downrange Distance (km)', fontsize=10)
    ax1.set_ylabel('Core Temperature (K)', color=color, fontsize=10)
    line1 = ax1.plot(x, T_core, color=color, linewidth=2.5, label='Core Temperature (K)')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle=':', alpha=0.5)
    
    ax2_twin = ax1.twinx()
    color = 'tab:blue'
    ax2_twin.set_ylabel('Dissociation Fraction ($\alpha_d$)', color=color, fontsize=10)
    line2 = ax2_twin.plot(x, dissociation_fraction, color=color, linewidth=2.5, linestyle='--', label='Dissociation Fraction')
    ax2_twin.tick_params(axis='y', labelcolor=color)
    ax2_twin.set_ylim(-0.05, 1.05)
    
    ax1.set_title('Thermal Dissociation vs. Downrange Distance', fontsize=11, fontweight='bold')
    
    # Plot 2: Plasma Electron Density (Log Scale for Plasma Formation)
    ax2.plot(x, np.log10(electron_density + 1), color='darkviolet', linewidth=2.5)
    ax2.set_title('Plasma Formation: Log10 Electron Density ($m^{-3}$)', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Downrange Distance (km)', fontsize=10)
    ax2.set_ylabel('$\log_{10}(n_e + 1)$ ($m^{-3}$)', fontsize=10)
    ax2.grid(True, linestyle=':', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('plume_dissociation_and_plasma.png', dpi=300)
    print("Successfully generated and saved 'plume_dissociation_and_plasma.png' (300 DPI).")
    plt.show()

if __name__ == '__main__':
    calculate_plasma_and_dissociation()
