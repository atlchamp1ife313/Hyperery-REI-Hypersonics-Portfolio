import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the coupled kinetics output
df = pd.read_csv('dual_track_coupled_kinetics_output.csv')

# Initialize 3D figure
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

x = df['Downrange_km']
y = df['Altitude_km']
z = df['TrackB_Baseline_Radiance_W_sr_m2']

# Scatter plot with thermal colormap
sc = ax.scatter(x, y, z, c=z, cmap='inferno', s=60, depthshade=True)

ax.set_xlabel('Downrange Distance (km)', labelpad=10)
ax.set_ylabel('Altitude (km)', labelpad=10)
ax.set_zlabel('Baseline Radiance (W/sr*m^2)', labelpad=10)
ax.set_title('3D Plume Radiance Profile Across Ascent Corridor', fontsize=14, pad=15)

fig.colorbar(sc, ax=ax, label='Radiance (W/sr*m^2)', pad=0.1)
plt.savefig('plume_3d_radiance.png', dpi=300, bbox_inches='tight')
plt.show()
print("📁 Saved 3D visualization as: plume_3d_radiance.png")
