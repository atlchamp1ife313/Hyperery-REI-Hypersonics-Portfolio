"""
Hyperery REI (Hypersonics ReImagined)
Atmospheric Optics & Trajectory Illumination Analysis
Script: Idealized Minimum Altitude for Direct Sunlight vs. Solar Depression
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_min_altitude():
    # Solar depression angles (degrees) from 0 to 15
    solar_depression = np.linspace(0, 15, 200)
    
    # Earth radius in km
    R_earth = 6371.0
    
    # Mathematical model: Minimum altitude h required to intercept direct sunlight
    # h = R_earth * (sec(theta) - 1) converted to radians
    theta_rad = np.radians(solar_depression)
    min_altitude = R_earth * (1.0 / np.cos(theta_rad) - 1.0)

    plt.figure(figsize=(9, 6))
    
    # Plot curve
    plt.plot(solar_depression, min_altitude, color='#1f77b4', linewidth=2.5)

    # Styling and Labels
    plt.xlabel('Solar Depression at the Point of Interest (degrees)', fontsize=11, fontweight='bold')
    plt.ylabel('Minimum Altitude (km)', fontsize=11, fontweight='bold')
    plt.title('2. Idealized Minimum Altitude for Direct Sunlight', fontsize=13, fontweight='bold', pad=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.xlim(-0.5, 15.5)
    plt.tight_layout()
    
    # Save figure for technical report inclusion
    plt.savefig('Idealized_Min_Altitude_Sunlight.png', dpi=300)
    print("--- Hyperery REI Plot Generation Complete ---")
    plt.show()

if __name__ == '__main__':
    plot_min_altitude()
