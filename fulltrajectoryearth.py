"""
Hyperery REI: Orbital-Scale Full-Trajectory & Earth Globe Model
Renders ascent corridors and plume dispersion profiles in orbit above a 3D Earth sphere.
"""

import numpy as np
from scipy.integrate import solve_ivp
import plotly.graph_objects as go

def run_trajectory_ode_solver():
    x_eval = np.linspace(10.0, 1000.0, 300) # Downrange distance in km
    
    def trajectory_physics_ode(x, y, ascent_rate_factor):
        r, altitude, intensity = y
        dr_dx = 0.015 * (1.0 + 5.0 * np.exp(-0.005 * x))
        alt_target = 400.0
        dalt_dx = ascent_rate_factor * (alt_target - altitude) / max(x, 10.0)
        dint_dx = -0.004 * intensity
        return [dr_dx, dalt_dx, dint_dx]

    sol_1 = solve_ivp(trajectory_physics_ode, [10.0, 1000.0], [2.0, 1.0, 1.0], args=(0.08,), t_eval=x_eval)
    sol_2 = solve_ivp(trajectory_physics_ode, [10.0, 1000.0], [1.2, 1.0, 0.7], args=(0.06,), t_eval=x_eval)
    sol_3 = solve_ivp(trajectory_physics_ode, [10.0, 500.0], [0.8, 1.0, 0.3], args=(0.12,), t_eval=np.linspace(10.0, 500.0, 300))

    return sol_1, sol_2, sol_3, x_eval

def generate_orbital_earth_model():
    sol_1, sol_2, sol_3, x_eval = run_trajectory_ode_solver()
    theta = np.linspace(0, 2 * np.pi, 50)

    # --- Generate Earth Sphere Surface ---
    R_earth = 6371.0 # Earth radius in km
    phi = np.linspace(0, np.pi / 2, 40) # Latitude slice
    theta_earth = np.linspace(0, 2 * np.pi, 60) # Longitude slice
    PHI_E, TH_E = np.meshgrid(phi, theta_earth)
    
    # Position Earth center so its surface touches Z = 0 at the launch origin
    X_earth = R_earth * np.sin(PHI_E) * np.cos(TH_E) + 200.0
    Y_earth = R_earth * np.sin(PHI_E) * np.sin(TH_E)
    Z_earth = R_earth * np.cos(PHI_E) - R_earth

    def build_macro_surface(sol, x_grid, y_offset, is_short=False):
        grid = np.linspace(10.0, 500.0, 300) if is_short else x_eval
        X, THETA = np.meshgrid(grid, theta)
        
        r_base = np.array([sol.y[0]] * len(theta))
        alt_base = np.array([sol.y[1]] * len(theta))
        int_base = np.array([sol.y[2]] * len(theta))
        
        R = r_base * (1.0 + 0.2 * np.sin(0.02 * X))
        Y = R * np.cos(THETA) + y_offset
        Z = alt_base + R * np.sin(THETA)
        
        return X, Y, Z, int_base

    X_1, Y_1, Z_1, sig_1 = build_macro_surface(sol_1, x_eval, 50.0)
    X_2, Y_2, Z_2, sig_2 = build_macro_surface(sol_2, x_eval, 0.0)
    X_3, Y_3, Z_3, sig_3 = build_macro_surface(sol_3, sol_3.t, -50.0, is_short=True)

    fig = go.Figure()
    
    # Trace 0: Earth Globe Surface (Deep blue/slate tint for space aesthetic)
    fig.add_trace(go.Surface(
        x=X_earth, y=Y_earth, z=Z_earth,
        colorscale=[[0, '#0f172a'], [1, '#1e293b']],
        showscale=False, opacity=0.7, name='Earth Curvature'
    ))

    # Trace 1: Standard Ascent Corridor
    fig.add_trace(go.Surface(
        x=X_1, y=Y_1, z=Z_1, surfacecolor=sig_1,
        colorscale='Hot', opacity=0.85, name='Standard Ascent Corridor'
    ))
    
    # Trace 2: Optimized Corridor
    fig.add_trace(go.Surface(
        x=X_2, y=Y_2, z=Z_2, surfacecolor=sig_2,
        colorscale='Inferno', opacity=0.85, name='Optimized Corridor'
    ))
    
    # Trace 3: Quenched Profile
    fig.add_trace(go.Surface(
        x=X_3, y=Y_3, z=Z_3, surfacecolor=sig_3,
        colorscale='Viridis', opacity=0.85, name='Quenched / Suppressed Profile'
    ))
    
    fig.update_layout(
        title='Hyperery REI: Orbital View & Trajectory Ascent Matrix over Earth',
        scene=dict(
            xaxis_title='Downrange Distance (km)',
            yaxis_title='Crossrange Offset (km)',
            zaxis_title='Altitude (km)',
            aspectratio=dict(x=2.5, y=1.5, z=1.2)
        ),
        template='plotly_dark',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    fig.write_html('orbital_earth_trajectory_model.html')
    print("Successfully generated 'orbital_earth_trajectory_model.html'.")
    fig.show()

if __name__ == '__main__':
    generate_orbital_earth_model()
