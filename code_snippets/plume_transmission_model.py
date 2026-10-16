"""
Hyperery REI (Hypersonics ReImagined)
Atmospheric Plume Transmission & Infrared Radiance Model
Based on the Beer-Lambert Law for remote optical tracking analysis.
"""

import numpy as np

def calculate_plume_transmission(initial_radiance: float, path_length_km: float, absorption_coeff: float) -> float:
    """
    Calculates the transmitted infrared radiance of an exhaust plume
    after traveling through an absorbing atmosphere using the Beer-Lambert law.
    Formula: I = I_0 * exp(-alpha * x)
    """
    transmitted_radiance = initial_radiance * np.exp(-absorption_coeff * path_length_km)
    return transmitted_radiance

if __name__ == "__main__":
    # Execution with baseline values
    initial_plume_radiance = 100.0  # Arbitrary units of core thermal emission
    sample_range = 10.0             # Distance to sensor in kilometers
    absorption_coefficient = 0.045  # 1/km (IR absorption band)
    
    final_sig = calculate_plume_transmission(initial_plume_radiance, sample_range, absorption_coefficient)
    
    print("--- Hyperery REI Plume Transmission Analysis ---")
    print(f"Initial Plume Radiance: {initial_plume_radiance} units")
    print(f"Transmitted Radiance at {sample_range} km: {final_sig:.2f} units")
    print(f"Attenuation: {((initial_plume_radiance - final_sig)/initial_plume_radiance)*100:.1f}%")
