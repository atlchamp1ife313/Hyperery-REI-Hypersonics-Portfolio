"""
Hyperery REI (Hypersonics ReImagined)
Plume Ionization & Molecular Dissociation Modeling Module (Fixed Escape Sequence)
"""

import numpy as np
import matplotlib.pyplot as plt

def calculate_plasma_and_dissociation():
    x = np.linspace(0.0, 30.0, 300)
    
    T_exit = 3500.0
    T_ambient = 300.0
    T_core = T_ambient + (T_exit - T_ambient) * np.exp(-0.15 * x)
    
    dissociation_fraction = 1.0 / (1.0 + np.exp((2200.0 - T_core) / 200.0))
    
    k_B = 1.380649e-23
    ionization_potential_eV = 13.6
    eV_to_Joules = 1.60218e-19
    E_ion = ionization_potential_eV * eV_to_Joules
    
    n_0 = 1e18
    electron_density = n_0 * np.power(T_core / 300.0, 1.5) * np.exp(-E_ion / (k_B * T_core))
    electron_density = np.maximum(electron_density, 0.0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), dpi=300)
    
    color = 'tab:red'
    ax1.set_xlabel('Downrange Distance (km)', fontsize=10)
    ax1.set_ylabel('Core Temperature (K)', color=color, fontsize=10)
    ax1.plot(x, T_core, color=color, linewidth=2.5, label='Core Temperature (K)')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle=':', alpha=0.5)
    
    ax2_twin = ax1.twinx()
    color = 'tab:blue'
    ax2_twin.set_ylabel(r'Dissociation Fraction ($\alpha_d$)', color=color, fontsize=10) # <-- Fixed with raw string 'r'
    ax2_twin.plot(x, dissociation_fraction, color=color, linewidth=2.5, linestyle='--', label='Dissociation Fraction')
    ax2_twin.tick_params(axis='y', labelcolor=color)
    ax2_twin.set_ylim(-0.05, 1.05)
    
    ax1.set_title('Thermal Dissociation vs. Downrange Distance', fontsize=11, fontweight='bold')
    
    ax2.plot(x, np.log10(electron_density + 1), color='darkviolet', linewidth=2.5)
    ax2.set_title(r'Plasma Formation: $\log_{10}$ Electron Density ($m^{-3}$)', fontsize=11, fontweight='bold') # <-- Fixed here too
    ax2.set_xlabel('Downrange Distance (km)', fontsize=10)
    ax2.set_ylabel(r'$\log_{10}(n_e + 1)$ ($m^{-3}$)', fontsize=10)
    ax2.grid(True, linestyle=':', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('plume_dissociation_and_plasma.png', dpi=300)
    print("Successfully generated and saved 'plume_dissociation_and_plasma.png' (300 DPI).")
    plt.show()

if __name__ == '__main__':
    calculate_plasma_and_dissociation()
