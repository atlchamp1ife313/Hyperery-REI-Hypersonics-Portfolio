import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Dark background for twilight contrast
plt.style.use('dark_background')
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

# --- Single Plume Origin (High Altitude Vacuum Zone) ---
vx, vy, vz = 300.0, 90.0, 85.0  # Location in upper atmosphere (km)

# Exhaust direction vector (pointing backward along flight path)
ux, uy, uz = -0.9, -0.3, -0.2  
mag = np.sqrt(ux**2 + uy**2 + uz**2)
ux, uy, uz = ux/mag, uy/mag, uz/mag

# --- Generate One Detailed Plume Structure ---
n_axial = 100
n_theta = 50
x_local = np.linspace(0, 40, n_axial)      # Length down the plume axis (km)
theta = np.linspace(0, 2 * np.pi, n_theta)
X_l, Theta_l = np.meshgrid(x_local, theta)

# Prandtl-Meyer / Vacuum Expansion Profile:
# Narrows near the nozzle, balloons out into a massive bell, then trails off
R_plume = 1.0 + 3.5 * (X_l / 5.0) * np.exp(-X_l / 15.0) + 0.1 * X_l

# Construct 3D mesh coordinates oriented along the exhaust vector
# (Using cross-products to find orthogonal local axes)
perp1_x, perp1_y, perp1_z = -uy, ux, 0.0
p1_mag = np.sqrt(perp1_x**2 + perp1_y**2)
if p1_mag > 0:
    perp1_x, perp1_y = perp1_x/p1_mag, perp1_y/p1_mag
else:
    perp1_x, perp1_y = 1.0, 0.0
perp2_x = uy * perp1_z - uz * perp1_y
perp2_y = uz * perp1_x - ux * perp1_z
perp2_z = ux * perp1_y - uy * perp1_x

X_mesh = vx + X_l * ux + R_plume * np.sin(Theta_l) * perp1_x + R_plume * np.cos(Theta_l) * perp2_x
Y_mesh = vy + X_l * uy + R_plume * np.sin(Theta_l) * perp1_y + R_plume * np.cos(Theta_l) * perp2_y
Z_mesh = vz + X_l * uz + R_plume * np.sin(Theta_l) * perp1_z + R_plume * np.cos(Theta_l) * perp2_z

# Plot the single smoothed plume surface
surf = ax.plot_surface(
    X_mesh, Y_mesh, Z_mesh, 
    cmap='plasma', 
    alpha=0.7, 
    linewidth=0, 
    antialiased=True
)

# Mark the rocket engine position
ax.scatter([vx], [vy], [vz], color='cyan', s=200, marker='o', label='Rocket Engine Position')

# --- Formatting ---
ax.set_title('Single High-Altitude Vacuum Plume Cross-Section', fontsize=14, fontweight='bold', pad=20, color='white')
ax.set_xlabel('Downrange North (km)', labelpad=10)
ax.set_ylabel('Downrange East (km)', labelpad=10)
ax.set_zlabel('Altitude (km)', labelpad=10)

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

ax.view_init(elev=25, azim=-60)
ax.legend(loc='upper left')

plt.tight_layout()
plt.savefig('single_plume_slice.png', dpi=300, bbox_inches='tight')
print("Successfully generated single plume slice plot.")
