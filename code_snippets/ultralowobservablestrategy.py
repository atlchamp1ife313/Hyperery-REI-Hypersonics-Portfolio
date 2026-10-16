"""
Hyperery REI: Ultra-Low Observable (ULO) Mitigated Plume 3D Visualizer
Simulates radical quenching, film cooling, and soot suppression resulting in near-immediate signature collapse.
"""

import numpy as np
import plotly.graph_objects as go

def generate_ulo_plume():
    # 1. Focused spatial grid (0 to 5 km where active suppression occurs)
    x = np.linspace(0.0, 5.0, 200)
    theta = np.linspace(0, 2 * np.pi, 60)
    X, THETA = np.meshgrid(x, theta)
    
    # 2. ULO Suppressed Geometry: Minimal radial bloom due to micro-mixers and boundary wall cooling
    r0 = 0.3
    r = (r0 + 0.02 * X) * (1.0 + 0.05 * np.exp(-1.0 * X) * np.cos(3.0 * X))
    Y, Z = r * np.cos(THETA), r * np.sin(THETA)
    
    # 3. Rapid Thermal & Signature Collapse (Driven by endothermic quenching & particulate elimination)
    # Intensity drops exponentially below sensor noise floors within ~1.5 km
    intensity = np.clip(np.exp(-1.8 * X) * (r0 / np.maximum(r, 0.05)), 0, 1)
    
    # 4. Render Interactive Surface with 'Viridis' or stealth-optimized palette
    fig = go.Figure(data=[go.Surface(
        x=X, y=Y, z=Z, 
        surfacecolor=intensity,
        colorscale='Viridis', 
        opacity=0.85,
        colorbar=dict(title='Suppressed Signature<br>(Sub-Threshold)')
    )])
    
    fig.update_layout(
        title='Hyperery REI: Ultra-Low Observable (ULO) Quenched Plume',
        scene=dict(
            xaxis_title='Downrange Standoff (km)', 
            yaxis_title='Radial Spread Y (m)', 
            zaxis_title='Radial Spread Z (m)',
            aspectratio=dict(x=1.5, y=1.0, z=1.0)
        ),
        template='plotly_dark', 
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    # Save interactive HTML asset for your R&D portfolio
    fig.write_html('ulo_mitigated_plume_3d.html')
    print("Successfully generated and saved 'ulo_mitigated_plume_3d.html'.")
    fig.show()

if __name__ == '__main__':
    generate_ulo_plume()
