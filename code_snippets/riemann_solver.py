"""
Hyperery REI (Hypersonics ReImagined)
1D Euler Solver / Ideal Gas Riemann Solver
Demonstrates high-speed flux evaluation for shock-capturing algorithms.
"""

import numpy as np

def compute_euler_fluxes(rho, u, p, gamma=1.4):
    """
    Computes 1D Euler flux vector given primitive variables.
    
    Parameters:
    rho : float - Density
    u   : float - Velocity
    p   : float - Pressure
    gamma : float - Ratio of specific heats (default 1.4 for air)
    """
    # Total energy per unit volume
    E = p / (gamma - 1.0) + 0.5 * rho * (u**2)
    
    # Flux vector: [mass flux, momentum flux, energy flux]
    F_mass = rho * u
    F_momentum = rho * (u**2) + p
    F_energy = (E + p) * u
    
    return np.array([F_mass, F_momentum, F_energy])

if __name__ == "__main__":
    # Test case: Hypersonic free-stream conditions (Mach > 5)
    rho_inf = 0.0118  # kg/m^3 (high altitude)
    u_inf = 1700.0    # m/s
    p_inf = 1000.0    # Pa
    
    fluxes = compute_euler_fluxes(rho_inf, u_inf, p_inf)
    print("--- Hyperery REI Euler Flux Solver ---")
    print(f"Mass Flux:     {fluxes[0]:.4f} kg/(m^2 s)")
    print(f"Momentum Flux: {fluxes[1]:.4f} N/m^2")
    print(f"Energy Flux:   {fluxes[2]:.4f} W/m^2")
