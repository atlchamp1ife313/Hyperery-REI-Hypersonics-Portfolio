"""
Hyperery REI: 3D Plume Mitigation & Signature Comparison Model
Renders Unmitigated, Mitigated, and ULO Quenched plumes simultaneously in a single 3D scene.
"""

import numpy as np
import plotly.graph_objects as go

def generate_3d_comparison_model():
    # Common spatial grids
    x = np.linspace(0.0, 30.0, 200)
    theta = np.linspace(0, 2 * np.pi, 50)
    X, THETA = np.meshgrid(x, theta)
    
    # 1. Unmitigated Baseline Plume (Offset Y = +6m)
    r0_1 = 0.6
    r_1 = (r0_1 + 0.08 * X) * (1.0 + 0.3 * np.exp(-0.05 * X) * np.cos(1.2 * X))
    Y_1 = r_1 * np.cos(THETA) + 6.0
    Z_1 = r_1 * np.sin(THETA)
    intensity_1 = np.clip(np.exp(-0.05 * X) * (r0_1 / np.maximum(r_1, 0.1)), 0, 1)
    
    # 2. Hyperery Mitigated Plume (Center Y = 0m)
    r0_2 = 0.4
    r_2 = (r0_2 + 0.05 * X**0.75) * (1.0 + 0.22 * np.exp(-0.08 * X) * np.cos(1.4 * X))
    Y_2 = r_2 * np.cos(THETA)
    Z_2 = r_2 * np.sin(THETA)
    intensity_2 = np.clip(np.exp(-0.12 * X) * (r0_2 / np.maximum(r_2, 0.1)), 0, 1)
    
    # 3. ULO Quenched Plume (Offset Y = -6m, restricted to 10km rapid drop)
    x_ulo = np.linspace(0.0, 10.0, 200)
    X_ulo, THETA_ulo = np.meshgrid(x_ulo, theta)
    r0_3 = 0.25
    r_3 = (r0_3 + 0.02 * X_ulo) * (1.0 + 0.05 * np.exp(-1.0 * X_ulo) * np.cos(3.0 * X_ulo))
    Y_3 = r_3 * np.cos(THETA_ulo) - 6.0
    Z_3 = r_3 * np.sin(THETA_ulo)
    intensity_3 = np.clip(np.exp(-1.8 * X_ulo) * (r0_3 / np.maximum(r_3, 0.05)), 0, 1)
    
    # Build Combined 3D Figure
    fig = go.Figure()
    
    # Trace 1: Unmitigated Baseline (Hot palette)
    fig.add_trace(go.Surface(
        x=X, y=Y_1, z=Z_1, surfacecolor=intensity_1,
        colorscale='Hot', opacity=0.88, name='Unmitigated Baseline'
    ))
    
    # Trace 2: Hyperery Mitigated (Inferno palette)
    fig.add_trace(go.Surface(
        x=X, y=Y_2, z=Z_2, surfacecolor=intensity_2,
        colorscale='Inferno', opacity=0.88, name='Hyperery Mitigated'
    ))
    
    # Trace 3: ULO Quenched (Viridis palette)
    fig.add_trace(go.Surface(
        x=X_ulo, y=Y_3, z=Z_3, surfacecolor=intensity_3,
        colorscale='Viridis', opacity=0.88, name='ULO Quenched'
    ))
    
    fig.update_layout(
        title='Hyperery REI: 3D Plume Mitigation & Signature Comparison Matrix',
        scene=dict(
            xaxis_title='Downrange Distance (km)',
            yaxis_title='Configuration Offset Y (m)',
            zaxis_title='Radial Spread Z (m)',
            aspectratio=dict(x=2.0, y=1.5, z=1.0)
        ),
        template='plotly_dark',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    fig.write_html('plume_3d_comparison_model.html')
    print("Successfully generated and saved 'plume_3d_comparison_model.html'.")
    fig.show()

if __name__ == '__main__':
    generate_3d_comparison_model()
