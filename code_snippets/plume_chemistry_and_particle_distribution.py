import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Dark background to simulate the twilight sky aesthetic
plt.style.use('dark_background')
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

# --- 1. Plume Origin & Vector Orientation (High-Altitude Vacuum Zone) ---
vx, vy, vz = 300.0, 90.0, 85.0  # Location in upper atmosphere (km)

# Exhaust direction vector (pointing backward along flight path)
ux, uy, uz = -0.9, -0.3, -0.2  
mag = np.sqrt(ux**2 + uy**2 + uz**2)
ux, uy, uz = ux/mag, uy/mag, uz/mag

# Construct orthogonal local axes for proper 3D orientation
perp1_x, perp1_y = -uy, ux
p1_mag = np.sqrt(perp1_x**2 + perp1_y**2)
perp1_x, perp1_y = perp1_x/p1_mag, perp1_y/p1_mag
perp2_x = uy * 0.0 - uz * perp1_y
perp2_y = uz * perp1_x - ux * 0.0
perp2_z = ux * perp1_y - uy * perp1_x
p2_mag = np.sqrt(perp2_x**2 + perp2_y**2 + perp2_z**2)
if p2_mag > 0:
    perp2_x, perp2_y, perp2_z = perp2_x/p2_mag, perp2_y/p2_mag, perp2_z/p2_mag
else:
    perp2_x, perp2_y, perp2_z = 0.0, 0.0, 1.0

# --- 2. Overall Vacuum Expansion Envelope (Prandtl-Meyer Bell) ---
n_axial = 80
n_theta = 40
x_local = np.linspace(0, 45, n_axial)
theta = np.linspace(0, 2 * np.pi, n_theta)
X_l, Theta_l = np.meshgrid(x_local, theta)

# Gas dynamic expansion profile
R_plume = 1.2 + 4.0 * (X_l / 6.0) * np.exp(-X_l / 18.0) + 0.08 * X_l

X_mesh = vx + X_l * ux + R_plume * np.sin(Theta_l) * perp1_x + R_plume * np.cos(Theta_l) * perp2_x
Y_mesh = vy + X_l * uy + R_plume * np.sin(Theta_l) * perp1_y + R_plume * np.cos(Theta_l) * perp2_y
Z_mesh = vz + X_l * uz + R_plume * np.sin(Theta_l) * 0.0 + R_plume * np.cos(Theta_l) * perp2_z

# Plot translucent gas envelope
ax.plot_surface(X_mesh, Y_mesh, Z_mesh, color='purple', alpha=0.12, linewidth=0)

# --- 3. Chemical Species & Particle Layers ---
np.random.seed(42)

# A. PLASMA CORE & IONS (High temperature, near nozzle exit)
n_plasma = 1200
p_dist = np.random.uniform(0, 12, n_plasma)
p_spread = np.random.normal(0, 0.35, n_plasma)
px = vx + p_dist * ux + p_spread * perp1_x
py = vy + p_dist * uy + p_spread * perp1_y
pz = vz + p_dist * uz + p_spread * perp2_z
ax.scatter(px, py, pz, c=p_dist, cmap='autumn', s=3, alpha=0.6, label='Plasma Core ($H_3O^+$, Free Electrons)')

# B. CRYOGENIC ICE CRYSTALS / WATER VAPOR (The expanding jellyfish bell)
n_ice = 3500
u = np.random.uniform(0, 1, n_ice)
v = np.random.uniform(0, 1, n_ice)
th_ice = 2 * np.pi * u
ph_ice = np.arccos(2 * v - 1)
r_ice = 13.0 * np.random.power(0.5, n_ice)

ix = vx + 16.0 * ux + r_ice * np.sin(ph_ice) * perp1_x + r_ice * np.cos(ph_ice) * perp2_x
iy = vy + 16.0 * uy + r_ice * np.sin(ph_ice) * perp1_y + r_ice * np.cos(ph_ice) * perp2_y
iz = vz + 16.0 * uz + r_ice * np.sin(ph_ice) * 0.0 + r_ice * np.cos(ph_ice) * perp2_z
ax.scatter(ix, iy, iz, c=r_ice, cmap='cool', s=2, alpha=0.2, label='Cryogenic Ice Crystals ($H_2O_{(s)}$)')

# C. SOOT & COMBUSTION GASES (Carbon particles, CO2, CO trailing core)
n_soot = 2000
s_dist = np.random.uniform(4, 38, n_soot)
s_spread = np.random.normal(0, 0.7, n_soot)
sx = vx + s_dist * ux + s_spread * perp1_x
sy = vy + s_dist * uy + s_spread * perp1_y
sz = vz + s_dist * uz + s_spread * perp2_z
ax.scatter(sx, sy, sz, c=s_dist, cmap='copper', s=1.5, alpha=0.35, label='Combustion Gases & Soot ($CO_2, CO$)')

# --- 4. Engine & Formatting ---
ax.scatter([vx], [vy], [vz], color='cyan', s=180, marker='^', label='Merlin Vacuum Engine')

ax.set_title('SpaceX Plume Chemistry & Particle Distribution', fontsize=14, fontweight='bold', pad=20, color='white')
ax.set_xlabel('Downrange North (km)', labelpad=10)
ax.set_ylabel('Downrange East (km)', labelpad=10)
ax.set_zlabel('Altitude (km)', labelpad=10)

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

ax.view_init(elev=25, azim=-60)
ax.legend(loc='upper left', frameon=True, facecolor='black')

plt.tight_layout()
plt.savefig('plume_chemistry_model.png', dpi=300, bbox_inches='tight')
print("Successfully generated chemical species plume model.")
