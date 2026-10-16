"""
Hyperery REI (Hypersonics ReImagined)
EO/IR Plume Signature Analysis & Mitigation Model
Script: Plume Radiance Suppression and Atmospheric Attenuation
"""

import numpy as np

def calculate_mitigated_plume_signature(
    base_radiance: float, 
    temp_suppression_factor: float, 
    soot_reduction_factor: float, 
    path_length_km: float, 
    base_absorption_coeff: float
) -> dict:
    """
    Calculates the suppressed and transmitted infrared radiance of an exhaust plume
    after applying thermodynamic cooling and chemical/particulate modification.
    
    Formulas:
        - Suppressed Initial Radiance: I_0' = I_0 * (T_factor^4) * soot_factor
        - Beer-Lambert Attenuation: I_final = I_0' * exp(-alpha_eff * x)
    """
    # 1. Core emission reduction based on Stefan-Boltzmann / temperature scaling (T^4)
    # and particulate reduction affecting the effective absorption/scattering coefficient.
    mitigated_initial_radiance = base_radiance * (temp_suppression_factor ** 4) * soot_reduction_factor
    
    # 2. Effective absorption coefficient adjusted by particulate modifications
    effective_absorption_coeff = base_absorption_coeff * soot_reduction_factor
    
    # 3. Final transmitted radiance after atmospheric path transmission
    transmitted_radiance = mitigated_initial_radiance * np.exp(-effective_absorption_coeff * path_length_km)
    
    # 4. Total attenuation percentage relative to unmitigated baseline
    total_reduction_pct = ((base_radiance - transmitted_radiance) / base_radiance) * 100.0
    
    return {
        "mitigated_initial": mitigated_initial_radiance,
        "transmitted": transmitted_radiance,
        "total_reduction_pct": total_reduction_pct
    }

if __name__ == "__main__":
    # Baseline Parameters
    baseline_radiance = 100.0       # Unmitigated core thermal signature (arbitrary units)
    sensor_range_km = 12.0          # Observation path length in kilometers
    absorption_coeff = 0.045        # Baseline atmospheric IR absorption coefficient (1/km)
    
    # Engineering Mitigation Inputs
    # e.g., Film cooling reduces core temp scaling factor to 0.85; 
    # Chemical scavengers/nozzle mixing cuts soot/particulate emission by 40% (factor of 0.60)
    t_factor = 0.85
    soot_factor = 0.60
    
    results = calculate_mitigated_plume_signature(
        baseline_radiance, t_factor, soot_factor, sensor_range_km, absorption_coeff
    )
    
    print("--- Hyperery REI Plume Signature Reduction Analysis ---")
    print(f"Baseline Unmitigated Radiance: {baseline_radiance:.2f} units")
    print(f"Mitigated Initial Core Radiance: {results['mitigated_initial']:.2f} units")
    print(f"Final Transmitted Radiance at {sensor_range_km} km: {results['transmitted']:.2f} units")
    print(f"Total Signature Reduction Achieved: {results['total_reduction_pct']:.1f}%")
