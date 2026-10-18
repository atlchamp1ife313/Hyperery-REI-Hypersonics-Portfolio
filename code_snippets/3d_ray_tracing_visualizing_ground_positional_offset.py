import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- 3D Ray-Tracing Error & Deflection Visualization ---
n_0 = 1.0003
H_scale = 8.5
altitudes = np.linspace(200, 0, 100)

# Compute deflection profile
deflection = np.zeros_like(altitudes)
for i in range(1, len(altitudes)):
    h = altitudes[i]
    dn_dh = - (n_0 - 1.0) / H_scale * np.exp(-max(h, 0) / H_scale)
    deflection[i] = deflection[i-1] - dn_dh * 15.0

max_offset = deflection[-1] # ~0.0025 km

# Create 3D visualization showing the straight path vs the bending path ending in the offset
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Straight vacuum line down to origin (0,0,0)
ax.plot([0, 0], [0, 0], [200, 0], color='tab:blue', linestyle='--', linewidth=2.5, label='Unrefracted Line-of-Sight (Vacuum)')

# Refracted ray path curving out in 3D
theta = np.pi / 4 # Direction of deflection azimuth
x_path = deflection * np.cos(theta)
y_path = deflection * np.sin(theta)
ax.plot(x_path, y_path, altitudes, color='tab:red', linewidth=3.5, label='Refracted Photon Path ($\nabla n$ bending)')

# Mark the ground positional offset point
ax.scatter([x_path[-1]], [y_path[-1]], [0], color='red', s=100, zorder=5, label=f'Ground Offset: {max_offset:.4f} km')

ax.set_title('3D Ray-Tracing: Visualizing Ground Positional Offset', fontsize=12, fontweight='bold', pad=15)
ax.set_xlabel('X Deflection (km)', labelpad=10)
ax.set_ylabel('Y Deflection (km)', labelpad=10)
ax.set_zlabel('Altitude (km)', labelpad=10)
ax.legend(loc='upper left', fontsize=10)

ax.view_init(elev=30, azim=135)
plt.tight_layout()
plt.savefig('ray_tracing_3d_offset.png', dpi=300, bbox_inches='tight')
plt.close()
print("3D offset plot generated.")
