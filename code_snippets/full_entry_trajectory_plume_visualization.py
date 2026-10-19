import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# --- 1. Define Full Entry Trajectory (From 100 km down to Ground) ---
# Downrange distance from entry interface
s_traj = np.linspace(0, 500, 200) 
# Re-entry altitude profile (e.g., exponential or hypocycloid glide slope)
z_traj = 100.0 * np.exp(-s_traj / 150.0)
# Lateral drift / crossrange
y_traj = 10.0 * np.sin(s_traj / 50.0)

# Plot the main spacecraft entry trajectory line
ax.plot(s_traj, y_traj, z_traj, color='yellow', linewidth=3, label='Entry Trajectory')

# --- 2. Model Evolving Plume at Key Re-entry Checkpoints ---
# Select specific downrange indices to render the 3D plume cross-sections/cones
checkpoint_indices = [20, 70, 120, 170]

x_local = np.linspace(0, 30, 25)
theta = np.linspace(0, 2 * np.pi, 20)
X_l, Theta_l = np.meshgrid(x_local, theta)

for idx in checkpoint_indices:
    vx = s_traj[idx]
    vy = y_traj[idx]
    vz = z_traj[idx]
    
    # Plume expansion grows larger as atmospheric pressure drops (higher altitude)
    altitude_factor = 0.5 + (vz / 100.0) * 1.5
    R_plume = (1.0 + 0.1 * X_l) * altitude_factor
    
    # Plume mesh coordinates trailing behind the vehicle position
    Y_plume = vy + R_plume * np.sin(Theta_l)
    Z_plume = vz + R_plume * np.cos(Theta_l) * 0.4
    X_plume_mesh = vx - X_l
    
    # Radiation intensity scaling based on altitude and local density
    radiation = (500.0 * np.exp(-X_l / 10.0)) * (vz / 100.0 + 0.2)
    
    ax.plot_surface(
        X_plume_mesh, Y_plume, Z_plume, 
        facecolors=plt.cm.plasma(radiation / 400.0), 
        alpha=0.5, 
        linewidth=0
    )

# --- 3. Ground Track & Impact / Sensor Point ---
z_ground = np.zeros_like(s_traj)
ax.plot(s_traj, y_traj, z_ground, color='gray', linestyle='--', alpha=0.6, label='Ground Track Projection')

# Mark Entry Interface and Touchdown / Sensor site
ax.scatter([s_traj[0]], [y_traj[0]], [z_traj[0]], color='cyan', s=200, marker='^', label='Entry Interface (100 km)')
ax.scatter([s_traj[-1]], [y_traj[-1]], [0], color='lime', s=200, marker='o', label='Impact / Ground Station')

# --- Formatting & View Configuration ---
ax.set_title('Full Atmospheric Re-Entry Plume Trajectory Study', fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Downrange Distance (km)', labelpad=10)
ax.set_ylabel('Crossrange Deflection (km)', labelpad=10)
ax.set_zlabel('Altitude (km)', labelpad=10)
ax.set_zlim(0, 110)

# Optimal viewing angle to see both descent profile and plume spread
ax.view_init(elev=25, azim=135)
ax.legend(loc='upper left')

plt.tight_layout()
plt.savefig('full_entry_trajectory_plume.png', dpi=300, bbox_inches='tight')
print("Successfully generated full entry trajectory plot.")
