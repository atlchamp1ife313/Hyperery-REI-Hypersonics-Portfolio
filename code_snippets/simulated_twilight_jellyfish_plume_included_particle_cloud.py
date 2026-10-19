import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Use a dark background to simulate the night sky
plt.style.use('dark_background')
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

# --- 1. Rocket Ascent Trajectory ---
t = np.linspace(0, 1, 200)
x_traj = 500 * (t ** 1.2)           # Downrange North (km)
y_traj = 150 * t                    # Eastward / Atlantic (km)
z_traj = 130 * (t ** 0.6)           # Altitude (km)

ax.plot(x_traj, y_traj, z_traj, color='yellow', linewidth=2.5, label='Rocket Flight Path')

# --- 2. Particle-Cloud "Jellyfish" Plume Simulation ---
# Instead of solid meshes, use thousands of glowing, transparent points
np.random.seed(42)
checkpoints = [80, 120, 160]

for idx in checkpoints:
    vx, vy, vz = x_traj[idx], y_traj[idx], z_traj[idx]
    
    if vz > 40: # High-altitude vacuum expansion zone
        # Exhaust trail direction vector (backward)
        dx_dt = 1.2 * 500 * (t[idx] ** 0.2)
        dy_dt = 150.0
        dz_dt = 0.6 * 130 * (t[idx] ** -0.4)
        mag = np.sqrt(dx_dt**2 + dy_dt**2 + dz_dt**2)
        ux, uy, uz = -dx_dt/mag, -dy_dt/mag, -dz_dt/mag
        
        # A. The "Jellyfish Head" (Bulbous cloud of particles)
        n_particles = 3000
        u = np.random.uniform(0, 1, n_particles)
        v = np.random.uniform(0, 1, n_particles)
        theta = 2 * np.pi * u
        phi = np.arccos(2 * v - 1)
        
        # Ellipsoidal spread expanding outward
        r = 10.0 * np.random.power(0.5, n_particles)
        hx = vx + 12.0 * ux + r * np.sin(phi) * np.cos(theta)
        hy = vy + 12.0 * uy + r * np.sin(phi) * np.sin(theta)
        hz = vz + 12.0 * uz + (r * 0.6) * np.cos(phi)
        
        # Plot head particles with high transparency (alpha) for a glowing look
        ax.scatter(hx, hy, hz, c=r, cmap='plasma', s=2, alpha=0.15, edgecolors='none')
        
        # B. The "Tentacles" (Fading exhaust wake trailing behind)
        n_wake = 1500
        wake_dist = np.random.uniform(0, 25, n_wake)
        spread = np.random.normal(0, 1.2, n_wake)
        
        wx = vx + wake_dist * ux + spread * np.random.randn(n_wake)
        wy = vy + wake_dist * uy + spread * np.random.randn(n_wake)
        wz = vz + wake_dist * uz + spread * np.random.randn(n_wake)
        
        ax.scatter(wx, wy, wz, c=wake_dist, cmap='inferno', s=1.5, alpha=0.1, edgecolors='none')

# --- 3. Ground References ---
ax.scatter([0], [0], [0], color='cyan', s=150, marker='^', label='Launch Site (Florida)')

# --- Formatting ---
ax.set_title('Simulated Twilight "Jellyfish" Plume (Particle Cloud)', fontsize=14, fontweight='bold', pad=20, color='white')
ax.set_xlabel('Downrange North (km)', labelpad=10)
ax.set_ylabel('Downrange East (km)', labelpad=10)
ax.set_zlabel('Altitude (km)', labelpad=10)
ax.set_zlim(0, 140)

# Clean up axes colors for the dark theme
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

ax.view_init(elev=25, azim=-45)
ax.legend(loc='upper left')

plt.tight_layout()
plt.savefig('jellyfish_particle_cloud.png', dpi=300, bbox_inches='tight')
print("Successfully generated particle-cloud plume plot.")
