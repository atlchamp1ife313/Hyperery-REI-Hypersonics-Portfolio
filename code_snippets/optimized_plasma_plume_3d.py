"""
Hyperery REI (Hypersonics ReImagined)
Optimized 3D Plume Plasma & Thermal Ionization Visualizer
Fixes color scaling so the ionization and temperature gradients are vividly rendered.
"""

import numpy as np
import plotly.graph_objects as go

def generate_3d_plasma_plume_optimized():
    # 1. Spatial Grids
    x_downrange = np.linspace(0.0, 30.0, 300)
    theta = np.linspace(0, 2 * np.pi, 80)
    X, THETA = np.meshgrid(x_downrange, theta)
    
    # 2. Plume Geometry with Shock Diamonds
    base_radius = 0.4
    expansion = 0.05 * np.power(X, 0.75)
    shock_frequency = 1.4
    shock_amplitude = 0.22 * np.exp(-0.08 * X)
    shock_effect = 1.0 + shock_amplitude * np.cos(shock_frequency * X)
    R = (base_radius + expansion) * shock_effect
    
    Y = R * np.cos(THETA)
    Z = R * np.sin(THETA)
    
    # 3. Normalized Thermal & Ionization Proxy Mapping for Visualization
    # Using a balanced decay profile so the transition from hot core to cooler outer envelope is clearly graded
    thermal_profile = np.exp(-0.12 * X) * (base_radius / np.maximum(R, 0.1))
    
    # Add localized intensity spikes at shock diamond nodes
    shock_glow = 0.3 * np.abs(np.cos(shock_frequency * X)) * np.exp(-0.05 * X)
    plasma_intensity = np.clip(thermal_profile + shock_glow, 0.0, 1.0)
    
    # 4. Build Interactive Plotly 3D Surface with High-Contrast 'Inferno' / 'Plasma' Scale
    fig = go.Figure(data=[go.Surface(
        x=X, y=Y, z=Z,
        surfacecolor=plasma_intensity,
        colorscale='Inferno',  # Brilliant thermal gradient from yellow-white core to dark purple edges
        opacity=0.95,
        colorbar=dict(title='Normalized Plasma<br>& Thermal Ionization')
    )])
    
    fig.update_layout(
        title='Hyperery REI: 3D Plume Plasma Ionization & Shock Thermal Mapping',
        scene=dict(
            xaxis_title='Downrange Standoff Distance (km)',
            yaxis_title='Radial Spread Y (m)',
            zaxis_title='Radial Spread Z (m)',
            camera=dict(eye=dict(x=1.6, y=2.0, z=0.9)),
            aspectratio=dict(x=2.0, y=1.0, z=1.0)
        ),
        template='plotly_dark',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    fig.write_html('predictive_plasma_plume_3d.html')
    print("Successfully generated and saved optimized 'predictive_plasma_plume_3d.html'.")
    fig.show()

if __name__ == '__main__':
    generate_3d_plasma_plume_optimized()
