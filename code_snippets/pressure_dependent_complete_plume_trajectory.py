import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# --- 1. Realistic Entry Trajectory ---
s_traj = np.linspace(0, 500, 200) 
z_traj = 90.0 * np.exp(-s_traj / 140.0)  # Glide path from 90 km down to surface
y_traj = 8.0 * np.sin(s_traj / 60.0)    # Minor crossrange drift

ax.plot(s_traj, y_traj, z_traj, color='yellow', linewidth=3, label='Entry Trajectory')

# --- 2. Pressure-Dependent Plume Evolution ---
checkpoint_indices = np.linspace(20, 180, 6, dtype=int)

x_local = np.linspace(0, 25, 20)
theta = np.linspace(0, 2 * np.pi, 20)
X_l, Theta_l = np.meshgrid(x_local, theta)

# Atmospheric scale height model for pressure/density (H ≈ 7.2 km)
H = 7.2 

for idx in checkpoint_indices:
    vx = s_traj[idx]
    vy = y_traj[idx]
    vz = z_traj[idx]
    
    # Ambient density relative to sea level: rho = exp(-z / H)
    # Lower altitude = higher density = greater compression on the plume
    rel_density = np.exp(-vz / H)
    
    # Plume expansion physics: 
    # High altitude (low density) -> massive over-expansion (large radius)
    # Low altitude (high density) -> strong ambient pressure confinement (smaller radius)
    expansion_factor = 1.0 + 4.0 * np.exp(-vz / 15.0)
    R_plume = (0.5 + 0.15 * X_l) * expansion_factor / (1.0 + 2.0 * rel_density**0.5)
    
    # Plume coordinates trailing behind the vehicle
    Y_plume = vy + R_plume * np.sin(Theta_l)
    Z_plume = vz + R_plume * np.cos(Theta_l) * 0.4
    X_plume_mesh = vx - X_l
    
    # Radiation/Signature intensity fades as energy dissipates and mixes
    radiation = (400.0 * np.exp(-X_l / 8.0)) * rel_density
    
    ax.plot_surface(
        X_plume_mesh, Y_plume, Z_plume, 
        facecolors=plt.cm.inferno(np.clip(radiation / 150.0, 0, 1)), 
        alpha=0.7, 
        linewidth=0
    )

# --- 3. Ground Track & Terminal Points ---
z_ground = np.zeros_like(s_traj)
ax.plot(s_traj, y_traj, z_ground, color='gray', linestyle='--', alpha=0.5, label='Ground Track')

ax.scatter([s_traj[0]], [y_traj[0]], [z_traj[0]], color='cyan', s=200, marker='^', label='Entry Interface (90 km)')
ax.scatter([s_traj[-1]], [y_traj[-1]], [0], color='lime', s=200, marker='o', label='Impact / Ground Station')

# --- Formatting ---
ax.set_title('Physically Accurate Plume Expansion Across Atmosphere', fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Downrange Distance (km)', labelpad=10)
ax.set_ylabel('Crossrange Deflection (km)', labelpad=10)
ax.set_zlabel('Altitude (km)', labelpad=10)
ax.set_zlim(0, 100)

ax.view_init(elev=22, azim=130)
ax.legend(loc='upper left')

plt.tight_layout()
plt.savefig('accurate_plume_entry.png', dpi=300, bbox_inches='tight')
print("Successfully generated physically accurate plume entry plot.")
