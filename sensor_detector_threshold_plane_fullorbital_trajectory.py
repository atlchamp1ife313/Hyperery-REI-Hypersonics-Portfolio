"""
Hyperery REI: Orbital-Scale Detectability & Signature Suppression Model
Includes a Sensor Detection Threshold Plane to visually demonstrate 
when a plume drops below enemy infrared/optical tracking capabilities.
"""

import numpy as np
from scipy.integrate import solve_ivp
import plotly.graph_objects as go

def run_detectability_ode_solver():
    x_eval = np.linspace(10.0, 1000.0, 300)
    
    def detectability_physics_ode(x, y, suppression_rate):
        r, altitude, ir_signature = y
        dr_dx = 0.015 * (1.0 + 2.0 * np.exp(-0.005 * x))
        alt_target = 400.0
        dalt_dx = 0.08 * (alt_target - altitude) / max(x, 10.0)
        
        # IR Signature intensity decay (rapid drop for quenched/mitigated profiles)
        dir_dx = -suppression_rate * ir_signature * np.exp(-0.002 * x)
        
        return [dr_dx, dalt_dx, dir_dx]

    # --- 1. Unmitigated Baseline (Remains above detection threshold for long range) ---
    sol_1 = solve_ivp(detectability_physics_ode, [10.0, 1000.0], [2.0, 1.0, 1.0], args=(0.001,), t_eval=x_eval)
    
    # --- 2. Hyperery Mitigated (Moderate signature reduction) ---
    sol_2 = solve_ivp(detectability_physics_ode, [10.0, 1000.0], [1.5, 1.0, 0.6], args=(0.008,), t_eval=x_eval)
    
    # --- 3. ULO Quenched (Drops below sensor detection threshold early in flight) ---
    sol_3 = solve_ivp(detectability_physics_ode, [10.0, 1000.0], [1.0, 1.0, 0.2], args=(0.025,), t_eval=x_eval)

    return sol_1, sol_2, sol_3, x_eval

def generate_detectability_model():
    sol_1, sol_2, sol_3, x_eval = run_detectability_ode_solver()
    theta = np.linspace(0, 2 * np.pi, 50)

    # --- Earth Sphere Surface ---
    R_earth = 6371.0
    phi = np.linspace(0, np.pi / 2, 40)
    theta_earth = np.linspace(0, 2 * np.pi, 60)
    PHI_E, TH_E = np.meshgrid(phi, theta_earth)
    
    X_earth = R_earth * np.sin(PHI_E) * np.cos(TH_E) + 200.0
    Y_earth = R_earth * np.sin(PHI_E) * np.sin(TH_E)
    Z_earth = R_earth * np.cos(PHI_E) - R_earth

    def build_detectability_surface(sol, x_grid, y_offset):
        X, THETA = np.meshgrid(x_grid, theta)
        r_base = np.array([sol.y[0]] * len(theta))
        alt_base = np.array([sol.y[1]] * len(theta))
        sig_base = np.array([sol.y[2]] * len(theta))
        
        R = r_base * (1.0 + 0.1 * np.sin(0.02 * X))
        Y = R * np.cos(THETA) + y_offset
        Z = alt_base + R * np.sin(THETA)
        
        return X, Y, Z, sig_base

    X_1, Y_1, Z_1, sig_1 = build_detectability_surface(sol_1, x_eval, 60.0)
    X_2, Y_2, Z_2, sig_2 = build_detectability_surface(sol_2, x_eval, 0.0)
    X_3, Y_3, Z_3, sig_3 = build_detectability_surface(sol_3, x_eval, -60.0)

    fig = go.Figure()
    
    # Earth Curvature
    fig.add_trace(go.Surface(
        x=X_earth, y=Y_earth, z=Z_earth,
        colorscale=[[0, '#0f172a'], [1, '#1e293b']],
        showscale=False, opacity=0.6, name='Earth Curvature'
    ))

    # Trace 1: Unmitigated Baseline (Stays hot/detectable)
    fig.add_trace(go.Surface(
        x=X_1, y=Y_1, z=Z_1, surfacecolor=sig_1,
        colorscale='Hot', opacity=0.9, name='Unmitigated (Fully Detectable)'
    ))
    
    # Trace 2: Hyperery Mitigated 
    fig.add_trace(go.Surface(
        x=X_2, y=Y_2, z=Z_2, surfacecolor=sig_2,
        colorscale='Inferno', opacity=0.9, name='Mitigated (Reduced Footprint)'
    ))
    
    # Trace 3: ULO Quenched (Rapidly fades below sensor threshold)
    fig.add_trace(go.Surface(
        x=X_3, y=Y_3, z=Z_3, surfacecolor=sig_3,
        colorscale='Viridis', opacity=0.9, name='ULO Quenched (Sub-Threshold)'
    ))
    
    # --- Sensor Detection Threshold Marker / Plane ---
    # Adding a transparent reference plane showing where IR sensors lose tracking lock
    x_plane = np.linspace(50, 950, 10)
    y_plane = np.linspace(-100, 100, 10)
    X_p, Y_p = np.meshgrid(x_plane, y_plane)
    Z_p = np.full_figsize = np.ones_like(X_p) * 120.0 # Altitude threshold slice
    
    fig.add_trace(go.Surface(
        x=X_p, y=Y_p, z=Z_p,
        colorscale=[[0, 'rgba(0, 255, 255, 0.15)'], [1, 'rgba(0, 255, 255, 0.15)']],
        showscale=False, name='Sensor Detection Threshold'
    ))

    fig.update_layout(
        title='Hyperery REI: Orbital Detectability & Threshold Suppression Matrix',
        scene=dict(
            xaxis_title='Downrange Distance (km)',
            yaxis_title='Crossrange Offset (km)',
            zaxis_title='Altitude (km)',
            aspectratio=dict(x=2.5, y=1.5, z=1.2)
        ),
        template='plotly_dark',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    fig.write_html('detectability_threshold_model.html')
    print("Successfully generated 'detectability_threshold_model.html'.")
    fig.show()

if __name__ == '__main__':
    generate_detectability_model()
